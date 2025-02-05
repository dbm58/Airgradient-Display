
class Devices:
    def __init__(self):
        self.current_device = 0
        self.devices = [
            { 'sn': '744dbdbf1dc4', 'descr': 'Basement'   },
            { 'sn': '404cca6dcc38', 'descr': 'Main Floor' },
            { 'sn': '404cca6eb068', 'descr': 'Top Floor'  },
        ]

    @property
    def current(self):
        dev = self.devices[self.current_device]
        return dev['sn'], dev['descr']

    def next(self):
        self.current_device = (self.current_device + 1) % 3
        return self.current

