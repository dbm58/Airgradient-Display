import board
import displayio
import terminalio
import time
from adafruit_display_text import label

from adafruit_displayio_layout.layouts.grid_layout import GridLayout

from colors import *
from ui_base import UiBase

class Ui(UiBase):

    def __init__(self):
        super().__init__()
        self.display = board.DISPLAY
        self.display.rotation = 0
        main_group = displayio.Group()
        self.display.root_group = main_group
        self.set_background()

        label_attrs = {
            'font': terminalio.FONT,
            'background_color': WHITE,
            'color': BLACK }

        location = label.Label(
            text="Hello",
            scale=2,
            **label_attrs,
            anchor_point=(0.5,0),
            anchored_position=(self.display.width/2,0))

        self.labels = [
            label.Label( text="Hello", scale=3, **label_attrs ),
            label.Label( text="Hello", scale=3, **label_attrs ),
            label.Label( text="Hello", scale=3, **label_attrs ),
            ]

        layout = GridLayout(
            x=0,
            y=(location.height * location.scale),
            width=self.display.width,
            height=self.display.height - (location.height * location.scale),
            grid_size=(1, 3),
            cell_padding=8,
            divider_lines=True,  # divider lines around every cell
            divider_line_color=BLACK,
            cell_anchor_point=(0.5, 0.5)
        )
        layout.add_content(self.labels[0], (0, 0), (1,1))
        layout.add_content(self.labels[1], (0, 1), (1,1))
        layout.add_content(self.labels[2], (0, 2), (1,1))

        self.captions = [
            self.caption(layout, self.labels[0], 'caption'),
            self.caption(layout, self.labels[1], 'caption'),
            self.caption(layout, self.labels[2], 'caption')
            ]

        main_group.append(location)
        main_group.append(layout)
        self.display.refresh()

    def set_background(self):
        bg_bitmap = displayio.Bitmap(self.display.width, self.display.height, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = WHITE
        bg_sprite = displayio.TileGrid(bg_bitmap, x=0, y=0, pixel_shader=bg_palette)
        bg_group = displayio.Group()
        bg_group.append(bg_sprite)
        self.display.root_group.append(bg_group)

    def caption(self, layout, target, text):
        caption = label.Label(
            terminalio.FONT,
            scale=1,
            text=text,
            background_color=WHITE,
            color=BLACK,
            anchor_point=(0.5, 0),
            anchored_position=(self.display.width/2,
                target.y + ((target.height * target.scale)/2)))
        layout.append(caption)
        return caption

    def set_value(self, index, value):
        self.labels[index].text = value

    def set_caption(self, index, text):
        self.captions[index].text = text

    def refresh(self):
        time.sleep(self.display.time_to_refresh + 0.1)
        self.display.refresh()


#layout.add_content(lx, (0, 2), (1,1), cell_anchor_point=(0.5, 0.5))
#print(lx.x, lx.y)
#  todo:  so we can position an additional label below the celll
#  contents by getting the x,y of the label, then adding to the main
#  group instead of the grid layout
