
import time
import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from .base import Base


class Vertical(Base):
    def __init__(self):
        self.rotation = 0
        super().__init__()
        
    def setup_display(self):
        self.set_background()
        
        self._location.scale = 2
        self._location.font = self.location_font
        self._location.text = 'Main Floor'
        self._location.anchor_point = (0.5, 0)
        self._location.anchored_position = (self.display.width // 2, 6)
        self.main_group.append(self._location)

        label_height = (self._location.height * 2) + 6        
        y = (self.display.height - label_height) // 6
        
        self._value1.font = self.value_font
        self._value1.scale = 2
        self._value1.text = '999'
        self._value1.anchor_point = (0.5, 0.5)
        self._value1.anchored_position = (self.display.width // 2, label_height + y)
        self.main_group.append(self._value1)

        self._value1_label.anchor_point = (0.5, 0)
        self._value1_label.anchored_position = (self.display.width // 2, self._value1.y + self._value1.height)
        self.main_group.append(self._value1_label)
        
        self._value2.font = self.value_font
        self._value2.scale = 2
        self._value2.text = '999'
        self._value2.anchor_point = (0.5, 0.5)
        self._value2.anchored_position = (self.display.width // 2, label_height + y * 3)
        self.main_group.append(self._value2)
        
        self._value2_label.anchor_point = (0.5, 0)
        self._value2_label.anchored_position = (self.display.width // 2, self._value2.y + self._value2.height)
        self.main_group.append(self._value2_label)
        
        self._value3.font = self.value_font
        self._value3.scale = 2
        self._value3.text = '999'
        self._value3.anchor_point = (0.5, 0.5)
        self._value3.anchored_position = (self.display.width // 2, label_height + y * 5)
        self.main_group.append(self._value3)
        
        self._value3_label.anchor_point = (0.5, 0)
        self._value3_label.anchored_position = (self.display.width // 2, self._value3.y + self._value3.height)
        self.main_group.append(self._value3_label)
        
        self.battery_group = displayio.Group()
        self.main_group.append(self.battery_group)
        self.battery_icon = self.icon("low-battery.bmp", self.display.width - 24, self.display.height - 24)
        
