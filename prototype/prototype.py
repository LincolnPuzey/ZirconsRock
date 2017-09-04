# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# http://www.tkdocs.com/tutorial/widgets.html
# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html
# https://stackoverflow.com/questions/16840660/scroll-a-group-of-widgets-in-tkinter


#padding=(left top right bottom)

import os
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import StringVar

# For sticky geometry
from tkinter import N
from tkinter import S
from tkinter import E
from tkinter import W

# For listBoxes
from tkinter import SINGLE
from tkinter import EXTENDED

# For scrollbars
from tkinter import VERTICAL
from tkinter import HORIZONTAL

# For images
from tkinter import PhotoImage

# For file I/O
from tkinter import filedialog



#inheriting from ttk makes 'SampleApp' the root window
class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        #initialising the base ttk class
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("CITS3200 Prototype")

        #determines U-Pb or TE processing was selected
        self.isUpb = True

        self.bigFont = tkfont.Font(family='Helvetica', size=28)
        self.mediumFont = tkfont.Font(family='Helvetica', size=20)
        self.smallFont = tkfont.Font(family='Helvetica', size=14)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = ttk.Frame(self, padding="20 20 20 20")
        container.grid(column=0, row=0, sticky=(N, W, E, S))

        container.rowconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)
        container.rowconfigure(2, weight=1)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.columnconfigure(2, weight=1)

        self.frames = {}
        for F in (StartPage, FilterStandardsPage, ConfigureStandardsPage,
                    NameStandardsPage, InputOutputPage, LoadingPage,
                    FinishedPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            print("boo")
            frame.grid(row=0, column=0, sticky="nsew")
            print("boo2")
        print("Boo3")
        self.show_frame("StartPage")
        print("boo4")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''

        #----Method 1----
        #Keep all frames THEN raise the target frame
        frame = self.frames[page_name]
        frame.tkraise()

        #----Method 2----
        #Remove all frames THEN draw the target frame
        # for frame in self.frames.values():
        #     frame.grid_remove()
        # frame = self.frames[page_name]
        # frame.grid()

    #returns either 'U-Pb' or 'TE'
    def getProcessName(self):
        if self.isUpb:
            return 'U-Pb'
        return 'TE'

class Header(ttk.Frame):

    def __init__(self, parent, controller, title_txt, subtitle_txt):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        #position at top of page
        self.grid(column=0, row=0, sticky=(W,E))

        title = ttk.Label(self, text=title_txt, font=controller.bigFont).grid(column=0, row=0, sticky=(W))
        if len(subtitle_txt) > 0:
            subtitle = ttk.Label(self, text=subtitle_txt, font=controller.smallFont).grid(column=0, row=1, sticky=(W))

        print(self.controller.isUpb)
        print(self.controller.getProcessName())

class Content(ttk.Frame):

     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, padding="0 25 0 25")
        self.controller = controller

        #position below the Header
        self.grid(column=0, row=1, sticky=(W,E))

class Footer(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid(column=0, row=2, sticky=(E))

class StartPage(ttk.Frame):

    def __init__(self, parent, controller):
        #initialising the base Frame class
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        #distinguishes between the frame's header and the frame's content
        headerFrame = Header(self, controller, "1. Select a process", "")
        contentFrame = Content(self, controller)
        footerFrame = Footer(self, controller)

        #can use GIF, PPM/PGP - http://effbot.org/tkinterbook/photoimage.html
        uraniumImg = PhotoImage(file='placeholder.gif')
        traceImg = PhotoImage(file='placeholder.gif')

        #define buttons
        uraniumButton = ttk.Button(contentFrame, text="U-Pb", image=uraniumImg, compound="top",
                                   command=self.onPressUpb,
                                   padding="5 20 5 20")
        traceButton = ttk.Button(contentFrame, text="Trace Element", image=traceImg, compound="top",
                                 command=self.onPressTE,
                                 padding="5 20 5 20")

        #need to maintain references to images like this
        #http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        uraniumButton.image = uraniumImg
        traceButton.image = traceImg

        orLabel = ttk.Label(contentFrame, text="or", font=controller.smallFont, padding="5 0 5 0")

        #draw widgets
        uraniumButton.grid( column=0, row=1)
        orLabel.grid(       column=1, row=1)
        traceButton.grid(   column=2, row=1)



    def onPressUpb(self):
        self.controller.isUpb = True
        print(self.controller.isUpb)
        self.controller.show_frame("FilterStandardsPage")

    def onPressTE(self):
        self.controller.isUpb = False
        print(self.controller.isUpb)
        self.controller.show_frame("FilterStandardsPage")

# https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter/3092341#3092341
class TableFrame(tk.Frame):
    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(parent, width=200, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.grid(column=1, row=1, sticky=(W,E,N,S))
        # self.vsb.pack(side="right", fill="y")
        self.canvas.grid(column=0, row=1, sticky=(W,E,N))
        # self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        # self.populate()

    def populate(self):
        '''Put in some fake data'''
        for row in range(100):
            tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1",
                     relief="solid").grid(row=row, column=0)
            t="this is the second column for row %s" %row
            tk.Label(self.frame, text=t).grid(row=row, column=1)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class TableOfEntries(ttk.Frame):

    def __init__(self, parent, controller, title, numRows):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        titleLabel = ttk.Label(self, text=title)

        # IMPORTANT: using a TEXT widget as a FRAME to enable scrolling across a group of widgets
        # see 'Images and widgets': http://www.tkdocs.com/tutorial/text.html#images
        # see answer: https://stackoverflow.com/questions/16840660/scroll-a-group-of-widgets-in-tkinter
        self.tableFrame = tk.Text(self, height=5, width=10)
        self.scrollBar = ttk.Scrollbar(self, orient=VERTICAL, command=self.tableFrame.yview)
        self.tableFrame.configure(yscrollcommand=self.scrollBar.set)

        self.entryList = []
        self.addButton = ttk.Button(self, text="Add 5 lines", command=lambda: self.addRows(5))

        titleLabel.grid(        column=0, row=0)
        self.tableFrame.grid(   column=0, row=1, sticky=(W,E,N,S))
        self.scrollBar.grid(    column=1, row=1, sticky=(W,E,N,S))


        self.addRows(numRows)
        self.addButton.grid(    column=0, row=2, sticky=(W,E))


    # Adds num rows to the table
    def addRows(self, num):
        for i in range(num):
            entry = ttk.Entry(self.tableFrame)
            self.entryList.append(entry)
            #add entry widget to the tableFrame (text widget)
            self.tableFrame.window_create(str(i+1.0), window=entry)
            self.tableFrame.configure(height=20)
            entry.grid(column=0, row=len(self.entryList), sticky=(W,E,N,S))
            entry.bind("<Up>", self.goToPreviousEntry)
            entry.bind("<Shift-Return>", self.goToPreviousEntry)
            entry.bind("<Down>", self.goToNextEntry)
            entry.bind("<Return>", self.goToNextEntry)


    # https://stackoverflow.com/questions/6687108/how-to-set-the-tab-order-in-a-tkinter-application
    def goToPreviousEntry(self, event):
        widget = event.widget
        tcl_obj = self.tk.call('tk_focusPrev', widget._w)
        prevWidget = self.nametowidget(tcl_obj.string)
        if isinstance(prevWidget, ttk.Entry):
            prevWidget.focus()

    # https://stackoverflow.com/questions/6687108/how-to-set-the-tab-order-in-a-tkinter-application
    def goToNextEntry(self, event):
        widget = event.widget
        tcl_obj = self.tk.call('tk_focusNext', widget._w)
        nextWidget = self.nametowidget(tcl_obj.string)
        if isinstance(nextWidget, ttk.Entry):
            nextWidget.focus()


class FilterStandardsPage(ttk.Frame):

     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        headerFrame = Header(self, controller, "2. Filter standards for " + self.controller.getProcessName(), "")
        contentFrame = Content(self, controller)
        footerFrame = Footer(self, controller)

        includeAllTable = TableOfEntries(contentFrame, controller, "Include all standards", 0)
        includeOnlyTable = TableOfEntries(contentFrame, controller, "Only include these standards", 10)
        excludeTable = TableOfEntries(contentFrame, controller, "Exclude these standards", 10)

        orLabel1 = ttk.Label(contentFrame, text="or")
        orLabel2 = ttk.Label(contentFrame, text="or")
        orLabel3 = ttk.Label(contentFrame, text="or")

        includeAllTable.grid(       column=0, row=0, sticky=(N))
        orLabel1.grid(              column=1, row=0)
        includeOnlyTable.grid(      column=2, row=0, sticky=(N))
        orLabel2.grid(              column=3, row=0)
        excludeTable.grid(          column=4, row=0, sticky=(N))

        backButton = ttk.Button(footerFrame, text="Back", command=lambda: controller.show_frame("StartPage"))
        continueButton = ttk.Button(footerFrame, text="Continue", command=lambda: controller.show_frame("ConfigureStandardsPage"))
        backButton.grid(column=0, row=0, sticky=(W))
        continueButton.grid(column=1,row=0, sticky=(E))


class ConfigureStandardsPage(ttk.Frame):

     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        headerFrame = Header(self, controller, "3. Configure standards for " + self.controller.getProcessName(),
                        "Select 'Custom standards' to create aliases for standards.")
        contentFrame = Content(self, controller)
        footerFrame = Footer(self, controller)

        defaultFrame = ttk.Frame(contentFrame)
        customFrame = ttk.Frame(contentFrame)

        defaultLabel = ttk.Label(defaultFrame, text="Default standards")
        defaultInfoLabel = ttk.Label(defaultFrame, text="(Leave the names of standards unchanged)")
        customLabel = ttk.Label(customFrame, text="Custom standards")
        customInfoLabel = ttk.Label(customFrame, text="(Create aliases for some standards)")
        createButton = ttk.Button(customFrame, text="Create new configuration", command=lambda: print("Create new configuration"))
        openButton = ttk.Button(customFrame, text="Open existing configuration", command=self.setOutputPath)

        homeDir = os.path.expanduser('~/')
        self.filePathStr = StringVar(value=homeDir)
        self.filePath = tk.Listbox(customFrame, listvariable=self.filePathStr, selectmode=SINGLE, height=1, relief="ridge")

        orLabel = ttk.Label(contentFrame, text="or")

        defaultFrame.grid(      column=0, row=0, sticky=(W,E))
        defaultLabel.grid(      column=0, row=0, sticky=(W))
        defaultInfoLabel.grid(  column=1, row=0, sticky=(W))
        orLabel.grid(           column=0, row=1)
        customFrame.grid(       column=0, row=2, sticky=(W,E))
        customLabel.grid(       column=0, row=0, sticky=(W))
        customInfoLabel.grid(   column=1, row=0, sticky=(W))
        createButton.grid(      column=0, row=1, sticky=(W,E))
        openButton.grid(        column=1, row=1, sticky=(W,E))
        self.filePath.grid(          column=0, row=2, sticky=(W,E), columnspan=2)

        backButton = ttk.Button(footerFrame, text="Back", command=lambda: controller.show_frame("FilterStandardsPage"))
        continueButton = ttk.Button(footerFrame, text="Continue", command=lambda: controller.show_frame("InputOutputPage"))
        backButton.grid(column=0, row=0, sticky=(W))
        continueButton.grid(column=1,row=0, sticky=(E))

     def setOutputPath(self):
         newPath = filedialog.askdirectory()
         self.filePathStr.set(newPath)

class NameStandardsPage(ttk.Frame):

     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        headerFrame = Header(self, controller, "Create a new naming convention", "")
        contentFrame = Content(self, controller)


class InputOutputPage(ttk.Frame):

     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.inFilePathList = []
        self.inFilePathStr = StringVar(value=self.inFilePathList)

        #desktopDir = os.path.join(os.environ["HOMEPATH"], "Desktop")
        homeDir = os.path.expanduser('~/')
        self.outFilePathStr = StringVar(value=homeDir)

        headerFrame = Header(self, controller, "4. Input / Output for " + self.controller.getProcessName(), "")
        contentFrame = Content(self, controller)
        footerFrame = Footer(self, controller)

        inputLabel = ttk.Label(contentFrame, text="Input files (Glitter csv) (drag and drop / open)")

        inputListFrame = ttk.Frame(contentFrame)
        self.inputList = tk.Listbox(inputListFrame, listvariable=self.inFilePathStr, selectmode=EXTENDED, height=5, relief="ridge")
        scrollBar = ttk.Scrollbar(inputListFrame, orient=VERTICAL, command=self.inputList.yview)
        self.inputList.configure(yscrollcommand=scrollBar.set)

        inputButtonFrame = ttk.Frame(contentFrame)
        removeButton = ttk.Button(inputButtonFrame, text="Remove", command=self.removeSelectedInputFiles)
        openButton = ttk.Button(inputButtonFrame, text="Open", command=self.addInputFile)

        outputLabel = ttk.Label(contentFrame, text="Output location")
        self.outputList = tk.Listbox(contentFrame, listvariable=self.outFilePathStr, selectmode=SINGLE, height=1, relief="ridge")
        chooseButton = ttk.Button(contentFrame, text="Choose", command=self.setOutputPath)

        inputLabel.grid(        column=0, row=0, sticky=(W))
        inputListFrame.grid(    column=0, row=1, sticky=(W,E))
        self.inputList.grid(    column=0, row=0, sticky=(W,E))
        scrollBar.grid(    column=1, row=0, sticky=(N,S,E))

        inputButtonFrame.grid(  column=0, row=2, sticky=(E))
        removeButton.grid(      column=0, row=0, sticky=(E))
        openButton.grid(        column=1, row=0, sticky=(E))

        outputLabel.grid(       column=0, row=3, sticky=(W))
        self.outputList.grid(   column=0, row=4, sticky=(W,E))
        chooseButton.grid(      column=0, row=5, sticky=(E))

        backButton = ttk.Button(footerFrame, text="Back", command=lambda: controller.show_frame("ConfigureStandardsPage"))
        goButton = ttk.Button(footerFrame, text="Go", command=lambda: controller.show_frame("LoadingPage"))

        backButton.grid(        column=0, row=0, sticky=(E))
        goButton.grid(          column=1, row=0, sticky=(E))

        contentFrame.columnconfigure(0, weight=1)
        inputListFrame.columnconfigure(0, weight=1)
        contentFrame.rowconfigure(1, weight=1)

        #remove input files by selecting items and pressing the backspace button
        self.inputList.bind("<BackSpace>", self.removeSelectedInputFiles)

     def addInputFile(self):
         paths = filedialog.askopenfilenames()  #paths is a tuple of filenames
         pathList = self.controller.tk.splitlist(paths) #split the tuple into a list
         for path in pathList:
             if path not in self.inFilePathList:
                 self.inFilePathList.append(path)
         #update the listBox
         self.inFilePathStr.set(self.inFilePathList)

     # gui button press: passes 1 argument
     # bound backspace press: passes 2 arguments
     # use *event to accept 1 or 2 parameters
     def removeSelectedInputFiles(self, *event):
         selection = self.inputList.curselection()
         for index in selection:
             #remove the selected filePath from the filePathList
             self.inFilePathList.remove(self.inputList.get(index))
         #update the listBox
         self.inFilePathStr.set(self.inFilePathList)

     def setOutputPath(self):
         newPath = filedialog.askdirectory()
         self.outFilePathStr.set(newPath)



class LoadingPage(ttk.Frame):

     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        contentFrame = Content(self, controller)
        footerFrame = Footer(self, controller)

        processingLabel = ttk.Label(contentFrame, text="Processing")
        progressBar = ttk.Progressbar(contentFrame, orient=HORIZONTAL, length=200, mode='determinate')
        infoLabel = ttk.Label(contentFrame, text="Description of current task")

        processingLabel.grid(column=0, row=0, sticky=(W,E,N,S))
        progressBar.grid(column=0, row=2, sticky=(W,E,N,S))
        infoLabel.grid(column=0, row=3, sticky=(W,E,N,S))


        backButton = ttk.Button(footerFrame, text="Back", command=lambda: controller.show_frame("InputOutputPage"))
        continueButton = ttk.Button(footerFrame, text="Continue", command=lambda: controller.show_frame("FinishedPage"))
        backButton.grid(column=0, row=0, sticky=(W))
        continueButton.grid(column=1,row=0, sticky=(E))


class FinishedPage(ttk.Frame):

     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        contentFrame = Content(self, controller)

        doneLabel = ttk.Label(contentFrame, text="Done.", font=controller.bigFont)
        locationLabel = ttk.Label(contentFrame, text="Location of results: C://user/documents/...", font=controller.mediumFont)
        showInFolderButton = ttk.Button(contentFrame, text="Show in folder")
        startAgainButton = ttk.Button(contentFrame, text="Start again", command=lambda: controller.show_frame("StartPage"))


        doneLabel.grid(column=0, row=0, sticky=(W))
        locationLabel.grid(column=0, row=1, sticky=(W))
        showInFolderButton.grid(column=0, row=2, sticky=(W))
        startAgainButton.grid(column=0,row=3, sticky=(W))

        backButton = ttk.Button(contentFrame, text="Back", command=lambda: controller.show_frame("LoadingPage"))
        backButton.grid(column=0, row=4, sticky=(W))


if __name__ == "__main__":
    app = App()
    app.mainloop()
