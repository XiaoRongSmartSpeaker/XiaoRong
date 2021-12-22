from flask import Flask, request, render_template
# from flask.wrappers import Request
import test.scan as scan
import test.connect as connect
import test.signin as sign
import test.setting as setup
import json


frontend_path = "../../Frontend/public/pages"
app = Flask(__name__, static_url_path='', static_folder=frontend_path ,template_folder=frontend_path)
@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/wifis")
def wifis():
    return json.dumps(scan.scan_wifi())
    # print(scan_wifi())
    # return render_template('wifi.html')

@app.route('/setting_wifi', methods=['PUT'])
def setting_wifi():
    if request.method == 'PUT':
        isConnected = connect.connect_wifi(request.data)
        # print(json.loads(request.data))
        response = {'isConnected':isConnected}
    return json.dumps(response)

@app.route('/signin', methods=['POST'])
def signin():
    print('hello')
    if request.method == 'POST':
        sign.signin(request.data)
        response = {'Success': True}
    elif request.method == 'GET':
        response = {'Success': False}
    return json.dumps(response)

@app.route('/setting', methods=['POST'])
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