#  =============================================================================
#  Calculate remaining batter life
#
#  From a CircuitPython Parsec video.
#  LiPo is ~4.0v nominal fully charged
#  3.7v is kind of the "sweet spot"
#  Less than 3.7v means that charging is needed

import board
import digitalio
import log

from analogio import AnalogIn

class Battery:
    def __init__(self):
        self.pin = AnalogIn(board.VOLTAGE_MONITOR)
        self.usb_power_pin = digitalio.DigitalInOut(board.NEOPIXEL_POWER)
        self.usb_power_pin.direction = digitalio.Direction.INPUT

    @property
    def voltage(self):
        return (self.pin.value * 3.3) / 65536 * 2

    @property
    def on_external_power(self):
        return self.usb_power_pin.value

    @property
    def charge_needed(self):
        if self.on_external_power:
            log.debug("Running on external power!")
            return False
        log.debug("Running on battery!")
        return self.voltage <= 3.7

#  =============================================================================
#  Alternative implementation:
#
#      from adafruit_magtag.magtag import MagTag
#      magtab = MagTag()
#      print(magtab.peripherals.battery)
#
#  but if we use MagTag(), then Keypad doesn't work!
#  this isn't really integrated.


