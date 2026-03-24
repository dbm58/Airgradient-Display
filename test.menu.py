import board
from ui_menu import Menu
from ui_base import UiBase

ui = UiBase(board.DISPLAY)
ui.display.rotation = 0
ui.set_background()

menu = Menu(20, 32, ui.display.width - 20, ui.display.height - 32 - 10)
menu.items = ['Refresh', 'Location', '', 'Close']
menu.hidden = False
ui.display.root_group.append(menu)
ui.refresh()

while True:
    pass
