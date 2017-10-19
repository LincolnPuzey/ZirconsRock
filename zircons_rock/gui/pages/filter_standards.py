from gui.resources import *

from defaults import CHONDRITE_FILE

import data_processing.UPb as UPb
import data_processing.TE as TE
import data_processing.common as common

# Serialised pickle files
from defaults import GUI_TEMPS_DIR
from defaults import UPB_NORMALISING
from defaults import UPB_CONTROLS
from defaults import UPB_UNKNOWNS
from defaults import TE_CONTROLS
from defaults import TE_UNKNOWNS
from defaults import URANIUM_PPM
from defaults import THORIUM_PPM
from defaults import USE_CART_FOR_PLOTS

from defaults import UPB_INPUT_FILEPATHS
from defaults import UPB_OUTPUT_FILEPATH
from defaults import UPB_OUTPUT_FILENAME
from defaults import UPB_OUTPUT_DIR
from defaults import TE_INPUT_FILEPATHS
from defaults import TE_OUTPUT_FILEPATH
from defaults import TE_OUTPUT_FILENAME
from defaults import TE_OUTPUT_DIR

from defaults import DEFAULT_URANIUM_PPM
from defaults import DEFAULT_THORIUM_PPM

class FilterStandardsPage(ttk.Frame):
    """
    Page for specifying which standards are normalising, control and unknown.

    The paths to the input CSV files are saved (pickled) so they can be loaded
    after the user closes and opens the program. The name and location of the
    Excel workbook are saved too.

    Two of these FilterStandardsPage pages are created in App.py. One for UPb and one for TE.

    The FilterStandardsPage for UPb has two entry boxes for specifying
    Uranium and Thorium PPM values.
    """

    def __init__(self, parent, controller, title):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.title = title

        self.header_frame = Header(self, controller, "3. Filter standards for " + self.title, "")

        content_frame = Content(self, controller)

        if self.title == "UPb":
            self.footer_frame = Footer(
                self, controller, True, "Back", "Go", "UPbInputOutputPage", "FinishedPage")
        else:
            self.footer_frame = Footer(
                self, controller, True, "Back", "Go", "TEInputOutputPage", "FinishedPage")

        self.footer_frame.set_next_btn_command(self.on_go)
        self.footer_frame.set_prev_btn_command(self.on_back)

        title_frame = ttk.Frame(content_frame)
        self.standard_label = ttk.Label(
            title_frame, text="Standard", style='subtitle.TLabel', padding="0 0 10 10")

        if self.title == "UPb":
            self.norm_label = ttk.Label(
                title_frame, text="N", style='subtitle.TLabel', padding="0 0 10 10")
            self.control_label = ttk.Label(
                title_frame, text="C", style='subtitle.TLabel', padding="0 0 10 10")
            self.unknown_label = ttk.Label(
                title_frame, text="U", style='subtitle.TLabel', padding="0 0 10 10")
        else:
            self.control_label = ttk.Label(
                title_frame, text="C", style='subtitle.TLabel', padding="0 0 10 10")
            self.unknown_label = ttk.Label(
                title_frame, text="U", style='subtitle.TLabel', padding="0 0 10 10")

        self.canvas = tk.Canvas(content_frame, highlightthickness=0, background=styles.BG_COLOUR, width=50, height=400)
        self.scrollbar = AutoScrollbar(content_frame)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.inner_canvas_frame = ttk.Frame(self.canvas)
        self.scrollbar.config(command=self.canvas.yview)

        self.all_button_frame = ttk.Frame(content_frame, padding="0 10 0 0")
        self.select_all_button = Button(self.all_button_frame, text="Select all", command=self.select_all_checkbuttons)
        self.deselect_all_button = Button(self.all_button_frame, text="Deselect all", command=self.deselect_all_checkbuttons)


        self.right_col_frame = ttk.Frame(content_frame, padding="30 0 0 0")
        self.legend_frame = ttk.Labelframe(self.right_col_frame, text="Legend", padding="10 10 10 10")

        if self.title == "UPb":
            self.norm_leg_label = ttk.Label(self.legend_frame, text="N: Normalising")
            self.control_leg_label = ttk.Label(self.legend_frame, text="C: Control")
            self.unknown_leg_label = ttk.Label(self.legend_frame, text="U: Unknown")
        else:
            self.control_leg_label = ttk.Label(self.legend_frame, text="C: Control")
            self.unknown_leg_label = ttk.Label(self.legend_frame, text="U: Unknown")

        # content_frame children
        title_frame.grid(column=0, row=0, sticky=(W))
        self.canvas.grid(column=0, row=1, sticky=(N, S, E, W))
        self.all_button_frame.grid(column=0, row=2, sticky=(N,S,E,W))
        self.scrollbar.grid(column=1, row=1, sticky=(N, S, E))
        self.right_col_frame.grid(column=2, row=0, sticky=(N,W), rowspan=2)

        # title_frame children
        self.standard_label.grid(column=0, row=0, sticky=(W, E))
        if self.title == "UPb":
            self.norm_label.grid(column=1, row=0, sticky=(W, E))
            self.control_label.grid(column=2, row=0, sticky=(W, E))
            self.unknown_label.grid(column=3, row=0, sticky=(W, E))
        else:
            self.control_label.grid(column=1, row=0, sticky=(W, E))
            self.unknown_label.grid(column=2, row=0, sticky=(W, E))

        # all_button_frame children
        self.select_all_button.grid(column=0, row=0, sticky=(N,S,E,W))
        self.deselect_all_button.grid(column=1, row=0, sticky=(N,S,E,W))


        # right_col_frame children
        self.legend_frame.grid(column=0, row=0, sticky=(N,S,E,W))

        # legend_frame children
        if self.title == "UPb":
            self.norm_leg_label.grid(column=0, row=0, sticky=(N,W))
            self.control_leg_label.grid(column=0, row=1, sticky=(N,W))
            self.unknown_leg_label.grid(column=0, row=2, sticky=(N,W))
        else:
            self.control_leg_label.grid(column=0, row=0, sticky=(N,W))
            self.unknown_leg_label.grid(column=0, row=1, sticky=(N,W))


        if title == "UPb":
            self.ppm_frame = ttk.Labelframe(self.right_col_frame, text="PPM Values", padding="10 10 10 10")
            self.uranium_ppm_frame = ttk.Frame(self.ppm_frame, padding="0 0 0 5")
            self.thorium_ppm_frame = ttk.Frame(self.ppm_frame, padding="0 0 0 5")

            self.uranium_ppm = tk.StringVar(value=DEFAULT_URANIUM_PPM)
            self.thorium_ppm = tk.StringVar(value=DEFAULT_THORIUM_PPM)

            self.uranium_ppm_label = ttk.Label(self.uranium_ppm_frame, text="Uranium", padding="0 0 10 5")
            self.thorium_ppm_label = ttk.Label(self.thorium_ppm_frame, text="Thorium", padding="0 0 10 5")
            self.reset_button = Button(self.ppm_frame, text="Reset", command=self.set_default_ppms)

            # restricts entry box to numbers only
            vcmd = (self.ppm_frame.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
            self.uranium_ppm_entry = ttk.Entry(self.uranium_ppm_frame, textvariable=self.uranium_ppm, width=10, validate = 'key', validatecommand = vcmd)
            self.thorium_ppm_entry = ttk.Entry(self.thorium_ppm_frame, textvariable=self.thorium_ppm, width=10, validate = 'key', validatecommand = vcmd)

            # right_col_frame children
            self.ppm_frame.grid(column=0, row=1, sticky=(N,S,E,W))

            # ppm_frame children
            self.uranium_ppm_frame.grid(column=0, row=0, sticky=(N,S,E,W))
            self.thorium_ppm_frame.grid(column=0, row=1, sticky=(N,S,E,W))
            self.reset_button.grid(column=0, row=2, sticky=(N,S,E,W))

            # uranium_ppm_frame children
            self.uranium_ppm_label.grid(column=0, row=0, sticky=(N,W,E,S))
            self.uranium_ppm_entry.grid(column=0, row=1, sticky=(N,W,E,S))

            # thorium_ppm_frame children
            self.thorium_ppm_label.grid(column=1, row=0, sticky=(N,W,E,S))
            self.thorium_ppm_entry.grid(column=1, row=1, sticky=(N,W,E,S))

        else:
            self.cart_frame = ttk.Labelframe(self.right_col_frame, text="Scatterplots", padding="10 10 10 10")
            self.cart_question = ttk.Label(self.cart_frame, text="Use cart\nclassifications\nfor scatterplots?", padding="0 0 0 5")
            self.yes_button_frame = ttk.Frame(self.cart_frame, padding="10 0 0 0")
            self.no_button_frame = ttk.Frame(self.cart_frame, padding="10 0 0 0")

            self.use_cart_for_plots = tk.BooleanVar(value=True)
            self.yes_button = CustomRadiobutton(self.yes_button_frame, variable=self.use_cart_for_plots, value=True, padding="0 0 0 0", num_columns=2)
            self.yes_label = ttk.Label(self.yes_button_frame, text="Yes")
            self.no_button = CustomRadiobutton(self.no_button_frame, variable=self.use_cart_for_plots, value=False, padding="0 0 0 0", num_columns=2)
            self.no_label = ttk.Label(self.no_button_frame, text="No")

            # right_col_frame children
            self.cart_frame.grid(column=0, row=1, sticky=(N,S,E,W))

            # cart_frame children
            self.cart_question.grid(column=0, row=0, sticky=(W))
            self.yes_button_frame.grid(column=0, row=1, sticky=(N,S,E,W))
            self.no_button_frame.grid(column=0, row=2, sticky=(N,S,E,W))

            # yes_button_frame children
            self.yes_button.grid(column=0, row=0, sticky=(N,S,E,W))
            self.yes_label.grid(column=1, row=0, sticky=(W))

            # no_button_frame children
            self.no_button.grid(column=0, row=0, sticky=(N,S,E,W))
            self.no_label.grid(column=1, row=0, sticky=(W))

        self.canvas.create_window(
            (0, 0), window=self.inner_canvas_frame, anchor="nw", tags="self.inner_canvas_frame")
        self.inner_canvas_frame.bind("<Configure>", self.on_frame_configure)

        self.standards = []
        self.norm_std = StringVar()

        #dictionaries of std_name:string_var
        self.is_control_str_vars = {}
        self.is_unknown_str_vars = {}

        self.control_checkbuttons = []
        self.unknown_checkbuttons = []

        # dictionaries of std_name:is_selected
        self.norm_std_prefs = ""
        self.control_std_prefs = {}
        self.unknown_std_prefs = {}
        self.load_std_prefs()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(1, weight=1)

    def populate_upb_standards(self, filepath):
        """
        Reads all standards from the CSV file specified by filepath

        Compares
        """

        # set the width of columns in the canvas to match the width of columns outside the canvas
        self.inner_canvas_frame.columnconfigure(0, minsize=self.standard_label.winfo_width())
        self.inner_canvas_frame.columnconfigure(1, minsize=self.norm_label.winfo_width())
        self.inner_canvas_frame.columnconfigure(2, minsize=self.control_label.winfo_width())

        # common.standard requires a list of filepaths
        file_path_list = []
        file_path_list.append(filepath)

        new_standards = []
        new_standards = common.standard(UPb.getAllZircons(file_path_list))

        row = len(self.standards)
        for s in new_standards:
            if s not in self.standards:

                self.standards.append(s)
                standard_name_label = ttk.Label(
                    self.inner_canvas_frame, text=s, padding="10 0 10 0")

                is_control = tk.StringVar(value="")
                is_unknown = tk.StringVar(value="")
                self.is_control_str_vars[s] = is_control
                self.is_unknown_str_vars[s] = is_unknown

                # remember which standard was the normalising standard
                if self.norm_std_prefs == s:
                    self.norm_std.set(s)

                if s in self.control_std_prefs:
                    if self.control_std_prefs[s] == 1:
                        is_control.set(s)
                else:
                    self.control_std_prefs[s] = 0

                if s in self.unknown_std_prefs:
                    if self.unknown_std_prefs[s] == 1:
                        is_unknown.set(s)
                else:
                    self.unknown_std_prefs[s] = 0

                is_norm_btn = CustomRadiobutton(
                    self.inner_canvas_frame, variable=self.norm_std, value=s, padding="0 0 0 0", num_columns=3)
                is_control_btn = CustomCheckbutton(
                    self.inner_canvas_frame, variable=is_control, onvalue=s, offvalue="", padding="0 0 0 0", num_columns=3)
                is_unknown_btn = CustomCheckbutton(
                    self.inner_canvas_frame, variable=is_unknown, onvalue=s, offvalue="", padding="0 0 0 0", num_columns=3)

                self.control_checkbuttons.append(is_control_btn)
                self.unknown_checkbuttons.append(is_unknown_btn)

                standard_name_label.grid(column=0, row=row, sticky=E)

                is_norm_btn.grid(column=1, row=row)
                is_control_btn.grid(column=2, row=row)
                is_unknown_btn.grid(column=3, row=row)

                row += 1

        # Set the default normalising standard
        if self.norm_std.get() == "" and len(self.standards) > 0:
            self.norm_std.set(self.standards[0])


    def populate_te_standards(self, filepath):
        # set the width of columns in the canvas to match the width of columns outside the canvas
        self.inner_canvas_frame.columnconfigure(0, minsize=self.standard_label.winfo_width())
        self.inner_canvas_frame.columnconfigure(1, minsize=self.control_label.winfo_width())
        self.inner_canvas_frame.columnconfigure(2, minsize=self.unknown_label.winfo_width())

        # common.standard requires a list of filepaths
        file_path_list = []
        file_path_list.append(filepath)

        new_standards = []
        new_standards = common.standard(TE.getAllZircons(file_path_list))

        row = len(self.standards)
        for s in new_standards:
            if s not in self.standards:

                self.standards.append(s)
                standard_name_label = ttk.Label(self.inner_canvas_frame, text=s, padding="10 0 10 0")

                is_control = tk.StringVar(value="")
                is_unknown = tk.StringVar(value="")
                self.is_control_str_vars[s] = is_control
                self.is_unknown_str_vars[s] = is_unknown

                if s in self.control_std_prefs:
                    if self.control_std_prefs[s] == 1:
                        is_control.set(s)
                else:
                    self.control_std_prefs[s] = 0

                if s in self.unknown_std_prefs:
                    if self.unknown_std_prefs[s] == 1:
                        is_unknown.set(s)
                else:
                    self.unknown_std_prefs[s] = 0

                is_control_btn = CustomCheckbutton(
                    self.inner_canvas_frame, variable=is_control, onvalue=s, offvalue="", padding="0 0 0 0", num_columns=2)
                is_unknown_btn = CustomCheckbutton(
                    self.inner_canvas_frame, variable=is_unknown, onvalue=s, offvalue="", padding="0 0 0 0", num_columns=2)

                self.control_checkbuttons.append(is_control_btn)
                self.unknown_checkbuttons.append(is_unknown_btn)

                standard_name_label.grid(column=0, row=row, sticky=E)

                is_control_btn.grid(column=1, row=row)
                is_unknown_btn.grid(column=2, row=row)

                row += 1


    def clear_standards(self):
        """Resets all standard information by clearing lists"""

        for widget in self.inner_canvas_frame.winfo_children():
            widget.destroy()
        self.standards.clear()
        self.norm_std.set("")
        self.is_control_str_vars.clear()
        self.is_unknown_str_vars.clear()
        self.control_checkbuttons.clear()
        self.unknown_checkbuttons.clear()


    def get_control_standards(self):
        """Returns a list of standards specified as control"""

        standards = []
        for strVar in self.is_control_str_vars.values():
            if strVar.get() != "":
                standards.append(strVar.get())

        return standards


    def get_unknown_standards(self):
        """Returns a list of standards specified as unknown"""

        standards = []
        for strVar in self.is_unknown_str_vars.values():
            if strVar.get() != "":
                standards.append(strVar.get())

        return standards


    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def select_all_checkbuttons(self):
        """Selects all checkbuttons on the page"""

        for btn in self.control_checkbuttons:
            btn.select()
        for btn in self.unknown_checkbuttons:
            btn.select()


    def deselect_all_checkbuttons(self):
        """Deselects all checkbuttons on the page"""

        for btn in self.control_checkbuttons:
            btn.deselect()
        for btn in self.unknown_checkbuttons:
            btn.deselect()


    def set_default_ppms(self):
        """Sets Uranium PPM and Thorium PPM as their default values"""
        self.uranium_ppm.set(DEFAULT_URANIUM_PPM)
        self.thorium_ppm.set(DEFAULT_THORIUM_PPM)


    def load_std_prefs(self):
        """
        Loads (unpickles) dictionaries that identify which standards
        were previously specified as Normalising, Control and Unknown.
        """

        if not os.path.isdir(GUI_TEMPS_DIR):
            os.makedirs(GUI_TEMPS_DIR)

        successful_load = True

        if self.title == "UPb":
            try:
                pickled_norm_stds = open(UPB_NORMALISING, 'rb')
                pickled_upb_ppm = open(URANIUM_PPM, 'rb')
                pickled_th_ppm = open(THORIUM_PPM, 'rb')
                pickled_controls_stds = open(UPB_CONTROLS, 'rb')
                pickled_unknown_stds = open(UPB_UNKNOWNS, 'rb')
            except FileNotFoundError:
                successful_load = False
        else:
            try:
                pickled_controls_stds = open(TE_CONTROLS, 'rb')
                pickled_unknown_stds = open(TE_UNKNOWNS, 'rb')
                pickled_use_cart = open(USE_CART_FOR_PLOTS, 'rb')
            except FileNotFoundError:
                successful_load = False

        if successful_load:
            if self.title == "UPb":
                self.norm_std_prefs = pickle.load(pickled_norm_stds)
                self.uranium_ppm.set(pickle.load(pickled_upb_ppm))
                self.thorium_ppm.set(pickle.load(pickled_th_ppm))
            self.control_std_prefs = pickle.load(pickled_controls_stds)
            self.unknown_std_prefs = pickle.load(pickled_unknown_stds)
            if self.title == "TE":
                self.use_cart_for_plots.set(pickle.load(pickled_use_cart))

        try:
            if self.title == "UPb":
                pickled_norm_stds.close()
                pickled_upb_ppm.close()
                pickled_th_ppm.close()
            pickled_controls_stds.close()
            pickled_unknown_stds.close()
            if self.title == "TE": pickled_use_cart.close()
        except UnboundLocalError:
            pass


    def save_std_prefs(self):
        """
        Saves (pickles) dictionaries that maintain which
        standards are currently specified as Normalising, Control and Unknown.
        """

        successful_load = True

        if self.title == "UPb":
            try:
                pickled_norm_stds = open(UPB_NORMALISING, 'wb')
                pickled_upb_ppm = open(URANIUM_PPM, 'wb')
                pickled_th_ppm = open(THORIUM_PPM, 'wb')
                pickled_controls_stds = open(UPB_CONTROLS, 'wb')
                pickled_unknown_stds = open(UPB_UNKNOWNS, 'wb')
            except FileNotFoundError:
                successful_load = False
        else:
            try:
                pickled_controls_stds = open(TE_CONTROLS, 'wb')
                pickled_unknown_stds = open(TE_UNKNOWNS, 'wb')
                pickled_use_cart = open(USE_CART_FOR_PLOTS, 'wb')
            except FileNotFoundError:
                successful_load = False

        if successful_load:

            if self.title == "UPb": self.norm_std_prefs = self.norm_std.get()

            for std in self.control_std_prefs.copy():
                if std in self.is_control_str_vars:
                    if self.is_control_str_vars[std].get() != "":
                        self.control_std_prefs[std] = 1
                    else:
                        self.control_std_prefs[std] = 0

            for std in self.unknown_std_prefs.copy():
                if std in self.is_unknown_str_vars:
                    if self.is_unknown_str_vars[std].get() != "":
                        self.unknown_std_prefs[std] = 1
                    else:
                        self.unknown_std_prefs[std] = 0

            try:
                if self.title == "UPb":
                    pickle.dump(self.norm_std_prefs, pickled_norm_stds)
                    pickle.dump(self.uranium_ppm.get(), pickled_upb_ppm)
                    pickle.dump(self.thorium_ppm.get(), pickled_th_ppm)
                pickle.dump(self.control_std_prefs, pickled_controls_stds)
                pickle.dump(self.unknown_std_prefs, pickled_unknown_stds)
                if self.title == "TE":
                    pickle.dump(self.use_cart_for_plots.get(), pickled_use_cart)
            except:
                pass

        try:
            if self.title == "UPb":
                pickled_norm_stds.close()
                pickled_upb_ppm.close()
                pickled_th_ppm.close()
            pickled_controls_stds.close()
            pickled_unknown_stds.close()
            if self.title == "TE": pickled_use_cart.close()
        except UnboundLocalError:
            pass


    def validate(self, action, index, value_if_allowed,
    prior_value, text, validation_type, trigger_type, widget_name):
        """
        Returns True if an entry box contains an integer or float
        Source: https://stackoverflow.com/questions/8959815/restricting-the-value-in-tkinter-entry-widget
        """

        if(action=='1'):
            if text in '0123456789.-+':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True


    def on_back(self, *event):
        """Saves which standards are currently specified as normalising, control and unknown"""

        self.save_std_prefs()
        self.footer_frame.go_to_prev_page()


    def on_go(self, *event):
        """Executes UPb or TE dataprocessing"""

        control_standards = self.get_control_standards()
        unknown_standards = self.get_unknown_standards()

        self.save_std_prefs()

        if self.controller.isUpb:
            output_filepath = self.controller.frames["UPbInputOutputPage"].output_filepath.get()
            files = self.controller.frames["UPbInputOutputPage"].valid_input_filepaths
            UPb.UPb(files, output_filepath, self.norm_std.get(), control_standards, unknown_standards, self.uranium_ppm.get(), self.thorium_ppm.get())
            self.footer_frame.go_to_next_page()
        else:
            output_filepath = self.controller.frames["TEInputOutputPage"].output_filepath.get()
            files = self.controller.frames["TEInputOutputPage"].valid_input_filepaths

            TE.te(files, output_filepath, CHONDRITE_FILE, control_standards, unknown_standards)
            self.footer_frame.go_to_next_page()
