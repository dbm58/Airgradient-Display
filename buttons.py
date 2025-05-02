import alarm
import board
from digitalio import DigitalInOut, Direction, Pull
import time

class Buttons:
    def __init__(self):
        attrs = { 'value': False, 'pull': True }
        self.pin_alarm_a = alarm.pin.PinAlarm(pin=board.BUTTON_A, **attrs)
        self.pin_alarm_b = alarm.pin.PinAlarm(pin=board.BUTTON_B, **attrs)
        self.pin_alarm_c = alarm.pin.PinAlarm(pin=board.BUTTON_C, **attrs)
        self.pin_alarm_d = alarm.pin.PinAlarm(pin=board.BUTTON_D, **attrs)
        self.alarms = (
            self.pin_alarm_a,
            self.pin_alarm_b,
            self.pin_alarm_c,
            self.pin_alarm_d
            )

    def button(self, pin):
        switch = DigitalInOut(pin)
        switch.direction = Direction.INPUT
        switch.pull = Pull.UP
        return switch

    def debounce(self, pin):
        button = self.button(pin)
        time.sleep(0.1)
        while not button.value:
            time.sleep(0.1)

    def name(self, alarm):
        if alarm == self.pin_alarm_a:
            return 'A'
        elif alarm == self.pin_alarm_b:
            return 'B'
        elif alarm == self.pin_alarm_c:
            return 'C'
        elif alarm == self.pin_alarm_d:
            return 'D'
        return None
