import board
import time
import sys

from ui_base import UiBase
from data import info
from layout import Layout
from battery import Battery

ui = UiBase(board.DISPLAY)
ui.display.rotation = 0
ui.set_background()

layout = Layout()
group, widgets = layout.render(info)
ui.display.root_group.append(group)
widgets['board'].text = sys.implementation._machine
widgets['version'].text = ".".join(map(str,  filter(None, sys.implementation.version)))

bat = Battery()
alarm = ' !!!' if bat.charge_needed else ''
widgets['voltage'].text = str(bat.voltage) + alarm
widgets['ext-power'].text = str(bat.on_external_power)

ui.refresh()

while True:
    pass


