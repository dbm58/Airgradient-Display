#  =============================================================
#  Calculate remaining batter life
#
#  From a CircuitPython Parsec video.
#  LiPo is ~4.0v nominal fully charged
#  3.7v is kind of the "sweet spot"
#  Less than 3.7v means that charging is needed

import board
from analogio import AnalogIn

class Battery:
    def __init__(self):
        self.pin = AnalogIn(board.VOLTAGE_MONITOR)

    @property
    def voltage(self):
        return (self.pin.value * 3.3) / 65536 * 2

    @property
    def charge_needed(self):
        return self.voltage <= 3.7

#  =============================================================
#  Alternative implementation:
#
#      from adafruit_magtag.magtag import MagTag
#      magtab = MagTag()
#      print(magtab.peripherals.battery)
#
#  but if we use MagTag(), then Keypad doesn't work!
#  this isn't really integrated.


