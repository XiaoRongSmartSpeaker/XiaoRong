import requests
import json

url = "http://www.xiaorongserver.tk"
# url = "http://localhost:8000"

def getDevice(device):
    r = requests.get(url+'/devicedata/'+device)
    return r.json()

def addDevice(device):
    r = requests.post(url+'/devicedata', data=device)
    return r.status_code

def getAllUser():
    r = requests.get(url+'/userdata')
    print("status code:" + str(r.status_code))
    return r.json()
def getUser(email=""):
    r = requests.get(url+'/userdata/'+email)
    print("status code:" + str(r.status_code))
    if(r.status_code == 200):
        print("OK")
        return r.json()
    else:
        return None

def addUser(user):
    r = requests.post(url+'/userdata', data=user)
    print("status code:" + str(r.status_code))
    return r.status_code

def getToken(device_id:str):
    r = requests.get(url+"/userdata/get_token/"+device_id)
    print("status code:" + str(r.status_code))
    return r.json()

def addLog(device_id:str, msg:str):
    data = json.dumps({
        "device_id": device_id,
        "message": msg
    })
    
    r = requests.post(url+'/log', data=data)
    print("status code:" + str(r.status_code))
    return r.status_code

def getLog(device_id:str):
    r = requests.get(url+"/log/"+device_id)
    print("status code:" + str(r.status_code))
    return r.json()

def isPlaying(device_id:str):
    data = {
        "isPlaying":True,
        "isPause":False,
        "isStop":False,
        "device_id":device_id
    }
    r = requests.put(url+"/devicedata/playing/"+device_id, data=data)
    print("status code:" + str(r.status_code))
    return r.status_code

def isPause(device_id:str):
    data = {
        "isPlaying":False,
        "isPause":True,
        "isStop":False,
        "device_id":device_id
    }
    r = requests.put(url+"/devicedata/playing/"+device_id, data=data)
    print("status code:" + str(r.status_code))
    return r.status_code

def isStop(device_id:str):
    data = {
        "isPlaying":False,
        "isPause":False,
        "isStop":True,
        "device_id":device_id
    }
    r = requests.put(url+"/devicedata/playing/"+device_id, data=data)
    print("status code:" + str(r.status_code))
    return r.status_code


# print(getAllUser())
# print(getUser("kizato1018@gmail.com"))

# # data = {"email":"abc", "name":"cde"}
# # text = ""
# # user = {"email":str, "name":str}

# # text = json.dumps(data)
# # user = json.loads(text)
# # print(user["email"])

# user = {
#     "user_name": "kizato",
#     "user_email": "kizato1018@gmail.com",
#     "access_token": "123456",
#     "client_secret": "654321",
#     "language": "tw"
# }

# print(addUser(json.dumps(user)))
# print(getToken("00000000000001"))
# device = "ERROR000000000"

# print(addLog(device, "hello world"))
# print(addLog(device, "i am xiaorong"))
# print(getLog(device))