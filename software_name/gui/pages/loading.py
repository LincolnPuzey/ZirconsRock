from gui.resources import *

class LoadingPage(ttk.Frame):

     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        contentFrame = Content(self, controller)
        footerFrame = Footer(self, controller, True, "Back", "Continue", "FilterStandardsPage", "FinishedPage")

        processingLabel = ttk.Label(contentFrame, text="Processing")
        progressBar = ttk.Progressbar(contentFrame, orient=HORIZONTAL, length=200, mode='determinate')
        infoLabel = ttk.Label(contentFrame, text="Description of current task")

        processingLabel.grid(   column=0, row=0, sticky=(W,E,N,S))
        progressBar.grid(       column=0, row=2, sticky=(W,E,N,S))
        infoLabel.grid(         column=0, row=3, sticky=(W,E,N,S))
