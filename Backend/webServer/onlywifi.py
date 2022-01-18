from flask import Flask, request, render_template, redirect
# from flask.wrappers import Request
import sys
import os
from wifi import wifi_connect, wifi_scan
# import test.scan as scan
# import test.connect as connect
import test.signin as sign
import test.setting as setup
import json
#from flask_cors import CORS, cross_origin

frontend_path = "../../Frontend/public/pages"
app = Flask(
    __name__,
    static_url_path='',
    static_folder=frontend_path,
    template_folder=frontend_path)
#CORS(app, support_credentials=True)


@app.route("/")
def hello():
    return redirect("wifi.html")


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
        isConnected = wifi_connect.CreateWifiConfig(
            wifi["SSID"], wifi["password"])
        # print(json.loads(request.data))
        response = {'isConnected': isConnected}
    return json.dumps(response)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
