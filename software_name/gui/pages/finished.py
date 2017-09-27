from gui.resources import *


class FinishedPage(ttk.Frame):

     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        contentFrame = Content(self, controller)
        footerFrame = Footer(self, controller, False, "","", "FilterStandardsPage", "FinishedPage")

        doneLabel = ttk.Label(contentFrame, text="Done.", font=controller.bigFont)


        outInfoFrame = ttk.Frame(contentFrame)
        nameTitleLabel = ttk.Label(outInfoFrame, text="Name of results: ", font=controller.mediumFont)
        #use a StringVar so the Label updates when the user changes the file name
        outNameStr = controller.frames[self.get_input_output_page()].output_filename
        nameLabel = ttk.Label(outInfoFrame, textvariable=outNameStr, font=controller.mediumFont)
        locationLabel = ttk.Label(outInfoFrame, text="Location of results: ", font=controller.mediumFont)
        #use a StringVar so the Label updates when the user changes the file path
        outDirStr = controller.frames[self.get_input_output_page()].output_dir
        outPathLabel = ttk.Label(outInfoFrame, textvariable=outDirStr, font=controller.mediumFont)

        openButton = Button(contentFrame, text="Open", command=lambda: self.open())
        showInFolderButton = Button(contentFrame, text="Show in folder", command=lambda: self.showInFolder())
        startAgainButton = Button(contentFrame, text="Start again", command=lambda: controller.show_frame("StartPage"))
        backButton = Button(contentFrame, text="Back", command=lambda: controller.show_frame("LoadingPage"))

        #contentFrame children
        doneLabel.grid(         column=0, row=0, sticky=(W))
        outInfoFrame.grid(      column=0, row=2, sticky=(W))
        openButton.grid(        column=0, row=3, sticky=(W))
        showInFolderButton.grid(column=0, row=4, sticky=(W))
        startAgainButton.grid(  column=0, row=5, sticky=(W))
        backButton.grid(        column=0, row=6, sticky=(W))

        #outInfoFrame children
        nameTitleLabel.grid(    column=0, row=0, sticky=(W))
        nameLabel.grid(         column=1, row=0, sticky=(W))
        locationLabel.grid(     column=0, row=1, sticky=(W))
        outPathLabel.grid(      column=1, row=1, sticky=(W))

     # https://stackoverflow.com/questions/13078071/start-another-program-from-python-separately
     def open(self):
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
        input_output_page = self.get_input_output_page()

        dir_path = self.controller.frames[input_output_page].output_dir.get()

        try:
            if sys.platform.startswith("win"):
                os.startfile(dirPath)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(["open", dir_path])
            else:
                subprocess.Popen(["xdg-open", dir_path])
        except:
            pass

     def get_input_output_page(self):
         if self.controller.isUpb:
             return "UPbInputOutputPage"
         else:
             return "TEInputOutputPage"
