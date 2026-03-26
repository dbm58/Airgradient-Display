import displayio
import terminalio

from adafruit_display_text import label
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.rect import Rect

class Layout():
    def __init__(self):
        self.widgets = {}
        self.renderer = {
            'field':   self._field,
            'heading': self._heading,
            'label':   self._label,
            'rect':    self._rect,
            'spacer':  self._spacer,
        }
        self.defaults ={}
        self.group = displayio.Group()

    def render(self, ui_data, screen_width=240):
        self.group = displayio.Group()
        
        self.defaults = {
            'background': ui_data.get("background", "0xFFFFFF"),
            'color':      ui_data.get("color",      "0x000000"),
            'margin':     ui_data.get("margin",      0),
            'padding':    ui_data.get("padding",     0),
            'width':      ui_data.get('width',       screen_width),
        }
        
        # Start at the top padding
        current_y = self.defaults['padding']
        x_pos = self.defaults['padding']
    
        for item in ui_data["elements"]:
            obj = None
    
            widget_type = item.get('type', 'unknown')
            print(widget_type)
            
            if not widget_type in self.renderer:
                continue

            obj, height = self.renderer[widget_type](item, x_pos, current_y)
    
            #  renderers should only return height
            #  renderers should store items in widgets, so that they can store
            #  multiples items if need be.
            #
            #  and, possibly, not return height.  just update current_y?
            if obj:
                if "id" in item:
                    self.widgets[item["id"]] = obj
                
                # THE MAGIC: Push the next element down
                current_y += height + item.get("margin_bottom", 0)
                print('new current_y: ', current_y)
                
        #  don't return these.  they should be available as properties
        return self.group, self.widgets

    def _spacer(self, item, x_pos, current_y):
        obj = self  #  just a dummy value
        height = item.get('height', 0)
        return obj, height

    def _heading(self, item, x_pos, current_y):
        w_color=int(item.get("color", self.defaults['color']), 16)
        w_width = item.get('width', self.defaults['width'])
        w_padding = item.get('padding', 0)
        w_height = 0
    
        tmp = Rect( x_pos, current_y, w_width, 1, fill=w_color )
        self.group.append(tmp)
        w_height += 1 + w_padding
    
        obj = label.Label(
            terminalio.FONT, 
            text=item["text"], 
            color=w_color,
            x=x_pos, y=(current_y + 5 + w_height) # Offset for font height
        )
        self.group.append(obj)
        w_height += 10 + w_padding
    
        tmp = Rect( x_pos, current_y + w_height, w_width, 1, fill=w_color )
        self.group.append(tmp)
        height = w_height + 1

        return obj, height

    def _field(self, item, x_pos, current_y):
        w_color=int(item.get("color", self.defaults['color']), 16)

        obj = label.Label(
            terminalio.FONT, 
            text=item["label"], 
            color=w_color,
            x=x_pos, y=(current_y + 5 + 5) # Offset for font height
        )
        self.group.append(obj)
        obj = label.Label(
            terminalio.FONT, 
            text=item["value"], 
            color=w_color,
            x=x_pos, y=(current_y + 5 + 10 + 5) # Offset for font height
        )
        self.group.append(obj)
        height = 30 

        return obj, height

    def _label(self, item, x_pos, current_y):
        # Labels in CircuitPython anchor at the center or baseline 
        # so we adjust y to represent the top-left for consistency
        w_color=int(item.get("color", self.defaults['color']), 16)
        obj = label.Label(
            terminalio.FONT, 
            text=item["text"], 
            color=w_color,
            x=x_pos, y=current_y + 5 # Offset for font height
        )
        self.group.append(obj)
        # Estimate height based on font (terminalio is ~10px)
        height = 10 
        return obj, height

    def _rect(self, item, x_pos, current_y):
        obj = Rect(
            x_pos, current_y, 
            item["width"], item["height"], 
            fill=int(item["fill"], 16)
        )
        self.group.append(obj)
        height = item["height"]
        return obj, height
