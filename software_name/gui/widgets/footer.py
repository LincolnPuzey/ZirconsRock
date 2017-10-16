from gui.resources import *


class Footer(ttk.Frame):
    """Template for creating back and next buttons on each page"""

    def __init__(self, parent, controller, show_buttons, prev_button_name, next_button_name, prev_page_name, next_page_name):
        """
        Initialises a frame with a back button and next button.
        Frame is gridded to row 2 of the parent frame.
        """

        ttk.Frame.__init__(self, parent, style="bg.TFrame")
        self.controller = controller
        self.next_page_name = next_page_name
        self.prev_page_name = prev_page_name

        if show_buttons:
            self.prev_button = Button(self, text=prev_button_name, command=self.go_to_prev_page)
            self.next_button = Button(self, text=next_button_name, command=self.go_to_next_page)

            self.grid(            column=0, row=2, sticky=E)
            self.prev_button.grid(column=0, row=0, sticky=W)
            self.next_button.grid(column=1, row=0, sticky=E)

        parent.parent.bind("<Right>", self.go_to_next_page)
        parent.parent.bind("<Left>", self.go_to_prev_page)


    # need *event to accept extra parameter from key bindings
    def go_to_prev_page(self, *event):
        """Displays the page called prev_page_name"""

        self.controller.show_frame(self.prev_page_name)


    def go_to_next_page(self, *event):
        """Displays the page called next_page_name"""

        self.controller.show_frame(self.next_page_name)


    def set_prev_page(self, page_name):
        """Sets the page to display when the back button is pressed"""

        self.prev_page_name = page_name


    def set_next_page(self, page_name):
        """Sets the page to display when the next button is pressed"""

        self.next_page_name = page_name


    def set_next_btn_command(self, new_command):
        """Assigns a custom command to the next button"""

        self.next_button.config(command=new_command)


    def set_prev_btn_command(self, new_command):
        """Assigns a custom command to the back button"""

        self.prev_button.config(command=new_command)
