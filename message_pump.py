import alarm
import board
from digitalio import DigitalInOut, Direction, Pull
import time

from buttons import Buttons

DISPLAY_DATA = 1
CHARGE_NEEDED = 2
BUTTON_DOWN = 10
BUTTON_UP = 11
BUTTON_DOWN_A = 12
BUTTON_DOWN_B = 13
BUTTON_DOWN_C = 14
BUTTON_DOWN_D = 15
BUTTON_UP_A = 16
BUTTON_UP_B = 17
BUTTON_UP_C = 18
BUTTON_UP_D = 19
PROGRAM_DONE = 99

class MessagePump:
    def __init__(self):
        self.buttons = Buttons()

        self.refresh_rate = 1 # 1 minute

    @property
    def time_alarm(self):
        next_update = time.monotonic() + (60 * self.refresh_rate)
        return alarm.time.TimeAlarm(monotonic_time=next_update)
        
    def __iter__(self):
        triggered_alarm = self.time_alarm
        while True:
            if isinstance(triggered_alarm, alarm.pin.PinAlarm):
                yield (BUTTON_DOWN, self.buttons.name(triggered_alarm))
                if triggered_alarm == self.buttons.pin_alarm_a:
                    yield (BUTTON_DOWN_A, None)
                    self.buttons.debounce(board.BUTTON_A)
                    yield (BUTTON_UP_A, None)
                elif triggered_alarm == self.buttons.pin_alarm_b:
                    yield (BUTTON_DOWN_B, None)
                    self.buttons.debounce(board.BUTTON_B)
                    yield (BUTTON_UP_B, None)
                elif triggered_alarm == self.buttons.pin_alarm_c:
                    yield (BUTTON_DOWN_C, None)
                    self.buttons.debounce(board.BUTTON_C)
                    yield (BUTTON_UP_C, None)
                elif triggered_alarm == self.buttons.pin_alarm_d:
                    yield (BUTTON_DOWN_D, None)
                    self.buttons.debounce(board.BUTTON_D)
                    yield (BUTTON_UP_D, None)
                yield (BUTTON_UP, self.buttons.name(triggered_alarm))
            elif isinstance(triggered_alarm, alarm.time.TimeAlarm):
                yield (DISPLAY_DATA, None)
            all_alarms = self.buttons.alarms + (self.time_alarm,)
            triggered_alarm = alarm.light_sleep_until_alarms(*(all_alarms))
