import displayio
import terminalio

from adafruit_display_text import label
from adafruit_display_shapes.roundrect import RoundRect

from colors import *

class Menu(displayio.Group):
    menu_background = SILVER

    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y

        item_attrs = {
            'anchor_point': (0, 0.5),
            'background_color': self.menu_background,
            'color': BLACK,
            'font': terminalio.FONT,
            'scale': 2,
            'text': '',
            }
        menu_attrs = {
            'x': 0,
            'y': 0,
            'width': width,
            'height': height,
            'r': 5,
            'fill': self.menu_background,
            'outline': BLACK,
            }

        self.append(RoundRect(**menu_attrs))
        self.append(label.Label(**item_attrs, anchored_position = (4, 20)))
        self.append(label.Label(**item_attrs, anchored_position = (4, 94)))
        self.append(label.Label(**item_attrs, anchored_position = (4, 168)))
        self.append(label.Label(**item_attrs, anchored_position = (4, 238)))
        self.hidden = False

    @property
    def items(self):
        return [item.text for item in self]
    @items.setter
    def items(self, value):
        for index, text in enumerate(value):
            # The RoundRect is [0], so add 1
            self[index + 1].text = text
