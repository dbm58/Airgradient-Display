import board
import displayio
import terminalio

from adafruit_display_text import label
from adafruit_display_shapes.roundrect import RoundRect

from colors import *
from icon import Icon

class Dialog(displayio.Group):
    menu_background = SILVER

    def __init__(self, x=10, y=10, icon=None):
        super().__init__(x=x, y=y)

        menu_attrs = {
            'x': 0,
            'y': 0,
            'width': board.DISPLAY.width - (2 * x),
            'height': board.DISPLAY.height - (2 * y),
            'r': 5,
            'fill': self.menu_background,
            'outline': BLACK,
            }

        self.append(RoundRect(**menu_attrs))

        if not icon == None:
            icon = Icon(icon)
            icon.x = int((menu_attrs['width'] / 2) - (icon.width / 2))
            icon.y = int((menu_attrs['height'] / 2) - (icon.height / 2))
            self.append(icon)

class Dialogs():
    WIFI_OFF = Dialog(icon='wifi-off.bmp')
    HOURGLASS = Dialog(icon='hourglass.bmp')
    BATTERY_ALERT = Dialog(icon='battery-alert-48.bmp')
