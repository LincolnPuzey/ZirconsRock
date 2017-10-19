Zircons Rock
==========
Repository for Zircons Rock Data Processing Software

Project Requires Python 3.5 or later

## Instructions for WINDOWS

For help with running python programs on Windows, see:
https://docs.python.org/3.5/faq/windows.html

##### Installation
  * First ensure you have Python 3 version 3.5 or later installed
  * Install program files by either cloning this Github repository or unzipping 
    ZIP file containing repository to your installation location.
    We recommend using your home directory as the installation location so you
    have full permissions over the program files.
  * Run install_requirements.py script to install the program's requirements.

#### Running the program
  * To start the program run the python file zircons_rock.pyw (located in the directory zircons_rock).
  * To start with the program with the python shell visible run the python file zircons_rock_terminal.py
    (also located in the directory zircons_rock).


### Instructions for LINUX
To set up your dev environment and install the program you will need to have the following installed:
  * Python 3 (Version 3.5 or later)

Steps to set up:
  * install virtual python tool: `apt-get install python3-venv`
  * clone this git repo
  * change directory into local copy of repo: `cd ZirconsRock`
  * set up virtual python and install required libraries with: `make virtual_python`
  * change into program files: `cd zircons_rock`

Once set up you can call the main method of zircons_rock_terminal.py to start the program with

  `make zircons_rock`

You can also start an interactive python shell that uses the virtual python environment with

  `make ipython`
