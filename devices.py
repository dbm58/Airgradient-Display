import os

class Devices:
    def __init__(self):
        self.current_device = 0
        locations_env = os.getenv('locations')
        self.devices = list(map(
            lambda l, s: { 'sn': s, 'descr': l },
            map(lambda l: l.split(':')[0], locations_env.split(',')),
            map(lambda l: l.split(':')[1], locations_env.split(','))
            ))

    @property
    def current(self):
        dev = self.devices[self.current_device]
        return dev['sn'], dev['descr']

    def next(self):
        self.current_device = (self.current_device + 1) % 3
        return self.current

