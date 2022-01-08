import pywifi
import time
import json

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[1]
iface.scan()
time.sleep(5)
results = iface.scan_results()

list_result = []

for i in results:
        dict_result = {}
        dict_result['bssid'] = i.bssid
        dict_result['ssid']  = i.ssid
        dict_result['freq'] = i.freq
        dict_result['auth'] = i.auth
        dict_result['akm'] = i.akm
        dict_result['signal'] = i.signal
        list_result.append(dict_result)

with open("WiFi_Info.json","w") as f:
        json.dump(list_result, f, indent = 4)