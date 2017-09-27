from gui.resources import *


class CustomCheckbutton(ttk.Checkbutton):

    def __init__(self, *args, **kwargs):
        ttk.Checkbutton.__init__(self, *args, **kwargs)

        self.bind("<Up>", self.traverse)
        self.bind("<Down>", self.traverse)
        self.bind("<Left>", self.traverse)
        self.bind("<Right>", self.traverse)

        self.bind("<Return>", self.toggle)

    def toggle(self, event):
        event.widget.invoke()

    # https://stackoverflow.com/questions/6687108/how-to-set-the-tab-order-in-a-tkinter-application
    def traverse(self, event):
        widget = event.widget
        if event.keysym == "Left":
            # find the previous widget
            tcl_obj = self.tk.call('tk_focusPrev', widget._w)
            prev_widget = self.nametowidget(tcl_obj.string)
            if isinstance(prev_widget, ttk.Checkbutton):
                prev_widget.focus()

        if event.keysym == "Right":
            # find the next widget
            tcl_obj = self.tk.call('tk_focusNext', widget._w)
            next_widget = self.nametowidget(tcl_obj.string)
            if isinstance(next_widget, ttk.Checkbutton):
                next_widget.focus()

        if event.keysym == "Up":
            # find the previous widget
            tcl_obj = self.tk.call('tk_focusPrev', widget._w)
            prev_widget = self.nametowidget(tcl_obj.string)
            # find the previous, previous widget
            tcl_obj = self.tk.call('tk_focusPrev', prev_widget._w)
            prev_widget = self.nametowidget(tcl_obj.string)
            if isinstance(prev_widget, ttk.Checkbutton):
                prev_widget.focus()

        if event.keysym == "Down":
            # find the next widget
            tcl_obj = self.tk.call('tk_focusNext', widget._w)
            next_widget = self.nametowidget(tcl_obj.string)
            # find the next, next widget
            tcl_obj = self.tk.call('tk_focusNext', next_widget._w)
            next_widget = self.nametowidget(tcl_obj.string)
            if isinstance(next_widget, ttk.Checkbutton):
                next_widget.focus()
