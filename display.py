
import time
import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font


class Display:
    display = None
    main_group = None
    co2_label = None
    datum_label = None
    floor_label = None
    rate_label = None
    _charge_needed = False

    def __init__(self):
        #font_path = "/fonts/LeagueSpartan_Bold_16.bdf"
        #font1 = bitmap_font.load_font(font_path, displayio.Bitmap)
        #font_path = "/fonts/Junction_regular_24.bdf"
        #font = bitmap_font.load_font(font_path, displayio.Bitmap)
        font_path = "/fonts/LibreBodoniv2002-Bold-27.bdf"
        font = bitmap_font.load_font(font_path, displayio.Bitmap)
        #font = terminalio.FONT

        self.display = board.DISPLAY
        #time.sleep(self.display.time_to_refresh)
        self.main_group = displayio.Group()

        # white background. Scaled to save RAM
        bg_bitmap = displayio.Bitmap(self.display.width // 8, self.display.height // 8, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = 0xFFFFFF
        bg_sprite = displayio.TileGrid(bg_bitmap, x=0, y=0, pixel_shader=bg_palette)
        bg_group = displayio.Group(scale=8)
        bg_group.append(bg_sprite)
        self.main_group.append(bg_group)

        self.floor_label = label.Label(
            font,
            scale=1, # 2
            text="XXXXXXXXX",
            color=0x000000,
            background_color=0xFFFFFF,
            padding_top=1,
            padding_bottom=3,
            padding_right=4,
            padding_left=4,
        )
        self.floor_label.anchor_point = (0.5, 0.5)
        self.floor_label.anchored_position = (self.display.width // 2, 10)
        self.main_group.append(self.floor_label)

        self.co2_label = label.Label(
            font,
            scale=3,  # 6
            text=f"XXX",
            color=0x000000,
            background_color=0xFFFFFF,
            padding_top=1,
            padding_bottom=3,
            padding_right=4,
            padding_left=4,
        )
        self.co2_label.anchor_point = (0.5, 0.5)
        self.co2_label.anchored_position = (self.display.width // 2, self.display.height // 2)
        self.main_group.append(self.co2_label)

        self.datum_label = self.add_label(15, 105)
        self.datum_label.text = 'CO2'

        self.rate_label = self.add_label(80, 105)
        self.rate_label.text = '1 min'

        #self.add_icon("tune.bmp",     15, 100)
        self.add_icon("refresh.bmp", 156, 100)
        self.add_icon("floor.bmp",   230, 100)

        self.battery_group = displayio.Group()
        self.main_group.append(self.battery_group)
        self.battery_icon = self.icon("low-battery.bmp", 260, 100)

    @property
    def floor(self):
        return self.floor_label.text
    @floor.setter
    def floor(self, value):
        self.floor_label.text = value

    @property
    def co2(self):
        return self.co2_label.text
    @co2.setter
    def co2(self, value):
        self.co2_label.text = f"{value}"

    @property
    def charge_needed(self):
        return self._charge_needed
    @charge_needed.setter
    def charge_needed(self, value):
        self._charge_needed = value

    @property
    def datum_text(self):
        return self.datum_label.text
    @datum_text.setter
    def datum_text(self, value):
        self.datum_label.text = value
        
    @property
    def rate_text(self):
        return self.rate_label.text
    @rate_text.setter
    def rate_text(self, value):
        self.rate_label.text = value
        
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

    def add_label(self, x, y):
        new_label = label.Label(
            terminalio.FONT,
            scale=1,
            text="",
            color=0x000000,
            background_color=0xFFFFFF,
            padding_top=1,
            padding_bottom=3,
            padding_right=4,
            padding_left=4
        )
        new_label.anchor_point = (0, 0)
        new_label.anchored_position = (x, y)
        self.main_group.append(new_label)
        return new_label
