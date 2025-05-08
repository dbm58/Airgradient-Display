import board
from menu import Menu

menu = Menu(20, 32, board.DISPLAY.width - 20, board.DISPLAY.height - 32 - 10)
menu.items = ['Refresh', 'Location', '', 'Close']
board.DISPLAY.root_group = menu
board.DISPLAY.refresh()

while True:
    pass
