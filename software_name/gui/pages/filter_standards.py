from gui.resources import *

from defaults import CHONDRITE_FILE

import data_processing.UPb as UPb
import data_processing.TE as TE
import data_processing.common as common


class FilterStandardsPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.header_frame = Header(self, controller, "", "")
        content_frame = Content(self, controller)
        self.footerFrame = Footer(
            self, controller, True, "Back", "Go", "InputOutputPage", "FinishedPage")

        self.footerFrame.set_next_btn_command(self.on_go)

        title_frame = ttk.Frame(content_frame)
        self.standard_label = ttk.Label(
            title_frame, text="Standard", style='subtitle.TLabel', padding="0 0 10 10")
        self.norm_label = ttk.Label(
            title_frame, text="N", style='subtitle.TLabel', padding="0 0 10 10")
        self.control_label = ttk.Label(
            title_frame, text="C", style='subtitle.TLabel', padding="0 0 10 10")

        self.canvas = tk.Canvas(
            content_frame, highlightthickness=0, background=styles.BG_COLOUR)
        self.scrollbar = ttk.Scrollbar(
            content_frame, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.inner_canvas_frame = ttk.Frame(self.canvas)

        title_frame.grid(column=0, row=0, sticky=(W))

        # title_frame children
        self.standard_label.grid(column=0, row=0, sticky=(W, E))
        self.norm_label.grid(column=1, row=0, sticky=(W, E))
        self.control_label.grid(column=2, row=0, sticky=(W, E))

        self.canvas.grid(column=0, row=1, sticky=(N, S, E, W), columnspan=3)
        self.scrollbar.grid(column=3, row=1, sticky=(N, S, E))

        # Temp button
        norm_button = Button(content_frame, text="Norm", command=lambda: print(
            self.get_normalising_standards()))
        control_button = Button(content_frame, text="Control",
                                command=lambda: print(self.get_control_standards()))

        norm_button.grid(column=0, row=2)
        control_button.grid(column=1, row=2)

        self.canvas.create_window(
            (0, 0), window=self.inner_canvas_frame, anchor="nw", tags="self.inner_canvas_frame")
        self.inner_canvas_frame.bind("<Configure>", self.on_frame_configure)

        # mousewheel bindings are platform dependant
        if sys.platform.startswith('linux'):
            self.bind_all("<Button-4>", self.on_mouse_wheel)
            self.bind_all("<Button-5>", self.on_mouse_wheel)
        else:
            self.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.standards = []
        self.is_norm_str_vars = []
        self.is_control_str_vars = []

    def populate_standards(self, filepath):

        # set the width of columns in the canvas to match the width of columns outside the canvas
        self.inner_canvas_frame.columnconfigure(
            0, minsize=self.standard_label.winfo_width())
        self.inner_canvas_frame.columnconfigure(
            1, minsize=self.norm_label.winfo_width())
        self.inner_canvas_frame.columnconfigure(
            2, minsize=self.control_label.winfo_width())

        # common.standard requires a list of filepaths
        file_path_list = []
        file_path_list.append(filepath)

        new_standards = []
        if self.controller.isUpb:
            new_standards = common.standard(UPb.getAllZircons(file_path_list))
        else:
            new_standards = common.standard(TE.getAllZircons(file_path_list))

        row = len(self.standards)
        for s in new_standards:
            if s not in self.standards:

                self.standards.append(s)
                standard_name_label = ttk.Label(
                    self.inner_canvas_frame, text=s, padding="10 0 10 0")

                is_norm = tk.StringVar(value="")
                is_control = tk.StringVar(value="")

                self.is_norm_str_vars.append(is_norm)
                self.is_control_str_vars.append(is_control)

                is_norm_btn = CustomCheckbutton(
                    self.inner_canvas_frame, variable=is_norm, onvalue=s, offvalue="", padding="0 0 0 0")
                is_control_btn = CustomCheckbutton(
                    self.inner_canvas_frame, variable=is_control, onvalue=s, offvalue="", padding="0 0 0 0")

                standard_name_label.grid(column=0, row=row, sticky=E)
                is_norm_btn.grid(column=1, row=row)
                is_control_btn.grid(column=2, row=row)

                row += 1

        # use 'invisible' labels to align canvas content with the above titles
        # invisibleStandardLabel = ttk.Label(self.inner_canvas_frame, text="Standard", padding="0 0 10 10")
        # invisibleNormLabel = ttk.Label(self.inner_canvas_frame, text="Normalizing",  padding="0 0 10 10")
        # invisibleControlLabel = ttk.Label(self.inner_canvas_frame, text="Control",   padding="0 0 10 10")
        #
        # invisibleStandardLabel.grid( column=0, row=20, sticky=(E))
        # invisibleNormLabel.grid(     column=1, row=20, sticky=(E))
        # invisibleControlLabel.grid(  column=2, row=20, sticky=(E))

    def clear_standards(self):
        for widget in self.inner_canvas_frame.winfo_children():
            widget.destroy()
        self.standards.clear()
        self.is_norm_str_vars.clear()
        self.is_control_str_vars.clear()

    def get_normalising_standards(self):
        standards = []
        for strVar in self.is_norm_str_vars:
            if strVar.get() != "":
                standards.append(strVar.get())

        return standards

    def get_control_standards(self):
        standards = []
        for strVar in self.is_control_str_vars:
            if strVar.get() != "":
                standards.append(strVar.get())

        return standards

    # enables scrolling from anywhere on the page
    # Note: yview_scroll's first parameter is platform dependant
    # Note: darwin = macOS
    # https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar
    # UnicodeDecodeError on MacOS: https://stackoverflow.com/questions/16995969/inertial-scrolling-in-mac-os-x-with-tkinter-and-python
    def on_mouse_wheel(self, event):
        if sys.platform.startswith('darwin'):
            self.canvas.yview_scroll(-1 * event.delta, "units")
        elif sys.platform.startswith('win'):
            self.canvas.yview_scroll(-1 * (event.delta / 120), "units")
        elif sys.platform.startswith('linux'):
            self.canvas.yview_scroll(-1 * (event.delta / 120), "units")

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def initialise_u_pb(self):
        self.header_frame.set_title("3. Filter standards for UPb")

    def initialise_t_e(self):
        self.header_frame.set_title("3. Filter standards for TE")

    def on_go(self, *event):
        control_standards = self.get_control_standards()
        normalising_standards = self.get_normalising_standards()
        print(CHONDRITE_FILE)
        if self.controller.isUpb:
            output_filepath = self.controller.frames["UPbInputOutputPage"].output_filepath.get(
            )
            files = self.controller.frames["UPbInputOutputPage"].valid_input_filepaths
            UPb.UPb(control_standards, normalising_standards,
                    files, output_filepath)
            self.footerFrame.go_to_next_page()
        else:
            output_filepath = self.controller.frames["TEInputOutputPage"].output_filepath.get(
            )
            files = self.controller.frames["TEInputOutputPage"].valid_input_filepaths
            TE.te(files, output_filepath, CHONDRITE_FILE)
            self.footerFrame.go_to_next_page()
