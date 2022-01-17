import json

def connect_wifi(data):
    data = json.loads(data)
    print('Connect:')
    print('SSID:'+data['SSID'])
    print('password:'+data['password'])
    if(data['SSID'] == 'wifi1'):
        print('false')
        return False
    return True