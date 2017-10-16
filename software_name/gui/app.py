# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# http://www.tkdocs.com/tutorial/widgets.html
# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html
# https://stackoverflow.com/questions/16840660/scroll-a-group-of-widgets-in-tkinter

# padding=(left top right bottom)

from gui.resources import *

from defaults import MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT
from defaults import INITIAL_WINDOW_WIDTH, INITIAL_WINDOW_HEIGHT

class App(tk.Tk):
    """
    Creates and maintains all GUI pages.
    All pages are stored as Frames within the container variable.
    Each page can access this object through their 'controller' attribute

    Example: A page can call self.controller.show_frame('PageName') to change page
    """

    def __init__(self, *args, **kwargs):
        # initialising the base ttk class
        tk.Tk.__init__(self, *args, **kwargs)

        styles.initialise_syles()

        self.title("CITS3200 Prototype")

        # set initial window size
        self.geometry(str(INITIAL_WINDOW_WIDTH) + "x" + str(INITIAL_WINDOW_HEIGHT))
        # set minimum window size
        self.minsize(width=MIN_WINDOW_WIDTH,height=MIN_WINDOW_HEIGHT)

        menubar = tk.Menu(self)
        menubar.add_command(label="Clear cache", command=self.clear_cache())

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = ttk.Frame(self, padding="20 20 20 20")
        container.grid(column=0, row=0, sticky=(N,S,E,W))

        # enable window resizing
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        # determines UPb or TE processing was selected
        self.isUpb = True

        self.frames = {}
        self.initialse_frames(container)
        self.show_frame("StartPage")

    def initialse_frames(self, container):
        """Initialises each page and stores them within the container."""
        # StartPage
        frame = StartPage(parent=container, controller=self)
        self.frames["StartPage"] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        # InputOutputPage for UPb
        frame = InputOutputPage(parent=container, controller=self, title="UPb")
        self.frames["UPbInputOutputPage"] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        # InputOutputPage for TE
        frame = InputOutputPage(parent=container, controller=self, title="TE")
        self.frames["TEInputOutputPage"] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        # FilterStandardsPage for UPb
        frame = FilterStandardsPage(parent=container, controller=self, title="UPb")
        self.frames["UPbFilterStandardsPage"] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        # FilterStandardsPage for TE
        frame = FilterStandardsPage(parent=container, controller=self, title="TE")
        self.frames["TEFilterStandardsPage"] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        # FinishedPage
        frame = FinishedPage(parent=container, controller=self)
        self.frames["FinishedPage"] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        """Displays the page called page_name"""

        frame = self.frames[page_name]
        frame.tkraise()

    # returns either 'U-Pb' or 'TE'
    def getProcessName(self):
        """
        Returns 'UPb' if UPb was selected at the StartPage
        Returns 'TE' if TE was selected at the StartPage
        """

        if self.isUpb:
            return 'UPb'
        return 'TE'

    def clear_cache(self):
        """Deletes all files in the /gui/temps/ directory"""
        print("clear cache")
