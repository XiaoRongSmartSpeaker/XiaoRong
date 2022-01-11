from flask import Flask, request, render_template, redirect
# from flask.wrappers import Request
import os
from ..WiFi import wifi_connect, wifi_scan
# import test.scan as scan
# import test.connect as connect
import test.signin as sign
import test.setting as setup
import json


frontend_path = "../../Frontend/public/pages"
app = Flask(__name__, static_url_path='', static_folder=frontend_path ,template_folder=frontend_path)
@app.route("/")
def hello():
    return redirect("index.html")

@app.route("/wifis")
def wifis():
    result = wifi_scan.WiFi.scan()
    print(result)
    return result
    # return render_template('wifi.html')

@app.route('/setting_wifi', methods=['PUT'])
def setting_wifi():
    if request.method == 'PUT':
        wifi = json.loads(request.data)
        isConnected = wifi_connect.WiFiConnect(wifi["SSID"], wifi["password"])
        # print(json.loads(request.data))
        response = {'isConnected':isConnected}
    return json.dumps(response)

@app.route('/user_info', methods=['POST'])
def signin():
    print('hello')
    if request.method == 'POST':
        sign.signin(request.data)
        response = {'Success': True}
    elif request.method == 'GET':
        response = {'Success': False}
    return json.dumps(response)

@app.route('/speaker_info', methods=['POST'])
def setting():
    setup.setup(request.data)
    response = {'Success': True}
    return json.dumps(response)

@app.route('/<path:path>')
def serve_page(path):
    print(path)
    return render_template(path)

if __name__ == '__main__':
    app.run(debug=True)