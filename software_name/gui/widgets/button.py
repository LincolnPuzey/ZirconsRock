from gui.resources import *


class Button(ttk.Button):

    def __init__(self, *args, **kwargs):
        ttk.Button.__init__(self, *args, **kwargs)
        self.bind("<Return>", self.on_press)
        self.bind("<Left>", self.traverse)
        self.bind("<Right>", self.traverse)

    def on_press(self, *event):
        self.invoke()

    def traverse(self, event):
        widget = event.widget
        if event.keysym == "Left":
            # find the previous widget
            tcl_obj = self.tk.call('tk_focusPrev', widget._w)
            prev_widget = self.nametowidget(tcl_obj.string)
            if isinstance(prev_widget, ttk.Button):
                prev_widget.focus()

        if event.keysym == "Right":
            # find the next widget
            tcl_obj = self.tk.call('tk_focusNext', widget._w)
            next_widget = self.nametowidget(tcl_obj.string)
            if isinstance(next_widget, ttk.Button):
                next_widget.focus()
