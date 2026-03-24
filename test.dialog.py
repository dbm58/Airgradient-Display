import board
import time

from ui_menu import Menu
from ui_base import UiBase
from ui_dialog import Dialogs

ui = UiBase(board.DISPLAY)
ui.display.rotation = 0
ui.set_background()

dialogs = [
    Dialogs.WIFI_OFF,
    Dialogs.HOURGLASS,
    Dialogs.BATTERY_ALERT
    ]
index = 0
for dialog in dialogs:
    dialog.hidden = True
    ui.display.root_group.append(dialog)
dialogs[index].hidden = False
ui.refresh()

while True:
    time.sleep(ui.display.time_to_refresh + 1)
    dialogs[index].hidden = True
    index = (index + 1) % len(dialogs)
    dialogs[index].hidden = False
    ui.refresh()

