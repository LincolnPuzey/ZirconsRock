import pip


def install_requirements():
    print("Installing requirements...")
    try:
        import pip
        pip.main(['install', '-r', 'requirements.txt'])

        print("Success")
        input("Press Enter to exit...")
    except Exception as e:
        print("Exception:")
        print(str(e))
        input("Press Enter to exit...")


if __name__ == "__main__":
    install_requirements()
