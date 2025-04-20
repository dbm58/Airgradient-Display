import alarm
import board
from digitalio import DigitalInOut, Direction, Pull
import time

CHANGE_ORIENTATION = 1
CHANGE_REFRESH = 2
REFRESH_DISPLAY = 3
CHANGE_LOCATION = 4
DISPLAY_DATA = 5
PROGRAM_DONE = 99

class MessagePump:
    def __init__(self):
        self.pin_alarm_a = alarm.pin.PinAlarm(pin=board.BUTTON_A, value=False, pull=True)
        self.pin_alarm_b = alarm.pin.PinAlarm(pin=board.BUTTON_B, value=False, pull=True)
        self.pin_alarm_c = alarm.pin.PinAlarm(pin=board.BUTTON_C, value=False, pull=True)
        self.pin_alarm_d = alarm.pin.PinAlarm(pin=board.BUTTON_D, value=False, pull=True)
        self.buttons = (self.pin_alarm_a, self.pin_alarm_b, self.pin_alarm_c, self.pin_alarm_d)
        self.refresh_rate = 1 # 1 minute

    @property
    def time_alarm(self):
        return alarm.time.TimeAlarm(monotonic_time=time.monotonic() + (60 * self.refresh_rate))
        
    def __iter__(self):
        yield (DISPLAY_DATA, None)
        triggered_alarm = None
        while True:
            if isinstance(triggered_alarm, alarm.pin.PinAlarm):
                if triggered_alarm == self.pin_alarm_a:
                    switch = DigitalInOut(board.BUTTON_A)
                    switch.direction = Direction.INPUT
                    switch.pull = Pull.UP
                    print('switch value', switch.value)
                    yield (CHANGE_ORIENTATION, None)
                    while not switch.value:
                        pass
                elif triggered_alarm == self.pin_alarm_b:
                    yield (CHANGE_REFRESH, None)
                elif triggered_alarm == self.pin_alarm_c:
                    yield (DISPLAY_DATA, None)
                elif triggered_alarm == self.pin_alarm_d:
                    yield (CHANGE_LOCATION, None)
            elif isinstance(triggered_alarm, alarm.time.TimeAlarm):
                yield (DISPLAY_DATA, None)
            triggered_alarm = alarm.light_sleep_until_alarms(*(self.buttons), self.time_alarm)
        
                