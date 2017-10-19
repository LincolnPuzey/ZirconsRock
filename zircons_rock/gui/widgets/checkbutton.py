from gui.resources import *


class CustomCheckbutton(ttk.Checkbutton):
    """
    Extends ttk.Checkbutton so arrow keys can be used to traverse
    between checkbuttons and radiobuttons.

    Also makes the checbutton's 'onvalue' attribute accessible after __init__
    """

    def __init__(self, *args, **kwargs):

        self.onvalue = kwargs.get('onvalue')
        self.variable = kwargs.get('variable')
        self.num_columns = kwargs.pop('num_columns')

        ttk.Checkbutton.__init__(self, *args, **kwargs)

        self.bind("<Up>", self.traverse)
        self.bind("<Down>", self.traverse)
        self.bind("<Left>", self.traverse)
        self.bind("<Right>", self.traverse)

        self.bind("<Return>", self.toggle)

    def toggle(self, event):
        """Toggles the checkbutton's state"""

        event.widget.invoke()


    def select(self):
        """Selects the checkbutton"""

        self.variable.set(self.onvalue)


    def deselect(self):
        """Deselects the checkbutton"""

        self.variable.set("")


    # https://stackoverflow.com/questions/6687108/how-to-set-the-tab-order-in-a-tkinter-application
    def traverse(self, event):
        """
        Traverses checkbuttons in the direction of the pressed arrow key.

        num_columns determines how many checkbuttons must be traversed left/right
        to find the above/below checkbutton
        """

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
            # find the above widget
            for i in range(0, self.num_columns):
                tcl_obj = self.tk.call('tk_focusPrev', widget._w)
                widget = self.nametowidget(tcl_obj.string)
            if isinstance(widget, ttk.Checkbutton):
                widget.focus()

        if event.keysym == "Down":
            # find the below widget
            for i in range(0, self.num_columns):
                tcl_obj = self.tk.call('tk_focusNext', widget._w)
                widget = self.nametowidget(tcl_obj.string)
            if isinstance(widget, ttk.Checkbutton):
                widget.focus()
