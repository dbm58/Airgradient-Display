import json
# ----
import time
import board
import displayio
import terminalio
from adafruit_display_text import label

class Airgradient:
    def fetch(self, requests, sn):
        url = f"http://airgradient_{sn}.local/measures/current"

        print(f"Fetching from airgradient {sn}")
        response = requests.get(url)
        data = response.json()
        print("-" * 40)
        print(json.dumps(data))
        print(data['rco2'])
        print(f"{data['rco2']}")
        print("-" * 40)
        return AirgradientData(data)

class AirgradientData:
    def __init__(self, data):
        self.data = data

    @property
    def co2(self):
        return round(self.data['rco2'])

