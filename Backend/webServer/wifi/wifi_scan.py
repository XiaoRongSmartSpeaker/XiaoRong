import os
import re
import json


class WiFi:

    def __init__(self):
        pass

    def scan(self):
        list_result = []

        scan = os.popen("sudo iwlist wlan1 scan", "r", -1).read()
        scan_split = scan.split("Cell", -1)

        for i in range(1, len(scan_split)):
            dict_result = {}
            mac = re.findall(
                r'Address: ([A-Z0-9]{2}:[A-Z0-9]{2}:[A-Z0-9]{2}:[A-Z0-9]{2}:[A-Z0-9]{2}:[A-Z0-9]{2})\s',
                scan_split[i])
            dict_result['MAC'] = mac[0]
            ssid = re.findall('ESSID:\"(.*?)\"', scan_split[i])
            dict_result['SSID'] = ssid[0]
            freq = re.findall('Frequency:(.*?)\n', scan_split[i])
            dict_result['Frequency'] = freq[0]
            Encryption = re.findall(r'key:(.*?)\s', scan_split[i])
            dict_result['Encryption'] = Encryption[0]
            # if Encryption == "on":
            #        Security = re.findall('',scan_split[i])
            #        dict_result['Security'] = Security[0]
            # else:
            #        dict_result['Security'] = "None"
            Quality = re.findall(r'Quality=(.*?)\s', scan_split[i])
            dict_result['Quality'] = Quality[0]
            Signal = re.findall(r'Signal level=(.*?)[\/\s]', scan_split[i])
            Signal[0] = int(Signal[0])
            if Signal[0] < 0:
                Signal[0] += 100
            dict_result['Signal'] = (str(Signal[0]) + "/100")
            list_result.append(dict_result)

        result = json.dumps(list_result, indent=4)
        return result
