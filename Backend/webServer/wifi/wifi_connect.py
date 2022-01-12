import os

def CreateWifiConfig(SSID, password):
        config_lines = [
                '\n'
                'network={',
                '\tssid="{}"'.format(SSID),
                '\tpsk="{}"'.format(password),
                '\tkey_mgmt=WPA-PSK',
                '}'
        ]

        config = '\n'.join(config_lines)
        print(config)

        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a+") as wifi:
                wifi.write(config)

        print("Wifi config added")
        os.system("wpa_cli -i wlan1 reconfigure")

def WiFiConnect(SSID, password):
    connect = os.system("sudo iw wlan0 " + SSID + " keys d:0:" + password)
    return connect