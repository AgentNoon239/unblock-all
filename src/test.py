import threading
import requests

def getsite(url,thread):
    print("Beginning of loop:",thread)
    requests.get(url)
    print("End of loop:",thread)

#x = threading.Thread(target=getsite, args=("https://realpython.com/async-io-python/#setting-up-your-environment","x"))
#y = threading.Thread(target=getsite, args=("https://github.com/AgentNoon239/unblock-all/blob/main/src-server/backend.py","y"))
#x.start()
#y.start()
getsite("https://realpython.com/async-io-python/#setting-up-your-environment",1)
getsite("https://github.com/AgentNoon239/unblock-all/blob/main/src-server/backend.py",2)
