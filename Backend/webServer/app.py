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
    "system_volume":int,
    "media_volume":int, 
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
    device['dev_name'] = request.data['speaker_name']
    device['time_zone'] = request.data['time']
    device['region'] = request.data['location']
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
