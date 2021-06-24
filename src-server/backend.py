# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import re

#Configuring globals
hostName = "localhost"
serverPort = 8080
url = None

#Configuring logging setup
import logging
import traceback
handler = logging.FileHandler(r"C:/Users/abc/Desktop/Tools/Python/unblock-all/src-server/main.log","w")
formatter = logging.Formatter("%(asctime)-15s : %(name)s : %(levelname)-8s :: %(url)s : %(trace)s : %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger("Core")
logger.setLevel("DEBUG")
logger.addHandler(handler)
#Logging helper function
def catch(type,e):
    if type == "error" or type == "critical":
        getattr(logger,type)(str(e),extra={"url":url,"trace":traceback.format_tb(e.__traceback__)})
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
                f = open("C:/Users/abc/Desktop/Tools/Python/unblock-all/src-server/main.log","r")
                logs = f.read().replace("\n","<br>") #Converting to HTML for rendering
                self.wfile.write(bytes("<p>"+logs+"</p>","utf-8"))
                f.close()
            #Internal command for bug reporting
            elif url[0:10] == "$%3Ereport": #Escape string for $>report
                raise Exception("User reported error")
                url = self.path[10:]
                self._headers()
            #Default functionality
            else:
                self._headers()
                self.wfile.write(bytes(format_site(url),"utf-8"))
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
    html = re.replace('<title>.*?</title>',<title>index.html</title>)
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
        j = i.replace("https://","http://localhost:8080/https://")
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

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    catch("info","Server online")
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except Exception as e:
        catch("critical",e)
    webServer.server_close()
    print("Server stopped.")
