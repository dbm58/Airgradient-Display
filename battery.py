
# -----------------------
# Calculate remaining batter life
# From a CircuitPython Parsec video.
# LiPo is ~4.0v nominal fully charged
# 3.7v is kind of the "sweet spot"
# Less than 3.7v means that charging is needed
# import board # Already imported
#from analogio import AnalogIn
#pin = AnalogIn(board.VOLTAGE_MONITOR)
#battery_voltage = (pin.value * 3.3) / 65536 * 2
# if < 3.7, put up a "charge me" icon
# this is all already in the magtag library?
# yes!
# from adafruit_magtag.magtag import MagTag
# magtab = MagTag()
# print(magtab.peripherals.battery)
# but if we use MagTag(), then Keypad doesn't work!
# this isn't really integrated.


