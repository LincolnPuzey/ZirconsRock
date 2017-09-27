from gui.resources import *


# from data_processing.UPb import *
import data_processing.UPb as UPb
import data_processing.TE as TE
import data_processing.common as common

class FilterStandardsPage(ttk.Frame):

     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.headerFrame = Header(self, controller, "", "")
        contentFrame = Content(self, controller)
        self.footerFrame = Footer(self, controller, True, "Back", "Go", "InputOutputPage", "FinishedPage")

        self.footerFrame.set_next_btn_command(self.onGo)

        titleFrame = ttk.Frame(contentFrame)
        self.standardLabel = ttk.Label(titleFrame, text="Standard", style='subtitle.TLabel', padding="0 0 10 10")
        self.normLabel = ttk.Label(titleFrame, text="N", style='subtitle.TLabel', padding="0 0 10 10")
        self.controlLabel = ttk.Label(titleFrame, text="C", style='subtitle.TLabel', padding="0 0 10 10")

        self.canvas = tk.Canvas(contentFrame, highlightthickness=0, background=styles.BG_COLOUR)
        self.scrollbar = ttk.Scrollbar(contentFrame, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.inner_canvas_frame = ttk.Frame(self.canvas)

        titleFrame.grid(       column=0, row=0, sticky=(W))

        # titleFrame children
        self.standardLabel.grid(    column=0, row=0, sticky=(W,E))
        self.normLabel.grid(        column=1, row=0, sticky=(W,E))
        self.controlLabel.grid(     column=2, row=0, sticky=(W,E))

        self.canvas.grid(   column=0, row=1, sticky=(N,S,E,W), columnspan=3)
        self.scrollbar.grid(column=3, row=1, sticky=(N,S,E))

        #Temp button
        normButton = Button(contentFrame, text="Norm", command=lambda: print(self.getNormalisingStandards()))
        controlButton = Button(contentFrame, text="Control", command=lambda: print(self.getControlStandards()))

        normButton.grid(column=0, row=2)
        controlButton.grid(column=1, row=2)

        self.canvas.create_window((0,0), window=self.inner_canvas_frame, anchor="nw",tags="self.inner_canvas_frame")
        self.inner_canvas_frame.bind("<Configure>", self.onFrameConfigure)

        #mousewheel bindings are platform dependant
        if sys.platform.startswith('linux'):
            self.bind_all("<Button-4>", self.onMouseWheel)
            self.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.bind_all("<MouseWheel>", self.onMouseWheel)


        self.standards = []
        self.isNormStrVars = []
        self.isControlStrVars = []

     def populateStandards(self, filepath):

        # set the width of columns in the canvas to match the width of columns outside the canvas
        self.inner_canvas_frame.columnconfigure(0, minsize=self.standardLabel.winfo_width())
        self.inner_canvas_frame.columnconfigure(1, minsize=self.normLabel.winfo_width())
        self.inner_canvas_frame.columnconfigure(2, minsize=self.controlLabel.winfo_width())

        # common.standard requires a list of filepaths
        filePathList = []
        filePathList.append(filepath)

        newStandards = []
        if self.controller.isUpb:
            newStandards = common.standard(UPb.getAllZircons(filePathList))
        else:
            newStandards = common.standard(TE.getAllZircons(filePathList))

        row = len(self.standards)
        for s in newStandards:
            if s not in self.standards:

                self.standards.append(s)
                standardNameLabel = ttk.Label(self.inner_canvas_frame, text=s, padding="10 0 10 0")

                isNorm = tk.StringVar(value="")
                isControl = tk.StringVar(value="")

                self.isNormStrVars.append(isNorm)
                self.isControlStrVars.append(isControl)

                isNormBtn = CustomCheckbutton(self.inner_canvas_frame, variable=isNorm, onvalue=s, offvalue="", padding="0 0 0 0")
                isControlBtn = CustomCheckbutton(self.inner_canvas_frame, variable=isControl, onvalue=s, offvalue="", padding="0 0 0 0")

                standardNameLabel.grid( column=0, row=row, sticky=(E))
                isNormBtn.grid(     column=1, row=row)
                isControlBtn.grid(  column=2, row=row)

                row+=1

        #use 'invisible' labels to align canvas content with the above titles
        # invisibleStandardLabel = ttk.Label(self.inner_canvas_frame, text="Standard", padding="0 0 10 10")
        # invisibleNormLabel = ttk.Label(self.inner_canvas_frame, text="Normalizing",  padding="0 0 10 10")
        # invisibleControlLabel = ttk.Label(self.inner_canvas_frame, text="Control",   padding="0 0 10 10")
        #
        # invisibleStandardLabel.grid( column=0, row=20, sticky=(E))
        # invisibleNormLabel.grid(     column=1, row=20, sticky=(E))
        # invisibleControlLabel.grid(  column=2, row=20, sticky=(E))

     def clearStandards(self):
         for widget in self.inner_canvas_frame.winfo_children():
             widget.destroy()
         self.standards.clear()
         self.isNormStrVars.clear()
         self.isControlStrVars.clear()

     def getNormalisingStandards(self):
         standards = []
         for strVar in self.isNormStrVars:
             if strVar.get() != "":
                 standards.append(strVar.get())

         return standards

     def getControlStandards(self):
         standards = []
         for strVar in self.isControlStrVars:
             if strVar.get() != "":
                 standards.append(strVar.get())

         return standards

    #enables scrolling from anywhere on the page
    #Note: yview_scroll's first parameter is platform dependant
    #Note: darwin = macOS
    #https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar
    #UnicodeDecodeError on MacOS: https://stackoverflow.com/questions/16995969/inertial-scrolling-in-mac-os-x-with-tkinter-and-python
     def onMouseWheel(self, event):
        if sys.platform.startswith('darwin'):
            self.canvas.yview_scroll(-1*(event.delta), "units")
        elif sys.platform.startswith('win'):
            self.canvas.yview_scroll(-1*(event.delta/120), "units")
        elif sys.platform.startswith('linux'):
            self.canvas.yview_scroll(-1*(event.delta/120), "units")

     def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

     def initialiseUPb(self):
         self.headerFrame.setTitle("3. Filter standards for UPb")

     def initialiseTE(self):
         self.headerFrame.setTitle("3. Filter standards for TE")

     def onGo(self, *event):
         control_standards = self.getControlStandards()
         normalising_standards = self.getNormalisingStandards()
         if self.controller.isUpb:
             UPb.UPb(control_standards, normalising_standards)
             self.footerFrame.goToNextPage()
         else:
             self.footerFrame.goToNextPage()
