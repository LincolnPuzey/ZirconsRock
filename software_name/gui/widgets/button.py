from gui.resources import *


class Button(ttk.Button):
    """
    Extends ttk.Button so arrow keys can be used to traverse
    between buttons
    """

    def __init__(self, *args, **kwargs):
        ttk.Button.__init__(self, *args, **kwargs)
        self.bind("<Return>", self.on_press)
        self.bind("<Left>", self.traverse)
        self.bind("<Right>", self.traverse)


    def on_press(self, *event):
        """Enables an event (e.g. key press) to invoke the button"""

        self.invoke()


    def traverse(self, event):
        """
        Traverses buttons in the direction of the pressed arrow key.
        """

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
