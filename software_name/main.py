from gui.app import App

def main():
    app = App()
    #need the while loop to catch a UnicodeDecodeError that occurs when scrolling on macOS.
    #https://stackoverflow.com/questions/16995969/inertial-scrolling-in-mac-os-x-with-tkinter-and-python
    while True:
        try:
            app.mainloop()
            break
        except UnicodeDecodeError:
            print("Uh-oh. Tkinter doesn't like scrolling on macOS.")
            pass

if __name__ == "__main__":
    main()
