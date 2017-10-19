import sys

from gui.app import App

import data_processing.UPb as uranium_lead
import data_processing.TE as trace_elements


def main():
    app = App()
    while True:
        try:
            app.mainloop()
            break
        except UnicodeDecodeError:
            pass


if __name__ == "__main__":
    main()
