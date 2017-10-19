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

        done_label = ttk.Label(content_frame, text="Done.", style="title.TLabel")

        out_info_frame = ttk.Frame(content_frame)
        name_title_label = ttk.Label(out_info_frame, text="Name of results: ", style="subtitle.TLabel")

        # use a StringVar so the Label updates when the user changes the file name
        self.out_name_str = tk.StringVar()
        name_label = ttk.Label(out_info_frame, textvariable=self.out_name_str, style="subtitle.TLabel")
        location_label = ttk.Label(out_info_frame, text="Location of results: ", style="subtitle.TLabel")

        # use a StringVar so the Label updates when the user changes the file path
        self.out_dir_str = tk.StringVar()
        out_path_label = ttk.Label(out_info_frame, textvariable=self.out_dir_str, style="subtitle.TLabel")

        button_frame_one = ttk.Frame(content_frame, padding="0 10 0 20")
        button_frame_two = ttk.Frame(content_frame, padding="0 0 0 5")
        button_frame_three = ttk.Frame(content_frame)

        open_button = Button(button_frame_one, text="Open", command=lambda: self.open())
        show_in_folder_button = Button(button_frame_one, text="Show in folder", command=lambda: self.showInFolder())
        start_again_button = Button(button_frame_two, text="Start again", command=lambda: controller.show_frame("StartPage"))
        exit_button = Button(button_frame_three, text="Exit", command=lambda: sys.exit())

        # content_frame children
        done_label.grid(column=0, row=0, sticky=(W))
        out_info_frame.grid(column=0, row=2, sticky=(W))
        button_frame_one.grid(column=0, row=3, sticky=(W))
        button_frame_two.grid(column=0, row=4, sticky=(W))
        button_frame_three.grid(column=0, row=5, sticky=(W))

        # out_info_frame children
        name_title_label.grid(column=0, row=0, sticky=(W))
        name_label.grid(column=1, row=0, sticky=(W))
        location_label.grid(column=0, row=1, sticky=(W))
        out_path_label.grid(column=1, row=1, sticky=(W))

        # button_frame_one children
        open_button.grid(column=0, row=0, sticky=(W))
        show_in_folder_button.grid(column=0, row=1, sticky=(W))

        # button_frame_two children
        start_again_button.grid(column=0, row=0, sticky=(W))

        # button_frame_three children
        exit_button.grid(column=0, row=0, sticky=(W))


    def update(self, name, directory):
        """Updates the name and location of the generated workbook"""

        if sys.platform.startswith("win"):
            directory = self.unix_path_to_windows(directory)

        self.out_name_str.set(name)
        self.out_dir_str.set(directory)


    # https://stackoverflow.com/questions/13078071/start-another-program-from-python-separately
    def open(self):
        """Opens the Excel workbook"""

        input_output_page = self.get_input_output_page()

        filepath = self.controller.frames[input_output_page].output_filepath.get()
        try:
            if sys.platform.startswith("win"):
                filepath = self.unix_path_to_windows(filepath)
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
                dir_path = self.unix_path_to_windows(dir_path)
                os.startfile(dir_path)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(["open", dir_path])
            else:
                subprocess.Popen(["xdg-open", dir_path])
        except:
            pass


    def unix_path_to_windows(self, path):
        """Takes a path of the form 'foo/bar/text.txt' and returns 'foo\bar\text.txt'"""

        return path.replace('/', '\\')


    def get_input_output_page(self):
        """
        Returns 'UPbInputOutputPage' if the user selected UPb processing at the StartPage
        Returns 'TEInputOutputPage' if the user selected TE processing at the StartPage
        """

        if self.controller.isUpb:
            return "UPbInputOutputPage"
        else:
            return "TEInputOutputPage"
