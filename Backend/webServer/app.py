from flask import Flask, request, render_template, redirect
# from flask.wrappers import Request
import sys
import os
from wifi import wifi_connect, wifi_scan
# import test.scan as scan
# import test.connect as connect
import test.signin as sign
import test.setting as setup
# import test.server as server
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
    "isPlaying":False,
    "isPause":False,
    "isStop":True,
    "user_email":str
}


@app.route("/")
def hello():
    return redirect("index.html")

@app.route("/wifis")
def wifis():
    result = wifi_scan.WiFi().scan()
    # result = json.dumps(scan.scan_wifi())
    print(result)
    return result
    # return render_template('wifi.html')

@app.route('/setting_wifi', methods=['PUT'])
def setting_wifi():
    if request.method == 'PUT':
        print(request.json)
        wifi = request.json
        isConnected = wifi_connect.CreateWifiConfig(wifi["SSID"], wifi["password"])
        # print(json.loads(request.json))
        response = {'isConnected':isConnected}
    return json.dumps(response)

@app.route('/user_info', methods=['POST'])
def signin():
    global user
    # print('hello')
    if request.method == 'POST':
        user["access_token"] = request.json["access_token"]
        user["client_secret"] = request.json["client_secret"]
        user["user_name"] = request.json["full_name"]
        user["language"] = request.json["language"]
        user["user_email"] = request.json["email"]
        # if(not server.getUser(user["user_email"])):
        #     if server.addUser(json.dumps(user)) == 201:
        #         response = {'Success': True}
        #     else:
        #         response = {'Success': False}
        # else:
        #     response = {'Success': True}
        sign.signin(json.dumps(user))
        response = {'Success': True}

    elif request.method == 'GET':
        response = {'Success': False}
    return json.dumps(response)

@app.route('/speaker_info', methods=['POST'])
def setting():
    global device
    global user
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
    device["device_name"] = request.json['speaker_name']
    device["region"] = request.json['time']
    device["time_zone"] = request.json['location']
    device["language"] = request.json["language"]
    device["user_email"] = user["user_email"]
    print(user)
    print(device)
    # server.addDevice(json.dumps(device))
    setup.setup(json.dumps(device))
    response = {'Success': True}
    return json.dumps(response)

@app.route('/done', methods=['GET'])
def done():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/<path:path>')
def serve_page(path):
    print(path)
    return render_template(path)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
