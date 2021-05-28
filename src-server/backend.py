# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import base64
import re

hostName = "localhost"
serverPort = 8080
html = ""

def get_site(url):
    return requests.get(url).text

def add_css(html,url):
    matches = re.findall('src=["\'][^http].*?["\']|href=["\'][^http].*?["\']',html) #Don't diss the regex. It's beautiful
    print(matches)
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
    print(matches)
    for i in matches:
        j = i.replace("https://","http://localhost:8080/https://")
        html = html.replace(i,j)
    return html

def combine_path(abpath,relpath):
    if relpath[0] == "/":
        if relpath[1] == "/":
            return relpath
        else:
            print(relpath)
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

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        print(self.path)
        html = get_site(self.path[1:])
        html = add_css(html,self.path[1:])
        print(html)
        self.wfile.write(bytes(html,"utf-8"))
    def get_site(self,url):
        return requests.get(url).text
if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
