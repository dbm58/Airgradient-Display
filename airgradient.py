import json

import log

class Airgradient:
    def fetch(self, requests, sn):
        url = f"http://airgradient_{sn}.local/measures/current"

        log.info("Fetching from airgradient %s", sn)
        response = requests.get(url)
        data = response.json()
        log.info("-" * 40)
        log.info(json.dumps(data))
        log.info("-" * 40)
        return AirgradientData(data)

class AirgradientData:
    def __init__(self, data):
        self.data = data

    def get_value(self, prop):
        return round(self.data[prop])
        
    @property
    def co2(self):
        return round(self.data['rco2'])

