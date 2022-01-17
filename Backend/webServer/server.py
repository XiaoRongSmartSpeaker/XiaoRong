import requests

r = requests.get('http://140.122.185.210/userdata')
print(r.json())
r = requests.get('http://140.122.185.210/devicedata')
print(r.json())