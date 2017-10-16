from gui.resources import *
from defaults import UPB_INPUT_FILEPATHS
from defaults import UPB_OUTPUT_FILEPATH
from defaults import UPB_OUTPUT_FILENAME
from defaults import UPB_OUTPUT_DIR
from defaults import TE_INPUT_FILEPATHS
from defaults import TE_OUTPUT_FILEPATH
from defaults import TE_OUTPUT_FILENAME
from defaults import TE_OUTPUT_DIR

import pickle

class InputOutputPage(ttk.Frame):
    """
    Page for specifying input CSV files, the name and location of the Excel
    workbook to be generated.

    User cannot proceed to the next page without specifying:
     - A valid input CSV file
     - Valid Excel workbook name
     - Valid Excel workbook location

    Whenever an input CSV file is added, the CSV file is checked for standards.
    If a problem occurs whilst checking a CSV file, it is considered 'unrecognised'
    and marked red in the GUI.

    The paths to the input CSV files are saved (pickled) so they can be loaded
    after the user closes and opens the program. The name and location of the
    Excel workbook are saved too.

    Two of these InputOutputPage pages are created in App.py. One for UPb and one for TE.
    """

    def __init__(self, parent, controller, title):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.title = title

        self.input_filepaths = []
        self.valid_input_filepaths = []
        self.input_listbox_items = StringVar()

        home_dir = os.path.expanduser('~/')
        self.output_filepath = StringVar(value="")  # filepath = dir + filename
        self.output_filename = StringVar(value="")
        self.output_dir = StringVar(value=home_dir)

        self.header_frame = Header(self, controller, "2. Input / Output for " + title, "")
        content_frame = Content(self, controller)

        if self.title == "UPb":
            self.footer_frame = Footer(
                self, controller, True, "Back", "Continue", "StartPage", "UPbFilterStandardsPage")
        else:
            self.footer_frame = Footer(
                self, controller, True, "Back", "Continue", "StartPage", "TEFilterStandardsPage")

        input_title_label = ttk.Label(content_frame, text="Input CSV files", style='subtitle.TLabel', padding='0 0 0 5')

        input_list_frame = ttk.Frame(content_frame)
        self.input_list = tk.Listbox(input_list_frame, listvariable=self.input_listbox_items,
                                    selectmode=EXTENDED, height=30, relief="flat")  # ridge
        scroll_bar = ttk.Scrollbar(input_list_frame, orient=VERTICAL, command=self.input_list.yview)
        self.input_list.configure(yscrollcommand=scroll_bar.set)

        self.error_label = ttk.Label(
            content_frame, text="Unrecognised files will be ignored", style="error.TLabel", padding='0 0 5 0')

        input_button_frame = ttk.Frame(content_frame, padding='0 5 0 15')
        remove_button = Button(input_button_frame, text="Remove", command=self.removeSelectedInputFiles)
        open_button = Button(input_button_frame, text="Add", command=self.addInputFile)

        output_title_label = ttk.Label(content_frame, text="Output Excel workbook", style='subtitle.TLabel', padding='0 0 0 5')
        output_instruction_label = ttk.Label(content_frame, text="(Choose a name and location)", style="tiny.TLabel")

        self.outputPathLabel = ttk.Label(
            content_frame, anchor='w', textvariable=self.output_filepath, style='filepath.TLabel', padding='0 5 0 5')
        output_button_frame = ttk.Frame(content_frame, padding='0 5 0 0')
        save_button = Button(output_button_frame, text="Choose", command=self.setOutputPath)

        # content_frame children
        input_title_label.grid(column=0, row=0, sticky=(W), columnspan=2)
        input_list_frame.grid(column=0, row=1, sticky=(W, E), columnspan=2)
        input_button_frame.grid(column=1, row=2, sticky=(E))
        output_title_label.grid(column=0, row=4, sticky=(W), columnspan=2)
        output_instruction_label.grid(column=1, row=4, sticky=(E))
        self.outputPathLabel.grid(column=0, row=5, sticky=(W, E), columnspan=2)
        output_button_frame.grid(column=0, row=6, sticky=(E), columnspan=2)

        # input_list_frame children
        self.input_list.grid(column=0, row=0, sticky=(W, E))
        scroll_bar.grid(column=1, row=0, sticky=(N, S, E))

        # input_button_frame children
        remove_button.grid(column=1, row=0, sticky=(E))
        open_button.grid(column=2, row=0, sticky=(E))

        # output_button_frame children
        save_button.grid(column=1, row=0, sticky=(E))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(1, weight=1)

        input_list_frame.columnconfigure(0, weight=1)
        input_list_frame.rowconfigure(0, weight=1)

        # remove input files by selecting items and pressing the backspace button
        self.input_list.bind("<BackSpace>", self.removeSelectedInputFiles)
        self.input_list.bind("<Delete>", self.removeSelectedInputFiles)


    def addInputFile(self):
        """
        Opens the operating system's file manager so a user can add
        input CSV files.
        """
        filepaths = filedialog.askopenfilenames()  # paths is a tuple of filenames

        for path in filepaths:
            if path not in self.input_filepaths:
                self.input_filepaths.append(path)
        self.input_listbox_items.set(self.input_filepaths)

        self.updateFilterStandardsPage()
        self.save_filepaths()
        self.check_next_button()


    # using *event to accept 1 or 2 parameters
    #      gui button press:       passes 1 argument
    #      bound backspace press:  passes 2 arguments
    def removeSelectedInputFiles(self, *event):
        """
        Removes the selected input CSV files.
        """
        selection = self.input_list.curselection()

        for index in selection:
            self.input_filepaths.remove(self.input_list.get(index))
        self.input_listbox_items.set(self.input_filepaths)

        self.updateFilterStandardsPage()
        self.save_filepaths()
        self.check_next_button()


    # updates the list of standards on the FilterStandardsPage
    def updateFilterStandardsPage(self):
        """
        Called whenever the list of input CSV files changes.

        Makes the FilterStandardsPage check every input CSV file for standards.
        If the FilterStandardsPage cannot find standards within a CSV file,
        that CSV file is marked red and considered 'unrecognised' or 'invalid'.
        """
        if self.controller.isUpb:
            filter_standards_page = self.controller.frames["UPbFilterStandardsPage"]
        else:
            filter_standards_page = self.controller.frames["TEFilterStandardsPage"]
        filter_standards_page.clear_standards()
        self.error_label.grid_forget()
        self.num_valid_files = 0
        self.valid_input_filepaths.clear()

        index = 0
        for path in self.input_filepaths:
            try:
                if self.controller.isUpb:
                    filter_standards_page.populate_upb_standards(path)
                else:
                    filter_standards_page.populate_te_standards(path)
                # sucessfully retrieved standards from file -> green
                self.input_list.itemconfig(index, {
                                          'background': styles.SUCCESS_COLOUR_LIGHT, 'selectbackground': styles.SUCCESS_COLOUR_MED})
                self.num_valid_files += 1
                self.valid_input_filepaths.append(path)
            except Exception as e:
                #  unsuccessfully retrieved standards from file -> red
                self.input_list.itemconfig(index, {
                                          'background': styles.ERROR_COLOUR_LIGHT, 'selectbackground': styles.ERROR_COLOUR_MED})
                self.error_label.grid(column=0, row=2, sticky=(W, N, S))
                # print("Unrecognised: ", path)
                # print("\t", e)
                pass
            index += 1


    def setOutputPath(self):
        """
        Opens the operating system's file manager so the user can specify
        the name and location of the output Excel workbook.
        """
        old_name = self.output_filename.get()
        old_dir = self.output_dir.get()
        olf_path = self.output_filepath.get()

        new_path = filedialog.asksaveasfilename(initialfile=old_name, initialdir=old_dir,
                    defaultextension='.xlsx', filetypes=[('Excel', ('*.xlsx', '.xls'))],
                    title="Save Excel workbook")

        if new_path == "":
            return

        # get the file name from the file path
        if sys.platform.startswith("win"):
            new_name = str.split(new_path, "\\")[-1]
            new_dir = new_path[:-len(new_name)]
        else:
            new_name = str.split(new_path, "/")[-1]
            new_dir = new_path[:-len(new_name)]

        self.output_filepath.set(new_path)
        self.output_filename.set(new_name)
        self.output_dir.set(new_dir)
        self.save_filepaths()
        self.check_next_button()


    def initialise(self):
        """Initialises the InputOutputPage"""
        self.disable_next_button()

        finished_page = self.controller.frames["FinishedPage"]
        finished_page.input_output_page = self.title + InputOutputPage.__name__

        self.updateFilterStandardsPage()
        self.load_filepaths()
        self.check_next_button()


    def check_next_button(self):
        """
        Enables the next button if there is at least one valid input CSV file and
        a filepath for the Excel workbook has been supplied.
        """
        if(self.num_valid_files > 0 and self.output_filename.get() != ""):
            self.enable_next_button()
        else:
            self.disable_next_button()


    def disable_next_button(self):
        """Disables the next button."""
        self.footer_frame.next_button.config(state=tk.DISABLED)

    def enable_next_button(self):
        """Enables the next button."""
        self.footer_frame.next_button.config(state=tk.NORMAL)


    # unpickles the input and ouput filepaths
    def load_filepaths(self):
        """Loads previously saved input/output filepaths from pickled objects."""

        try:
            successful_load = True

            if self.title == "UPb":
                try:
                    pickled_input_filepaths = open(UPB_INPUT_FILEPATHS, 'rb')
                    pickled_output_filepath = open(UPB_OUTPUT_FILEPATH, 'rb')
                    pickled_output_filename = open(UPB_OUTPUT_FILENAME, 'rb')
                    pickled_output_dir = open(UPB_OUTPUT_DIR, 'rb')
                except FileNotFoundError:
                    successful_load = False
            else:
                try:
                    pickled_input_filepaths = open(TE_INPUT_FILEPATHS, 'rb')
                    pickled_output_filepath = open(TE_OUTPUT_FILEPATH, 'rb')
                    pickled_output_filename = open(TE_OUTPUT_FILENAME, 'rb')
                    pickled_output_dir = open(TE_OUTPUT_DIR, 'rb')
                except FileNotFoundError:
                    successful_load = False

            if successful_load:
                self.input_filepaths = pickle.load(pickled_input_filepaths)
                self.output_filepath.set(pickle.load(pickled_output_filepath))
                self.output_filename.set(pickle.load(pickled_output_filename))
                self.output_dir.set(pickle.load(pickled_output_dir))

                # check input_filepaths are accessible (e.g. filepath to a USB that was removed from the system)
                # https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
                paths_to_remove = []
                for path in self.input_filepaths:
                    dirname = os.path.dirname(path) or os.getcwd()
                    if not os.access(dirname, os.W_OK):
                        paths_to_remove.append(path)

                for path in paths_to_remove:
                    self.input_filepaths.remove(path)

                self.input_listbox_items.set(self.input_filepaths)

                # check output_filepath is valid (e.g. filepath to a USB that was removed from the system)
                # https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
                dirname = os.path.dirname(self.output_filepath.get()) or os.getcwd()
                if not os.access(dirname, os.W_OK):
                    self.output_filepath.set("")
                    self.output_filename.set("")
                    self.output_dir.set("")

                self.updateFilterStandardsPage()
                self.save_filepaths()

            try:
                pickled_input_filepaths.close()
                pickled_output_filepath.close()
                pickled_output_filename.close()
                pickled_output_dir.close()
            except UnboundLocalError:
                pass
        except:
            pass


    # pickles the input and output filepaths so they can be loaded after closing the application
    def save_filepaths(self):
        """Saves the input/output filepaths as pickled objects."""

        try:
            if self.title == "UPb":
                try:
                    pickled_input_filepaths = open(UPB_INPUT_FILEPATHS, 'wb')
                    pickled_output_filepath = open(UPB_OUTPUT_FILEPATH, 'wb')
                    pickled_output_filename = open(UPB_OUTPUT_FILENAME, 'wb')
                    pickled_output_dir = open(UPB_OUTPUT_DIR, 'wb')
                except FileNotFoundError:
                    successful_load = False
            else:
                try:
                    pickled_input_filepaths = open(TE_INPUT_FILEPATHS, 'wb')
                    pickled_output_filepath = open(TE_OUTPUT_FILEPATH, 'wb')
                    pickled_output_filename = open(TE_OUTPUT_FILENAME, 'wb')
                    pickled_output_dir = open(TE_OUTPUT_DIR, 'wb')
                except FileNotFoundError:
                    successful_load = False

            try:
                pickle.dump(self.input_filepaths, pickled_input_filepaths)
                pickle.dump(self.output_filepath.get(), pickled_output_filepath)
                pickle.dump(self.output_filename.get(), pickled_output_filename)
                pickle.dump(self.output_dir.get(), pickled_output_dir)
            except:
                pass

            try:
                pickled_input_filepaths.close()
                pickled_output_filepath.close()
                pickled_output_filename.close()
                pickled_output_dir.close()
            except UnboundLocalError:
                pass
        except:
            pass
