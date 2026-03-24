import board
import time

from ui_base import UiBase
from data import ui2
from layout import load_auto_ui

ui = UiBase(board.DISPLAY)
ui.display.rotation = 0
ui.set_background()

group, widgets = load_auto_ui(ui2)
ui.display.root_group.append(group)
widgets['temp_read'].text = '33C'
ui.refresh()

while True:
    pass

