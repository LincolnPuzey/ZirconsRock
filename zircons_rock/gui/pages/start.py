from gui.resources import *
from defaults import UPB_IMAGE, TE_IMAGE
import data_processing.UPb as UPb
import data_processing.TE as TE
import data_processing.common as common

class StartPage(ttk.Frame):
    """
    Page for selecting between UPb or TE processing.

    This is the first page the user sees.
    """

    def __init__(self, parent, controller):
        """
        Initialises buttons and grids them to the page.
        Enables window scaling through columnconfigure and rowconfigure.
        """

        # initialising the base Frame class
        ttk.Frame.__init__(self, parent, style='bg.TFrame')
        self.parent = parent
        self.controller = controller

        # distinguishes between the frame's header and the frame's content
        header_frame = Header(self, controller, "1. Select a process", "")
        content_frame = Content(self, controller)

        # can use GIF, PPM/PGP - http://effbot.org/tkinterbook/photoimage.html
        uranium_img = PhotoImage(file=UPB_IMAGE)
        trace_img = PhotoImage(file=TE_IMAGE)

        button_frame = ttk.Frame(content_frame, padding="0 20 0 20");

        # define buttons
        uranium_button = Button(button_frame, text="\nU-Pb Dating", image=uranium_img, compound="top",
                               style="image.TButton", command=self.onPressUpb, padding="5 20 5 20")
        trace_button = Button(button_frame, text="\nTrace Element", image=trace_img, compound="top",
                             style="image.TButton", command=self.onPressTE, padding="5 20 5 20")

        # temporary test buttons
        # test_upb_button = Button(content_frame, text="Test UPb", command=self.test_upb)
        # test_te_button = Button(content_frame, text="Test TE", command=self.test_te)

        # need to maintain references to images like this
        # http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        uranium_button.image = uranium_img
        trace_button.image = trace_img

        or_label = ttk.Label(button_frame, text="or", padding="5 0 5 0")

        # content_frame children
        button_frame.grid(column=0, row=0)

        uranium_button.grid(column=0, row=0)
        or_label.grid(column=1, row=0)
        trace_button.grid(column=2, row=0)

        # test_upb_button.grid(column=0, row=1)
        # test_te_button.grid(column=2, row=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)

        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)


    def onPressUpb(self):
        """Initialises UPbInputOutputPage and sets the controller to UPb processing"""

        self.controller.isUpb = True
        self.controller.frames["UPbInputOutputPage"].initialise()
        self.controller.show_frame("UPbInputOutputPage")


    def onPressTE(self):
        """Initialises TEInputOutputPage and sets the controller to TE processing"""

        self.controller.isUpb = False
        self.controller.frames["TEInputOutputPage"].initialise()
        self.controller.show_frame("TEInputOutputPage")
