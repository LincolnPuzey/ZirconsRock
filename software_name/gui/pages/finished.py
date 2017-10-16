from gui.resources import *


class FinishedPage(ttk.Frame):
    """
    Page that displays the name and location of the generated Excel workbook.

    There are buttons for:
        - Opening the Excel workbook
        - Showing the Excel workbook in its folder
        - Going back to the StartPage
        - Exiting the program
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        content_frame = Content(self, controller)
        footer_frame = Footer(self, controller, False, "", "", "FilterStandardsPage", "FinishedPage")

        doneLabel = ttk.Label(content_frame, text="Done.", style="title.TLabel")

        outInfoFrame = ttk.Frame(content_frame)
        nameTitleLabel = ttk.Label(outInfoFrame, text="Name of results: ", style="subtitle.TLabel")

        # use a StringVar so the Label updates when the user changes the file name
        outNameStr = controller.frames[self.get_input_output_page()].output_filename
        nameLabel = ttk.Label(outInfoFrame, textvariable=outNameStr, style="subtitle.TLabel")
        locationLabel = ttk.Label(outInfoFrame, text="Location of results: ", style="subtitle.TLabel")

        # use a StringVar so the Label updates when the user changes the file path
        outDirStr = controller.frames[self.get_input_output_page()].output_dir
        outPathLabel = ttk.Label(outInfoFrame, textvariable=outDirStr, style="subtitle.TLabel")

        button_frame_one = ttk.Frame(content_frame, padding="0 10 0 20")
        button_frame_two = ttk.Frame(content_frame, padding="0 0 0 5")
        button_frame_three = ttk.Frame(content_frame)

        openButton = Button(button_frame_one, text="Open", command=lambda: self.open())
        showInFolderButton = Button(button_frame_one, text="Show in folder", command=lambda: self.showInFolder())
        startAgainButton = Button(button_frame_two, text="Start again", command=lambda: controller.show_frame("StartPage"))
        exitButton = Button(button_frame_three, text="Exit", command=lambda: sys.exit())

        # content_frame children
        doneLabel.grid(column=0, row=0, sticky=(W))
        outInfoFrame.grid(column=0, row=2, sticky=(W))
        button_frame_one.grid(column=0, row=3, sticky=(W))
        button_frame_two.grid(column=0, row=4, sticky=(W))
        button_frame_three.grid(column=0, row=5, sticky=(W))

        # outInfoFrame children
        nameTitleLabel.grid(column=0, row=0, sticky=(W))
        nameLabel.grid(column=1, row=0, sticky=(W))
        locationLabel.grid(column=0, row=1, sticky=(W))
        outPathLabel.grid(column=1, row=1, sticky=(W))

        # button_frame_one children
        openButton.grid(column=0, row=0, sticky=(W))
        showInFolderButton.grid(column=0, row=1, sticky=(W))

        # button_frame_two children
        startAgainButton.grid(column=0, row=0, sticky=(W))

        # button_frame_three children
        exitButton.grid(column=0, row=0, sticky=(W))


    # https://stackoverflow.com/questions/13078071/start-another-program-from-python-separately
    def open(self):
        """Opens the Excel workbook"""

        input_output_page = self.get_input_output_page()

        filepath = self.controller.frames[input_output_page].output_filepath.get()
        try:
            if sys.platform.startswith("win"):
                os.startfile(filepath)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(["open", filepath])
            else:
                subprocess.Popen(["xdg-open", filepath])
        except:
            pass


    # https://stackoverflow.com/questions/6631299/python-opening-a-folder-in-explorer-nautilus-mac-thingie
    def showInFolder(self):
        """Shows the Excel workbook in its folder"""

        input_output_page = self.get_input_output_page()

        dir_path = self.controller.frames[input_output_page].output_dir.get()

        try:
            if sys.platform.startswith("win"):
                os.startfile(dir_path)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(["open", dir_path])
            else:
                subprocess.Popen(["xdg-open", dir_path])
        except:
            pass


    def get_input_output_page(self):
        """
        Returns 'UPbInputOutputPage' if the user selected UPb processing at the StartPage
        Returns 'TEInputOutputPage' if the user selected TE processing at the StartPage
        """

        if self.controller.isUpb:
            return "UPbInputOutputPage"
        else:
            return "TEInputOutputPage"
