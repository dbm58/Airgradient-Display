import displayio

from colors import *
        
class Icon(displayio.TileGrid):
    def __init__(self, path):
        bitmap = displayio.OnDiskBitmap(f"/images/{path}")

        palette = displayio.Palette(2)
        palette[0] = SILVER
        palette[1] = BLACK
        super().__init__(bitmap, pixel_shader=palette)
        self.bitmap = bitmap

    @property
    def width(self):
        return self.bitmap.width

    @property
    def height(self):
        return self.bitmap.height
