
def install_requirements():
    print("Installing requirements...")
    try:
        import pip
        pip.main(['install', '-r', 'requirements.txt'])
        print("Success")
        input("Press Enter to exit...")
    except Exception as e:
        print("Could not import pip. Do you have Python 3.5 or later?")
        print("Exception:")
        print(str(e))
        input("Press Enter to exit...")


if __name__ == "__main__":
    install_requirements()
