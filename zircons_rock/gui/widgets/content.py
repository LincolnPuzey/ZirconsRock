from gui.resources import *


class Content(ttk.Frame):
    """
    Template for creating a blank frame.
    A page's content should be added to this fame.
    """

    def __init__(self, parent, controller):
        """
        Initialises a blank frame.
        Frame is gridded to row 1 of the parent frame.
        """

        ttk.Frame.__init__(self, parent, style="bg.TFrame", padding="0 25 0 25")
        self.controller = controller

        # position below the Header
        self.grid(column=0, row=1, sticky=(N,S,E,W))
