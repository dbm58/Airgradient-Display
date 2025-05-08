import os
import socketpool
import ssl
import wifi

import adafruit_requests

import log

def connect():
    ssid = os.getenv('wifi_ssid')
    password = os.getenv('wifi_password')
    log.info(f"Connecting to {ssid}")
    wifi.radio.connect(ssid, password)
    log.info(f"Connected to {ssid}")
    log.info(f"My IP address: {wifi.radio.ipv4_address}")

    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    return requests


