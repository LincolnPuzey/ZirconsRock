from gui.resources import *


class Content(ttk.Frame):

     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="bg.TFrame", padding="0 25 0 25")
        self.controller = controller

        #position below the Header
        self.grid(column=0, row=1, sticky=(W,E))
