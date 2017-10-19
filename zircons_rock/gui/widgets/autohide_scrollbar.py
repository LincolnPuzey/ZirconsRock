from gui.resources import *

class AutoScrollbar(ttk.Scrollbar):
    """
    Extends the ttk.Scrollbar to hide itself when not needed

    Code from http://effbot.org/zone/tkinter-autoscrollbar.htm
    """

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        ttk.Scrollbar.set(self, lo, hi)


    def pack(self, **kw):
        raise TclError


    def place(self, **kw):
        raise TclError
