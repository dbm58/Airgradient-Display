import board
import time
import sys

from ui_base import UiBase
from data import info
from layout import load_auto_ui

ui = UiBase(board.DISPLAY)
ui.display.rotation = 0
ui.set_background()

group, widgets = load_auto_ui(info)
ui.display.root_group.append(group)
widgets['board'].text = sys.implementation._machine
widgets['version'].text = ".".join(map(str,  filter(None, sys.implementation.version)))
ui.refresh()

while True:
    pass


