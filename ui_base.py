import displayio
import terminalio
from adafruit_bitmap_font import bitmap_font

class UiBase:
    def __init__(self):
        font_path = "/fonts/LibreBodoniv2002-Bold-27.bdf"
        self.value_font = bitmap_font.load_font(font_path, displayio.Bitmap)
        self.label_font = terminalio.FONT
        self.location_font = terminalio.FONT
