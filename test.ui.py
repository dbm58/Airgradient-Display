
from ui import Ui

ui = Ui()
ui.set_value(0, "99")
ui.set_value(1, "88")
ui.set_value(2, "77")
ui.set_caption(0, "v1")
ui.set_caption(1, "v2")
ui.set_caption(2, "v3")
ui.refresh()

while True:
    pass
