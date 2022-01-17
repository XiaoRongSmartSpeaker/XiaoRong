import requests
import json

# url = "http://140.122.185.210"
url = "http://localhost:8000"

def getDevice():
    r = requests.get(url+'/devicedata')
    return r.json

def addDevice(device):
    r = requests.post(url+'/devicedata', data=device)
    return r.status_code

def getAllUser():
    r = requests.get(url+'/userdata')
    return r.json()
def getUser(email=""):
    r = requests.get(url+'/userdata/'+email)
    if(r.status_code == 200):
        print("OK")
        return r.json
    else:
        return None

def addUser(user):
    r = requests.post(url+'/userdata', data=user)
    return r.status_code


# print(getAllUser())
print(getUser("kizato1018@gmail.com"))

# data = {"email":"abc", "name":"cde"}
# text = ""
# user = {"email":str, "name":str}

# text = json.dumps(data)
# user = json.loads(text)
# print(user["email"])