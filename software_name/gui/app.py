# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# http://www.tkdocs.com/tutorial/widgets.html
# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html
# https://stackoverflow.com/questions/16840660/scroll-a-group-of-widgets-in-tkinter

#padding=(left top right bottom)

from gui.resources import *

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        #initialising the base ttk class
        tk.Tk.__init__(self, *args, **kwargs)

        styles.initialise_syles()

        self.title("CITS3200 Prototype")

        #determines U-Pb or TE processing was selected
        self.isUpb = True

        self.bigFont = tkfont.Font(family='Helvetica', size=28)
        self.mediumFont = tkfont.Font(family='Helvetica', size=18)
        self.smallFont = tkfont.Font(family='Helvetica', size=14)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = ttk.Frame(self, padding="20 20 20 20")
        container.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


        # container.rowconfigure(0, weight=1)
        # container.rowconfigure(1, weight=1)
        # container.rowconfigure(2, weight=1)
        # container.columnconfigure(0, weight=1)
        # container.columnconfigure(1, weight=1)
        # container.columnconfigure(2, weight=1)

        self.frames = {}

        #InputOutputPage for UPb
        frame = InputOutputPage(parent=container, controller=self, title="UPb")
        self.frames["UPbInputOutputPage"] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        #InputOutputPage for TE
        frame = InputOutputPage(parent=container, controller=self, title="TE")
        self.frames["TEInputOutputPage"] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        for F in (StartPage, FilterStandardsPage,
                LoadingPage, FinishedPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''

        frame = self.frames[page_name]
        frame.tkraise()

    #returns either 'U-Pb' or 'TE'
    def getProcessName(self):
        if self.isUpb:
            return 'UPb'
        return 'TE'
