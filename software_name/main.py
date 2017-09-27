import sys

from gui.app import App

import data_processing.UPb as upb
import data_processing.TE as te

def main():
    app = App()
    #need the while loop to catch a UnicodeDecodeError that occurs when scrolling on macOS.
    #https://stackoverflow.com/questions/16995969/inertial-scrolling-in-mac-os-x-with-tkinter-and-python

    if len(sys.argv) > 1:
        if sys.argv[1] == "te":
            te.te()
        elif sys.argv[1] == "upb":
            upb.UPb(['STDGJ','INT1'],['INT2','MT'])
    else:
        while True:
            try:
                app.mainloop()
                break
            except UnicodeDecodeError:
                print("Uh-oh. Tkinter doesn't like scrolling on macOS.")
                pass


if __name__ == "__main__":
    main()
