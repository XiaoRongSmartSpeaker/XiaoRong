import requests

url = "http://140.122.185.210"

def getDevice():
    r = requests.get(url+'/devicedata')
    return r.json()

def addDevice(device):
    r = requests.post(url+'/devicedata', data=device)
    return r.json()

print(getDevice())