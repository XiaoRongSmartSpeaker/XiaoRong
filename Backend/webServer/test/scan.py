wifi_list = [
    {
        "SSID" : "wifi1" ,
        "Frequency" : "2.4 GHz" ,
        "Encryption_key" : "on" ,
        "Security" : "WPA-EAP",
        "Quality" : "72/100" ,
        "Signal_level" : "43/100"
    },
    {
        "SSID" : "wifi2" ,
        "Frequency" : "5 GHz" ,
        "Encryption_key" : "on" ,
        "Security" : "WPA2-PSK",
        "Quality" : "88/100" ,
        "Signal_level" : "42/100"
    }
]

def scan_wifi():
    return wifi_list