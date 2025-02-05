import board
import keypad

class Keys:
    def __init__(self):
        button_pins = (board.BUTTON_A, board.BUTTON_B,
                       board.BUTTON_C, board.BUTTON_D)
        buttons = keypad.Keys(button_pins, value_when_pressed=False, pull=True)

