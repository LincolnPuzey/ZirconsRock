import sys

from gui.app import App

import data_processing.UPb as uranium_lead
import data_processing.TE as trace_elements


def main():
    app = App()

    if len(sys.argv) > 1:
        if sys.argv[1] == "te":
            trace_elements.te()
        elif sys.argv[1] == "upb":
            uranium_lead.UPb(['STDGJ', 'INT1'], ['INT2', 'MT'])
    else:
        # need the while loop to catch a UnicodeDecodeError that occurs when scrolling on macOS.
        # https://stackoverflow.com/questions/16995969/inertial-scrolling-in-mac-os-x-with-tkinter-and-python
        while True:
            try:
                app.mainloop()
                break
            except UnicodeDecodeError:
                pass


if __name__ == "__main__":
    main()
