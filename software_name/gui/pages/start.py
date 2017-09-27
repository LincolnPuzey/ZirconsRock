from gui.resources import *

import defaults as defaults
# from data_processing.UPb import *
import data_processing.UPb as UPb
import data_processing.TE as TE
import data_processing.common as common


class StartPage(ttk.Frame):

    def __init__(self, parent, controller):
        # initialising the base Frame class
        ttk.Frame.__init__(self, parent, style='bg.TFrame')
        self.parent = parent
        self.controller = controller

        # distinguishes between the frame's header and the frame's content
        headerFrame = Header(self, controller, "1. Select a process", "")
        contentFrame = Content(self, controller)
        footerFrame = Footer(self, controller, False, "",
                             "", "StartPage", "FilterStandardsPage")

        # can use GIF, PPM/PGP - http://effbot.org/tkinterbook/photoimage.html
        uraniumImg = PhotoImage(file='./gui/images/placeholder.gif')
        traceImg = PhotoImage(file='./gui/images/placeholder.gif')

        # define buttons
        uraniumButton = Button(contentFrame, text="\nUruanium Lead", image=uraniumImg, compound="top",
                               style="image.TButton", command=self.onPressUpb, padding="5 20 5 20")
        traceButton = Button(contentFrame, text="\nTrace Element", image=traceImg, compound="top",
                             style="image.TButton", command=self.onPressTE, padding="5 20 5 20")

        # temporary test buttons
        test_upb_button = Button(
            contentFrame, text="Test UPb", command=self.test_upb)
        test_te_button = Button(
            contentFrame, text="Test TE", command=self.test_te)

        # need to maintain references to images like this
        # http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        uraniumButton.image = uraniumImg
        traceButton.image = traceImg

        orLabel = ttk.Label(contentFrame, text="or",
                            font=controller.smallFont, padding="5 0 5 0")

        # draw widgets
        uraniumButton.grid(column=0, row=0)
        orLabel.grid(column=1, row=0)
        traceButton.grid(column=2, row=0)

        test_upb_button.grid(column=0, row=1)
        test_te_button.grid(column=2, row=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        contentFrame.columnconfigure(0, weight=1)
        contentFrame.columnconfigure(1, weight=1)
        contentFrame.columnconfigure(2, weight=1)
        contentFrame.rowconfigure(0, weight=1)

    def onPressUpb(self):
        self.controller.isUpb = True

        self.controller.frames["UPbInputOutputPage"].initialise()
        self.controller.frames["FilterStandardsPage"].initialiseUPb()
        self.controller.show_frame("UPbInputOutputPage")

    def onPressTE(self):
        self.controller.isUpb = False

        self.controller.frames["TEInputOutputPage"].initialise()
        self.controller.frames["FilterStandardsPage"].initialiseTE()
        self.controller.show_frame("TEInputOutputPage")

    def test_upb(self):
        UPb.UPb(defaults.CONTROL_STANDARDS, defaults.NORMALISING_STANDARDS,
                defaults.UPB_INPUT_FILEPATHS, defaults.UPB_OUTPUT_FILEPATH)
        self.controller.isUpb = True
        self.controller.frames["UPbInputOutputPage"].output_filepath.set(
            defaults.UPB_OUTPUT_FILEPATH)
        self.controller.frames["UPbInputOutputPage"].output_dir.set(
            defaults.OUTPUT_DIR)
        self.controller.frames["UPbInputOutputPage"].output_filename.set(
            defaults.UPB_OUTPUT_FILEPATH)

        self.controller.frames["FilterStandardsPage"].footerFrame.goToNextPage()

    def test_te(self):
        TE.te(defaults.TE_INPUT_FILEPATHS,
              defaults.TE_OUTPUT_FILEPATH, defaults.CHONDRITE_FILE)
        self.controller.isUpb = False
        self.controller.frames["TEInputOutputPage"].output_filepath.set(
            defaults.TE_OUTPUT_FILEPATH)
        self.controller.frames["TEInputOutputPage"].output_dir.set(
            defaults.OUTPUT_DIR)
        self.controller.frames["TEInputOutputPage"].output_filename.set(
            defaults.TE_OUTPUT_FILEPATH)

        self.controller.frames["FilterStandardsPage"].footerFrame.goToNextPage()
