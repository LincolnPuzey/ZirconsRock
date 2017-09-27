from gui.resources import *

class Header(ttk.Frame):

    def __init__(self, parent, controller, title_txt, subtitle_txt):
        ttk.Frame.__init__(self, parent, style='bg.TFrame')
        self.controller = controller

        #position at top of page
        self.grid(column=0, row=0, sticky=(W,E))

        self.title_txt = StringVar(value=title_txt)
        self.title = ttk.Label(self, textvariable=self.title_txt, style='title.TLabel').grid(column=0, row=0, sticky=(W))
        if len(subtitle_txt) > 0:
            subtitle = ttk.Label(self, text=subtitle_txt, style='subtitle.TLabel').grid(column=0, row=1, sticky=(W))

    def setTitle(self, txt):
        self.title_txt.set(txt)
