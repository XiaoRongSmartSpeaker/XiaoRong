from asyncio.windows_events import NULL
import requests
import json

# url = "http://140.122.185.210"
url = "http://localhost:8000"

def getDevice():
    r = requests.get(url+'/devicedata')
    return json.loads(r.json())

def addDevice(device):
    r = requests.post(url+'/devicedata', data=device)
    return json.loads(r.json())

def getAllUser():
    r = requests.get(url+'/userdata')
    return json.loads(r.json())
def getUser(email=""):
    r = requests.get(url+'/userdata/'+email)
    if(r.status_code == 200):
        return json.loads(r.json())
    else:
        return NULL

def addUser(user):
    r = requests.post(url+'/userdata', data=user)
    return json.loads(r.json())

def getToken():
    r = requests.get(url+'/googletoken')
    return json.loads(r.json())

def addToken(token):
    r = requests.post(url+'/googletoken', data=token)
    return json.loads(r.json())


print(getAllUser())
# print(getUser("kizato1018@gmail.com"))

# data = {"email":"abc", "name":"cde"}
# text = ""
# user = {"email":str, "name":str}

# text = json.dumps(data)
# user = json.loads(text)
# print(user["email"])