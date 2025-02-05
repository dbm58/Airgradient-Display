import ssl
import wifi
import socketpool
import adafruit_requests
from secrets import secrets

def connect():
    print(f"Connecting to {secrets['ssid']}")
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print(f"Connected to {secrets['ssid']}")
    print(f"My IP address: {wifi.radio.ipv4_address}")

    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    return requests


