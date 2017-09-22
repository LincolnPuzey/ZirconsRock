import subprocess

if __name__ == "__main__":
    print("Installing requirements...")
    completed = subprocess.run(
        ["pip", "install", "-r", "requirements.txt"],
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )
    print(completed.stdout)
    input("Press Enter to exit...")
