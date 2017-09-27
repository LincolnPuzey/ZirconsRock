from gui.resources import *


class Button(ttk.Button):

    def __init__(self, *args, **kwargs):
        ttk.Button.__init__(self, *args, **kwargs)
        self.bind("<Return>", self.onPress)
        self.bind("<Left>", self.traverse)
        self.bind("<Right>", self.traverse)

    def onPress(self, *event):
        self.invoke()

    def traverse(self, event):
        widget = event.widget
        if event.keysym == "Left":
            #find the previous widget
            tcl_obj = self.tk.call('tk_focusPrev', widget._w)
            prevWidget = self.nametowidget(tcl_obj.string)
            if isinstance(prevWidget, ttk.Button):
                prevWidget.focus()

        if event.keysym == "Right":
            #find the next widget
            tcl_obj = self.tk.call('tk_focusNext', widget._w)
            nextWidget = self.nametowidget(tcl_obj.string)
            if isinstance(nextWidget, ttk.Button):
                nextWidget.focus()
