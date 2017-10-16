from gui.resources import *


class CustomRadiobutton(ttk.Checkbutton):
    """
    Extends ttk.Checkbutton so arrow keys can be used to traverse
    between radiobuttons and checkbuttons
    """

    def __init__(self, *args, **kwargs):

        self.num_columns = kwargs.pop('num_columns')

        ttk.Radiobutton.__init__(self, *args, **kwargs)

        self.bind("<Up>", self.traverse)
        self.bind("<Down>", self.traverse)
        self.bind("<Left>", self.traverse)
        self.bind("<Right>", self.traverse)

        self.bind("<Return>", self.toggle)


    def toggle(self, event):
        """Toggles the radiobutton's state"""
        event.widget.invoke()


    # https://stackoverflow.com/questions/6687108/how-to-set-the-tab-order-in-a-tkinter-application
    def traverse(self, event):
        """
        Traverses radiobuttons in the direction of the pressed arrow key.

        num_columns determines how many radiobuttons must be traversed left/right
        to find the above/below radiobutton
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
