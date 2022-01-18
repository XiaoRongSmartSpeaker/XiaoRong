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
    os.system("sudo wpa_cli -i wlan1 reconfigure")
    os.system("sudo systemctl daemon-reload")
    os.system("sudo systemctl restart dhcpcd")
