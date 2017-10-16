from gui.resources import *


class Header(ttk.Frame):
    """Template for creating a title and subtitle on each page"""

    def __init__(self, parent, controller, title_txt, subtitle_txt):
        """
        Initialises a frame with a title and subtitle.
        Frame is gridded to the top of the parent frame.
        """

        ttk.Frame.__init__(self, parent, style='bg.TFrame')
        self.controller = controller

        # position at top of page
        self.grid(column=0, row=0, sticky=(W, E))

        self.title_txt = StringVar(value=title_txt)
        self.title = ttk.Label(self, textvariable=self.title_txt, style='title.TLabel').grid(column=0, row=0, sticky=W)
        if len(subtitle_txt) > 0:
            subtitle = ttk.Label(self, text=subtitle_txt, style='heading.TLabel').grid(column=0, row=1, sticky=W)


    def set_title(self, txt):
        """Sets the page's title to txt"""

        self.title_txt.set(txt)
