import requests

url = "http://140.122.185.210"

def getDevice():
    r = requests.get(url+'/devicedata')
    return r.json()

def addDevice(device):
    r = requests.post(url+'/devicedata', data=device)
    return r.json()

def getUser():
    r = requests.get(url+'/userdata')
    return r.json()

def addUser(user):
    r = requests.post(url+'/userdata', data=user)
    return r.json()

def getToken():
    r = requests.get(url+'/googletoken')
    return r.json()

def addToken(token):
    r = requests.post(url+'/googletoken', data=token)
    return r.json()


print(getDevice())