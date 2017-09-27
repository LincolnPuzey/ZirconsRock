from gui.resources import *

class InputOutputPage(ttk.Frame):

     def __init__(self, parent, controller, title):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.title = title

        self.input_filepaths = []
        self.valid_input_filepaths = []
        self.input_listbox_items = StringVar()

        home_dir = os.path.expanduser('~/')
        self.output_filepath = StringVar(value="") #filepath = dir + filename
        self.output_filename = StringVar(value="")
        self.output_dir = StringVar(value=home_dir)

        self.headerFrame = Header(self, controller, "2. Input / Output for " + title, "")
        contentFrame = Content(self, controller)
        self.footerFrame = Footer(self, controller, True, "Back", "Continue", "StartPage", "FilterStandardsPage")

        inputTitleLabel = ttk.Label(contentFrame, text="Input CSV files (Click 'open' to add files)", style='subtitle.TLabel', padding='0 0 0 5')

        inputListFrame = ttk.Frame(contentFrame)
        self.inputList = tk.Listbox(inputListFrame, listvariable=self.input_listbox_items, selectmode=EXTENDED, height=5, relief="flat") #ridge
        scrollBar = ttk.Scrollbar(inputListFrame, orient=VERTICAL, command=self.inputList.yview)
        self.inputList.configure(yscrollcommand=scrollBar.set)

        self.errorLabel = ttk.Label(contentFrame, text="Unrecognised files will be ignored", style="error.TLabel", padding='0 0 5 0')

        inputButtonFrame = ttk.Frame(contentFrame, padding='0 5 0 15')
        removeButton = Button(inputButtonFrame, text="Remove", command=self.removeSelectedInputFiles)
        openButton = Button(inputButtonFrame, text="Open", command=self.addInputFile)

        outputTitleLabel = ttk.Label(contentFrame, text="Output Excel workbook", style='subtitle.TLabel', padding='0 0 0 5')

        self.outputPathLabel = ttk.Label(contentFrame, anchor='w', textvariable=self.output_filepath, style='filepath.TLabel', padding='0 5 0 5')
        outputButtonFrame = ttk.Frame(contentFrame, padding='0 5 0 0')
        saveButton = Button(outputButtonFrame, text="Save As", command=self.setOutputPath, )

        #contentFrame children
        inputTitleLabel.grid(       column=0, row=0, sticky=(W), columnspan=2)
        inputListFrame.grid(        column=0, row=1, sticky=(W,E), columnspan=2)
        inputButtonFrame.grid(      column=1, row=2, sticky=(E))
        outputTitleLabel.grid(      column=0, row=4, sticky=(W), columnspan=2)
        self.outputPathLabel.grid(  column=0, row=5, sticky=(W,E), columnspan=2)
        outputButtonFrame.grid(     column=0, row=6, sticky=(E), columnspan=2)

        #inputListFrame children
        self.inputList.grid(    column=0, row=0, sticky=(W,E))
        scrollBar.grid(         column=1, row=0, sticky=(N,S,E))

        #inputButtonFrame children
        removeButton.grid(      column=1, row=0, sticky=(E))
        openButton.grid(        column=2, row=0, sticky=(E))

        #outputButtonFrame children
        saveButton.grid(        column=0, row=0, sticky=(E))

        contentFrame.columnconfigure(0, weight=1)
        inputListFrame.columnconfigure(0, weight=1)
        contentFrame.rowconfigure(1, weight=1)

        #remove input files by selecting items and pressing the backspace button
        self.inputList.bind("<BackSpace>", self.removeSelectedInputFiles)
        self.inputList.bind("<Delete>", self.removeSelectedInputFiles)

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


     def addInputFile(self):
         filepaths = filedialog.askopenfilenames()  #paths is a tuple of filenames

         for path in filepaths:
             if path not in self.input_filepaths:
                 self.input_filepaths.append(path)
         self.input_listbox_items.set(self.input_filepaths)

         self.updateFilterStandardsPage()
         self.check_next_button()


     # using *event to accept 1 or 2 parameters
     #      gui button press:       passes 1 argument
     #      bound backspace press:  passes 2 arguments
     def removeSelectedInputFiles(self, *event):
         selection = self.inputList.curselection()

         for index in selection:
             self.input_filepaths.remove(self.inputList.get(index))
         self.input_listbox_items.set(self.input_filepaths)

         self.updateFilterStandardsPage()
         self.check_next_button()


     # updates the list of standards on the FilterStandardsPage
     def updateFilterStandardsPage(self):
         filterStandardsPage = self.controller.frames["FilterStandardsPage"]
         filterStandardsPage.clearStandards()
         self.errorLabel.grid_forget()
         self.numValidFiles = 0
         self.valid_input_filepaths.clear()

         index=0
         for path in self.input_filepaths:
             try:
                 filterStandardsPage.populateStandards(path)
                 # sucessfully retrieved standards from file -> green
                 self.inputList.itemconfig(index, {'background': styles.SUCCESS_COLOUR_LIGHT, 'selectbackground': styles.SUCCESS_COLOUR_MED})
                 self.numValidFiles+=1
                 self.valid_input_filepaths.append(path)
             except Exception as e:
                 #  unsuccessfully retrieved standards from file -> red
                 self.inputList.itemconfig(index, {'background': styles.ERROR_COLOUR_LIGHT, 'selectbackground': styles.ERROR_COLOUR_MED})
                 self.errorLabel.grid(column=0, row=2, sticky=(W,N,S))
                 print("Error while processing", path)
                 print("\t", e)
                 pass
             index+=1

     def setOutputPath(self):
         #  newPath = filedialog.askdirectory()
         oldName = self.output_filename.get()
         oldDir = self.output_dir.get()
         oldPath = self.output_filepath.get()

         newPath = filedialog.asksaveasfilename(initialfile=oldName, initialdir=oldDir,
                    defaultextension='.xlsx', filetypes=[('Excel', ('*.xlsx', '.xls'))],
                    title="Save Excel workbook")

         if newPath == "":
             return

         # get the file name from the file path
         if sys.platform.startswith("win"):
             newName = str.split(newPath, "\\")[-1]
             newDir = newPath[:-len(newName)]
         else:
             newName = str.split(newPath, "/")[-1]
             newDir = newPath[:-len(newName)]

         self.output_filepath.set(newPath)
         self.output_filename.set(newName)
         self.output_dir.set(newDir)
         self.check_next_button()


     def initialise(self):
         self.disable_next_button()

         filter_standards_page = self.controller.frames["FilterStandardsPage"]
         filter_standards_page.footerFrame.set_prev_page(self.title + InputOutputPage.__name__)

         finished_page = self.controller.frames["FinishedPage"]
         finished_page.input_output_page = self.title + InputOutputPage.__name__

         self.updateFilterStandardsPage()

         self.check_next_button()

     def check_next_button(self):
         if(self.numValidFiles > 0 and self.output_filename.get() != ""):
             self.enable_next_button()
         else:
             self.disable_next_button()

     def disable_next_button(self):
         self.footerFrame.nextButton.config(state=tk.DISABLED)

     def enable_next_button(self):
         self.footerFrame.nextButton.config(state=tk.NORMAL)
