from gui.app import App


def main():
    print("This program comes with ABSOLUTELY NO WARRANTY")
    print("This is free software, and you are welcome to redistribute it under the terms of the GNU GPL:")
    print("    https://www.gnu.org/licenses/gpl-3.0.en.html")

    app = App()
    while True:
        try:
            app.mainloop()
            break
        except UnicodeDecodeError:
            pass


if __name__ == "__main__":
    main()
