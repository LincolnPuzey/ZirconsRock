from gui.resources import *


class Footer(ttk.Frame):

    def __init__(self, parent, controller, showButtons, prevButtonName, nextButtonName, prevPageName, nextPageName):
        ttk.Frame.__init__(self, parent, style="bg.TFrame")
        self.controller = controller
        self.nextPageName = nextPageName
        self.prevPageName = prevPageName

        if showButtons:
            self.prevButton = Button(self, text=prevButtonName, command=self.goToPrevPage)
            self.nextButton = Button(self, text=nextButtonName, command=self.goToNextPage)

            self.grid(          column=0, row=2, sticky=(E))
            self.prevButton.grid(    column=0, row=0, sticky=(W))
            self.nextButton.grid(    column=1, row=0, sticky=(E))

        parent.parent.bind("<Right>", self.goToNextPage)
        parent.parent.bind("<Left>", self.goToPrevPage)

    #need *event to accept extra parameter from key bindings
    def goToPrevPage(self, *event):
        self.controller.show_frame(self.prevPageName)

    def goToNextPage(self, *event):
        self.controller.show_frame(self.nextPageName)

    def set_prev_page(self, page_name):
        self.prevPageName = page_name

    def set_next_page(self, page_name):
        self.nextPageName = page_name

    def set_next_btn_command(self, new_command):
        self.nextButton.config(command=new_command)

    def set_prev_btn_command(self, new_command):
        self.prevButton.config(command=new_command)
