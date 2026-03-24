import displayio
import terminalio

from adafruit_display_text import label
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.rect import Rect

def load_auto_ui(ui_data, screen_width=240):
    group = displayio.Group()
    widgets = {}
    
    # Start at the top padding
    current_y = ui_data.get("padding", 0)
    x_pos = ui_data.get("padding", 0)

    for item in ui_data["elements"]:
        obj = None

        widget_type = item.get('type', 'unknown')
        print(widget_type)
        
        if widget_type == 'heading':
            w_color=int(item["color"], 16)
            tmp = Rect(
                x_pos, current_y, 
                item["width"], 1,
                fill=w_color
            )
            group.append(tmp)
            obj = label.Label(
                terminalio.FONT, 
                text=item["text"], 
                color=w_color,
                x=x_pos, y=(current_y + 2 + 5) # Offset for font height
            )
            group.append(obj)
            tmp = Rect(
                x_pos, current_y + 12, 
                item["width"], 1,
                fill=w_color
            )
            group.append(tmp)
            height = 14

        elif widget_type == 'field':
            print('field: ', item)
            w_color=int(item["color"], 16)
            obj = label.Label(
                terminalio.FONT, 
                text=item["label"], 
                color=w_color,
                x=x_pos, y=(current_y + 5) # Offset for font height
            )
            group.append(obj)
            w = obj.width
            obj = label.Label(
                terminalio.FONT, 
                text=item["value"], 
                color=w_color,
                x=x_pos + w, y=(current_y + 5) # Offset for font height
            )
            group.append(obj)
            height = 10 

        elif widget_type == "label":
            # Labels in CircuitPython anchor at the center or baseline 
            # so we adjust y to represent the top-left for consistency
            obj = label.Label(
                terminalio.FONT, 
                text=item["text"], 
                color=int(item["color"], 16),
                x=x_pos, y=current_y + 5 # Offset for font height
            )
            group.append(obj)
            # Estimate height based on font (terminalio is ~10px)
            height = 10 

        elif widget_type == "rect":
            obj = Rect(
                x_pos, current_y, 
                item["width"], item["height"], 
                fill=int(item["fill"], 16)
            )
            group.append(obj)
            height = item["height"]

        if obj:
            if "id" in item:
                widgets[item["id"]] = obj
            
            # THE MAGIC: Push the next element down
            current_y += height + item.get("margin_bottom", 0)
            
    return group, widgets
