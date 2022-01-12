import os
import re
import json

class WiFi:

        def __init__(self):
                pass

        def scan(self):
                list_result = []

                # scan = os.popen("sudo iwlist wlan1 scan","r",-1).read()
                scan = os.popen("sudo iwlist wlan0 scan","r",-1).read()

                mac = re.findall('Address: ([A-Z0-9]{2}:[A-Z0-9]{2}:[A-Z0-9]{2}:[A-Z0-9]{2}:[A-Z0-9]{2}:[A-Z0-9]{2})\s',scan)
                ssid = re.findall('ESSID:\"(.*?)\"',scan)
                freq = re.findall('Frequency:(.*?)\n',scan)
                Encryption = re.findall('key:(.*?)\s',scan)
                #Security = re.findall('',scan)
                Quality = re.findall('Quality=(.*?)\s',scan)
                Signal = re.findall('Signal level=(.*?)\n',scan)

                for i in range(0,len(mac)):
                        dict_result = {}
                        dict_result['MAC'] = mac[i]
                        dict_result['SSID']  = ssid[i]
                        dict_result['Frequency'] = freq[i]
                        dict_result['Encryption'] = Encryption[i]
                        dict_result['Quality'] = Quality[i]
                        dict_result['Signal'] = Signal[i]
                        list_result.append(dict_result)

                result = json.dumps(list_result, indent = 4)
                return result

