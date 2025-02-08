
import time
import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font


class Display:
    display = None
    main_group = None
    value_font = None
    
    _location = None
    _value1 = None
    _value1_label = None
    _value2 = None
    _value2_label = None
    _value3 = None
    _value3_label = None
    
    _charge_needed = False

    def __init__(self):
        font_path = "/fonts/LibreBodoniv2002-Bold-27.bdf"
        self.value_font = bitmap_font.load_font(font_path, displayio.Bitmap)
        #font = terminalio.FONT

        self.display = board.DISPLAY
        self.display.rotation = 0
        self.main_group = displayio.Group()

        bg_bitmap = displayio.Bitmap(self.display.width, self.display.height, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = 0xFFFFFF
        bg_sprite = displayio.TileGrid(bg_bitmap, x=0, y=0, pixel_shader=bg_palette)
        bg_group = displayio.Group()
        bg_group.append(bg_sprite)
        self.main_group.append(bg_group)

        self._location = self.add_label(0, 6, 'Main Floor')
        self._location.scale = 2
        label_height = (self._location.height * 2) + 6
        
        y = (self.display.height- label_height) // 6
        self._value1 = self.add_value_label(0, label_height + y, '999')       
        self._value1_label = self.add_label(0, self._value1.y + self._value1.height + 10, 'prop')

        self._value2 = self.add_value_label(0, label_height + y * 3, '999')
        self._value2_label = self.add_label(0, self._value2.y + self._value2.height + 10, 'prop')
        
        self._value3 = self.add_value_label(0, label_height + y * 5, '999')
        self._value3_label = self.add_label(0, self._value3.y + self._value3.height + 10, 'prop')
        
        self.battery_group = displayio.Group()
        self.main_group.append(self.battery_group)
        self.battery_icon = self.icon("low-battery.bmp", 260, 100)

    @property
    def location(self):
        return self._location.text
    @location.setter
    def location(self, value):
        self._location.text = value

    @property
    def value1(self):
        return self._value1.text
    @value1.setter
    def value1(self, value):
        self._value1.text = f"{value}"

    @property
    def value1_label(self):
        return self._value1_label.text
    @value1_label.setter
    def value1_label(self, value):
        self._value1_label.text = value

    @property
    def value2(self):
        return self._value2.text
    @value2.setter
    def value2(self, value):
        self._value2.text = f"{value}"

    @property
    def value2_label(self):
        return self._value2_label.text
    @value2_label.setter
    def value2_label(self, value):
        self._value2_label.text = value

    @property
    def value3(self):
        return self._value3.text
    @value3.setter
    def value3(self, value):
        self._value3.text = f"{value}"

    @property
    def value3_label(self):
        return self._value3_label.text
    @value3_label.setter
    def value3_label(self, value):
        self._value3_label.text = value

    @property
    def charge_needed(self):
        return self._charge_needed
    @charge_needed.setter
    def charge_needed(self, value):
        self._charge_needed = value
        
    def refresh(self):
        if self.battery_icon in self.battery_group:
            self.battery_group.pop()
        if self.charge_needed:
            self.battery_group.append(self.battery_icon)

        self.display.root_group = self.main_group
        self.display.refresh()
        time.sleep(self.display.time_to_refresh)

    def add_icon(self, path, x, y):
        tile_grid = self.icon(path, x, y)
        self.main_group.append(tile_grid)
        return tile_grid
        
    def icon(self, path, x, y):
        bitmap = displayio.OnDiskBitmap(f"/images/{path}")
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
        tile_grid.x = x
        tile_grid.y = y
        return tile_grid

    def add_value_label(self, x, y, value=''):
        value_label = label.Label(
            self.value_font,
            scale=2,
            text=value,
            color=0x000000,
            background_color=0xFFFFFF,
            padding_top=3,
            padding_bottom=3,
            padding_right=4,
            padding_left=4,
        )
        value_label.anchor_point = (0.5, 0.5)
        value_label.anchored_position = (self.display.width // 2, y)
        self.main_group.append(value_label)
        return value_label


    def add_label(self, x, y, value=''):
        new_label = label.Label(
            terminalio.FONT,
            scale=1,
            text=value,
            color=0x000000,
            background_color=0xFFFFFF,
            padding_top=1,
            padding_bottom=3,
            padding_right=4,
            padding_left=4
        )
        new_label.anchor_point = (0.5, 0)
        new_label.anchored_position = (self.display.width // 2, y)
        self.main_group.append(new_label)
        return new_label
