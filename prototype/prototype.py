# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# http://www.tkdocs.com/tutorial/widgets.html
# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html

#padding=(left top right bottom)

import os

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

from tkinter import N
from tkinter import S
from tkinter import E
from tkinter import W

from tkinter import PhotoImage

from tkinter import filedialog

from tkinter import StringVar


#inheriting from ttk makes 'SampleApp' the root window
class SampleApp(tk.Tk):

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
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (DemoStartPage, PageOne, PageTwo, StartPage,
                  FilterStandardsPage, ConfigureStandardsPage, NameStandardsPage,
                  InputOutputPage, LoadingPage, FinishedPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''

        #----Method 1----
        #Keep all frames THEN raise the target frame
        frame = self.frames[page_name]
        frame.tkraise()

        #----Method 2----
        #Remove all frames THEN draw the target frame
    #    for frame in self.frames.values():
    #        frame.grid_remove()
    #    frame = self.frames[page_name]
    #    frame.grid()

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
        subtitle = ttk.Label(self, text=subtitle_txt, font=controller.smallFont).grid(column=0, row=1, sticky=(W))


class Content(ttk.Frame):

     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        #position below the Header
        self.grid(column=0, row=1, sticky=(W,E))

class Footer(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid(column=0, row=2, sticky=(W,E))


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
        uraniumButton.grid(column=0, row=1)
        orLabel.grid(column=2, row=1)
        traceButton.grid(column=3, row=1)

    def onPressUpb(self):
        self.controller.isUpb = True
        print(self.controller.isUpb)
        self.controller.show_frame("FilterStandardsPage")

    def onPressTE(self):
        self.controller.isUpb = False
        print(self.controller.isUpb)
        self.controller.show_frame("FilterStandardsPage")



class FilterStandardsPage(ttk.Frame):

     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        headerFrame = Header(self, controller, "2. Filter standards for " + self.controller.getProcessName(), "")
        contentFrame = Content(self, controller)
        footerFrame = Footer(self, controller)

        includeAllButton = ttk.Button(contentFrame, text="Include all standards")

        orLabel1 = ttk.Label(contentFrame, text="or")
        orLabel2 = ttk.Label(contentFrame, text="or")
        orLabel3 = ttk.Label(contentFrame, text="or")

        includeAllButton.grid(column=0, row=0, sticky=(W,E))
        orLabel1.grid(column=1, row=0)
        orLabel2.grid(column=2, row=0)
        orLabel3.grid(column=3, row=0)

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

        backButton = ttk.Button(footerFrame, text="Back", command=lambda: controller.show_frame("FilterStandardsPage"))
        continueButton = ttk.Button(footerFrame, text="Continue", command=lambda: controller.show_frame("InputOutputPage"))
        backButton.grid(column=0, row=0, sticky=(W))
        continueButton.grid(column=1,row=0, sticky=(E))


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
        inputList = tk.Listbox(contentFrame, listvariable=self.inFilePathStr, height=5)
        openButton = ttk.Button(contentFrame, text="Open", command=self.addInputFile)
        outputLabel = ttk.Label(contentFrame, text="Output location")
        outputList = tk.Listbox(contentFrame, listvariable=self.outFilePathStr, height=1)
        chooseButton = ttk.Button(contentFrame, text="Choose", command=self.setOutputPath)

        inputLabel.grid(column=0, row=0, sticky=(E))
        inputList.grid(column=0, row=1, sticky=(W,E))
        openButton.grid(column=0, row=2, sticky=(E))
        outputLabel.grid(column=0, row=3, sticky=(W))
        outputList.grid(column=0, row=4, sticky=(W,E))
        chooseButton.grid(column=0, row=5, sticky=(E))

        backButton = ttk.Button(footerFrame, text="Back", command=lambda: controller.show_frame("ConfigureStandardsPage"))
        goButton = ttk.Button(footerFrame, text="Go", command=lambda: controller.show_frame("LoadingPage"))
        backButton.grid(column=0, row=0, sticky=(W))
        goButton.grid(column=1,row=0, sticky=(E))

     def addInputFile(self):
         newPath = filedialog.askopenfilename()
         self.inFilePathList.append(newPath)
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



#-------------------Begin tutorial stuff--------------------------

class DemoStartPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="This is the start page", font=controller.bigFont)
        label.pack(side="top", fill="x", pady=10)

        button1 = ttk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = ttk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class PageOne(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="This is page 1", font=controller.bigFont)
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("DemoStartPage"))
        button.pack()


class PageTwo(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="This is page 2", font=controller.bigFont)
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("DemoStartPage"))
        button.pack()

#----------------------End tutorial stuff-----------------------------

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
