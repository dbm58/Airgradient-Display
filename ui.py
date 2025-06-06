import displayio
import terminalio

from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect

from colors import *
from devices import Devices
from ui_base import UiBase
from ui_dialog import Dialogs
from ui_menu import Menu

class Ui(UiBase):
    """
    Usage:
        ui = Ui(board.DISPLAY)
        ui.heading = 'Heading'
        ui.define_fields = ['CO2', 'TVOC', 'NOX']
        ui['CO2'] = 450
        ui['TVIOC'] = 100
        ui['NOX'] = 1
        ui.refresh()
    """
    _font_path = "/fonts/LibreBodoniv2002-Bold-27.bdf"
    value_font = bitmap_font.load_font(_font_path, displayio.Bitmap)
    label_font = terminalio.FONT
    location_font = terminalio.FONT
    cmn_attrs = {
        'background_color': WHITE,
        'color': BLACK,
        }
    caption_attrs = cmn_attrs | {
        'font': label_font,
        'scale': 1,
        }
    heading_attrs = cmn_attrs | {
        'font': label_font,
        'scale': 2,
        }
    value_attrs = cmn_attrs | {
        'font': value_font,
        'scale': 2,
        }

    def __init__(self, display):
        super().__init__(display)
        self.display.rotation = 0
        self.set_background()

        self.heading_label = label.Label(
            text="XXX",
            **self.heading_attrs,
            anchor_point=(0.5,0),
            anchored_position=(self.display.width/2,0))

        self.labels = [
            label.Label( text="99", **self.value_attrs ),
            label.Label( text="99", **self.value_attrs ),
            label.Label( text="99", **self.value_attrs ),
            ]

        layout = GridLayout(
            x=0,
            y=(self.heading_label.height * self.heading_label.scale),
            width=self.display.width,
            height=self.display.height -
                (self.heading_label.height * self.heading_label.scale),
            grid_size=(1, 3),
            cell_padding=8,
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

        [setattr(obj, 'text', "") for obj in self.labels]
        [setattr(obj, 'text', "") for obj in self.captions]
        self.heading_label.text = ""

        self.battery = self.add_icon(
            "low-battery.bmp",
            self.display.width - 24,
            self.display.height - 24)
        self.battery.hidden = True

        self.display.root_group.append(self.heading_label)
        self.display.root_group.append(layout)

        self.battery_alert_dialog = Dialogs.BATTERY_ALERT
        self.battery_alert_dialog.hidden = True
        self.display.root_group.append(self.battery_alert_dialog)

        self.hourglass_dialog = Dialogs.HOURGLASS
        self.hourglass_dialog.hidden = True
        self.display.root_group.append(self.hourglass_dialog)

        self.wifi_off_dialog = Dialogs.WIFI_OFF
        self.wifi_off_dialog.hidden = True
        self.display.root_group.append(self.wifi_off_dialog)

        menu = Menu(0, 32,
            self.display.width, self.display.height - 32 - 10)
        menu.items = ['Refresh', 'Location', '', 'Close']
        self.display.root_group.append(menu)
        self.menu = menu

        devices = Devices()
        locations = Menu(0, 32,
            self.display.width, self.display.height - 32 - 10)
        locations.items = [
            devices.devices[0]['descr'],
            devices.devices[1]['descr'],
            devices.devices[2]['descr'],
            ]
        self.display.root_group.append(locations)
        self.locations = locations

    def caption(self, layout, target, text):
        caption = label.Label(
            text=text,
            **self.caption_attrs,
            anchor_point=(0.5, 0),
            anchored_position=(self.display.width/2,
                target.y + ((target.height * target.scale)/2) + 6))
        layout.append(caption)
        return caption

    @property
    def heading(self):
        return self.heading_label.text
    @heading.setter
    def heading(self, value):
        self.heading_label.text = str(value)

    def define_fields(self, fields):
        for index, name in enumerate(fields):
            self.captions[index].text = name
        self.fields = fields

    def __setitem__(self, key, value):
        index = self.fields.index(key)
        self.labels[index].text = str(value)

