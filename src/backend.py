# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import re
import threading
import collections
import sys
from time import sleep
from json import load

#Configuring globals
config = load(open(r"src\config.json"))
url = None
lock = threading.Lock()
waiting = False

#Configuring logging setup
import logging
import traceback
handler = logging.FileHandler(r"src/main.log","w")
formatter = logging.Formatter("%(asctime)-15s : %(name)s : %(levelname)-8s :: %(url)s : %(trace)s : %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger("Core")
logger.setLevel("DEBUG")
logger.addHandler(handler)

#Logging helper function
def catch(type,e):
    if type == "error" or type == "critical":
        getattr(logger,type)(str(e),extra={"url":url,"trace":traceback.format_tb(e.__traceback__,limit=1)})
    else:
        getattr(logger,type)(str(e),extra={"url":url,"trace":None})

catch("info","Logging system online")

#Server class will process indivual requests
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path[1:] #Shorthand
        try:
            #Command for logs access
            if str(url) == "$%3Elog": #Escape string for $>log
                self._headers()
                f = open("main.log","r")
                logs = f.read().replace("\n","<br>") #Converting to HTML for rendering
                self.wfile.write(bytes("<p>"+logs+"</p>","utf-8"))
                f.close()
            elif str(url) == "$%3Ecache":
                self._headers()
                with lock:
                    self.wfile.write(bytes("<p>"+str(c.memory.keys())+"</p>","utf-8"))
            #Internal command for bug reporting
            elif url[0:10] == "$%3Ereport": #Escape string for $>report
                raise Exception("User reported error")
                url = self.path[10:]
                self._headers()
            #Default functionality
            else:
                url = "https://"+url
                self._headers()
                waiting = True
                with lock:
                    file = c.get(url)
                    if file == None:
                        file = format_site(url)
                        c.add(url,file)
                waiting = False
                self.wfile.write(bytes(file,"utf-8"))
                catch("info","Serviced request for "+url)
            #Handling and recording of exceptions
        except Exception as e:
            print(type(e))
            if isinstance(e,requests.exceptions.MissingSchema): #Checking for common exceptions
                catch("warning",e)
            else:
                catch("error",e)
    #Post request logger before implementation
    def do_POST(self):
        catch("warning","Post error not implemented")

    def _headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        return

def format_site(url):
    html = requests.get(url).text
    html = re.sub('<title>.*?</title>','<title>index.html</title>',html)
    matches = re.findall('src=["\'][^http].*?["\']|href=["\'][^http].*?["\']',html) #Don't diss the regex. It's beautiful
    newmatches = []
    parsedurl = url.replace("/","/,").split(",") #Parseurl
    parsedurl[0] = parsedurl[0] + parsedurl[1] + parsedurl[2]
    del parsedurl[1:3]
    for i in matches:
        if i[0] == "s":
            newmatches.append(i[:5]+combine_path(parsedurl,i[5:]))
        elif i[0] == "h":
            newmatches.append(i[:6]+combine_path(parsedurl,i[6:]))
        else:
            print(i[0]+" Present at the front of string")
            raises
    if len(newmatches) != len(matches):
        print("Match incorrect")
        raise
    for i in range(len(matches)):
        html = html.replace(matches[i],newmatches[i])
    matches = re.findall('<a.*?href=["\'].*?["\']',html)
    for i in matches:
        j = i.replace("https://",config["domain"])
        html = html.replace(i,j)
    return html

def combine_path(abpath,relpath):
    if relpath[0] == "/":
        if relpath[1] == "/":
            return relpath
        else:
            return abpath[0]+relpath[1:]
    if relpath[1] == ".":
        abpath = abpath[0:-1*(relpath.find("/"))]
        return concat_list(abpath) + relpath[relpath.find("/")+1:]
    else:
        return concat_list(abpath[:-1])+relpath

def concat_list(lst):
    concatlst = ""
    for l in lst:
        concatlst += l
    return concatlst

class cache():
    def __init__(self):
        self.memory = collections.OrderedDict()
        self.size = 0
    def add(self,url,file):
        self.memory[url] = file #Inserts at the end of the cache so will be last removed
        self.size += sys.getsizeof(file) #Adds size to size total
    def get(self,url):
        if url in self.memory:
            self.memory.move_to_end(url,True)
            return self.memory[url]
    def maintain(self):
        while True: #Daemon thread so loops forever until exit
            with lock:
                while not waiting and self.size > config["cacheSize"]*1000000:
                    self.size -= sys.getsizeof(self.memory.popitem(False)[1]) #Removes the last item and subtracts its size
            sleep(10)

if __name__ == "__main__":
    print(config)
    webServer = HTTPServer((config["hostName"], config["serverPort"]), MyServer)
    c = cache()
    catch("info","Server online")
    print("Server started http://%s:%s" % (config["hostName"], config["serverPort"]))
    #Configuring the threading setup
    try:
        mthread = threading.Thread(target=webServer.serve_forever)
        cthread = threading.Thread(target=c.maintain,daemon=True)
        mthread.start()
        cthread.start()
    except Exception as e:
        catch("critical",e)
