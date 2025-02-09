
import time
import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from .base import Base


class Horizontal(Base):
    def __init__(self):
        self.rotation = 270
        super().__init__()
        
    def setup_display(self):
        self.set_background()
        
        self._location.scale = 2
        self._location.anchor_point = (0.5, 0)
        self._location.anchored_position = (self.display.width // 2, 0)
        self.main_group.append(self._location)
        
        self._value1.anchor_point = (0.5, 0.5)
        self._value1.anchored_position = (self.display.width // 2, self.display.height // 2)
        self._value1.font = self.value_font
        self._value1.scale = 3
        self.main_group.append(self._value1)
        
        self.battery_group = displayio.Group()
        self.main_group.append(self.battery_group)
        self.battery_icon = self.icon("low-battery.bmp", 260, 100)
