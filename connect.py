import os
import ssl
import wifi
import socketpool
import adafruit_requests

def connect():
    ssid = os.getenv('wifi_ssid')
    password = os.getenv('wifi_password')
    print(f"Connecting to {ssid}")
    wifi.radio.connect(ssid, password)
    print(f"Connected to {ssid}")
    print(f"My IP address: {wifi.radio.ipv4_address}")

    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    return requests


