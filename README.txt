CITS3200
==========
Repository for CITS3200 Project

Project Requires Python 3.5 or later

## Instructions for WINDOWS

##### Installation
  * First ensure you have Python 3 version 3.5 or later installed
  * Install program files by either cloning this Github repository or unzipping 
    provided ZIP file to your installation location. We recommend using your home
    directory as the installation location so you have full permissions over the 
    program files.
  * Run install_requirements.py script to install the program's requirements.

#### Running the program
  * To start the program run the python file main.py (located in the directory software_name).


### Instructions for LINUX
To set up your dev environment you will need to have the following installed:
  * Python 3 (Version 3.5 or later)

Steps to set up:
  * install virtual python tool: `apt-get install python3-venv`
  * clone this git repo
  * change into program files: `cd CITS3200`
  * set up virtual python and install required libraries with: `make virtual-python`
  * change into program files: `cd software_name`

Once set up you can start an interactive python shell that uses the virtual python with

  `make ipython`
  
Or you call the main method of main.py to start the program with

  `make main`
