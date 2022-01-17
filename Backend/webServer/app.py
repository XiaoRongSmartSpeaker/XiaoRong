from asyncio.windows_events import NULL
from flask import Flask, request, render_template, redirect
# from flask.wrappers import Request
import sys
import os
from wifi import wifi_connect, wifi_scan
# import test.scan as scan
# import test.connect as connect
import test.signin as sign
import test.setting as setup
import test.server as server
import json
#from flask_cors import CORS, cross_origin

frontend_path = "../../Frontend/public/pages"
app = Flask(__name__, static_url_path='', static_folder=frontend_path ,template_folder=frontend_path)
#CORS(app, support_credentials=True)


user = {
    "user_name": str,
    "user_email": str,
    "access_token":str,
    "client_secret":str,
    "language":str
}
device = {
    "device_id":str,
    "device_name":str,
    "language":str,
    "system_volume":50,
    "media_volume":50, 
    "region":str,
    "time_zone":str,
    "user_email":str
}


@app.route("/")
def hello():
    return redirect("index.html")

@app.route("/wifis")
def wifis():
    result = wifi_scan.WiFi().scan()
    print(result)
    return result
    # return render_template('wifi.html')

@app.route('/setting_wifi', methods=['PUT'])
def setting_wifi():
    if request.method == 'PUT':
        wifi = json.loads(request.data)
        isConnected = wifi_connect.CreateWifiConfig(wifi["SSID"], wifi["password"])
        # print(json.loads(request.data))
        response = {'isConnected':isConnected}
    return json.dumps(response)

@app.route('/user_info', methods=['POST'])
def signin():
    # print('hello')
    if request.method == 'POST':
        user = server.getUser(request.data["email"])
        if(user == NULL):
            user["access_token"] = request.data["access_token"]
            user["client_secret"] = request.data["client_secret"]
            user["user_email"] = request.data["email"]
            user["user_name"] = request.data["full_name"]
        
        sign.signin(request.data)
        response = {'Success': True}
    elif request.method == 'GET':
        response = {'Success': False}
    return json.dumps(response)

@app.route('/speaker_info', methods=['POST'])
def setting():
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    device["device_id"] = cpuserial
    device["device_name"] = request.data['speaker_name']
    device["region"] = request.data['time']
    device["time_zone"] = request.data['location']
    device["language"] = request.data["language"]
    device["user_email"] = user["user_email"]
    setup.setup(request.data)
    server.addDevice(device)
    response = {'Success': True}
    return json.dumps(response)

@app.route('/<path:path>')
def serve_page(path):
    print(path)
    return render_template(path)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
