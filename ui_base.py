import displayio
import terminalio
import time

from colors import *

class UiBase:
    def __init__(self, display):
        self.display = display
        self.display.root_group = displayio.Group()

    def set_background(self):
        bg_bitmap = displayio.Bitmap(self.display.width, self.display.height, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = WHITE
        bg_sprite = displayio.TileGrid(bg_bitmap, x=0, y=0, pixel_shader=bg_palette)
        bg_group = displayio.Group()
        bg_group.append(bg_sprite)
        self.display.root_group.append(bg_group)

    def refresh(self):
        time.sleep(self.display.time_to_refresh + 0.1)
        self.display.refresh()

    def add_icon(self, path, x, y):
        tile_grid = self.icon(path, x, y)
        self.display.root_group.append(tile_grid)
        return tile_grid
        
    def icon(self, path, x, y):
        bitmap = displayio.OnDiskBitmap(f"/images/{path}")
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
        tile_grid.x = x
        tile_grid.y = y
        return tile_grid
