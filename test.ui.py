import board
from ui import Ui

ui = Ui(board.DISPLAY)
ui.heading = 'Location'
ui.define_fields(['v1', 'v2', 'v3'])
ui['v1'] = 99
ui['v2'] = 88
ui['v3'] = 77
ui.refresh()

while True:
    pass
