import time
import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font


class Base:
    display = None
    main_group = None
    rotation = 0

    label_font = None
    location_font = None
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
        self.label_font = terminalio.FONT
        self.location_font = terminalio.FONT

        self.display = board.DISPLAY
        self.display.rotation = self.rotation
        self.main_group = displayio.Group()

        self._location = self.add_basic_label()
        self._location.font = self.location_font
        
        self._value1 = self.add_basic_label()
        self._value1.font = self.value_font
        self._value1_label = self.add_basic_label()
        self._value1_label.font = self.label_font
        
        self._value2 = self.add_basic_label()
        self._value2.font = self.value_font
        self._value2_label = self.add_basic_label()
        self._value2_label.font = self.label_font
        
        self._value3 = self.add_basic_label()
        self._value3.font = self.value_font
        self._value3_label = self.add_basic_label()
        self._value3_label.font = self.label_font
        
        self.setup_display()

    def setup_display(self):
        Pass

    def set_background(self):
        bg_bitmap = displayio.Bitmap(self.display.width, self.display.height, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = 0xFFFFFF
        bg_sprite = displayio.TileGrid(bg_bitmap, x=0, y=0, pixel_shader=bg_palette)
        bg_group = displayio.Group()
        bg_group.append(bg_sprite)
        self.main_group.append(bg_group)

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
        if self._value2 != None:
            return self._value2.text
        return None
    @value2.setter
    def value2(self, value):
        if self._value2 != None:
            self._value2.text = f"{value}"

    @property
    def value2_label(self):
        if self._value2_label != None:
            return self._value2_label.text
        return None
    @value2_label.setter
    def value2_label(self, value):
        if self._value2_label != None:
            self._value2_label.text = value

    @property
    def value3(self):
        if self._value3 != None:
            return self._value3.text
        return None
    @value3.setter
    def value3(self, value):
        if self._value3 != None:
            self._value3.text = f"{value}"

    @property
    def value3_label(self):
        if self._value3_label != None:
            return self._value3_label.text
        return None
    @value3_label.setter
    def value3_label(self, value):
        if self._value3_label != None:
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

        self.display.rotation = self.rotation
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

    def add_basic_label(self):
        basic_label = label.Label(
            self.label_font,
            scale=1,
            text="",
            color=0x000000,
            background_color=0xFFFFFF,
            padding_top=3,
            padding_bottom=3,
            padding_right=4,
            padding_left=4,
        )
        #self.main_group.append(basic_label)
        return basic_label

    def add_value(self, x, y, value=''):
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

    def add_label(self, x, y, value='', font=None):
        
        new_label = label.Label(
            font or self.label_font,
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
