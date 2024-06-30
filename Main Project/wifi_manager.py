import network
from config import WIFI_SSID, WIFI_PASS

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            pass
    print('WiFi connected:', wlan.ifconfig()[0])
