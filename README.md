CITS3200
==========
Repository for CITS3200 Project

Project Requires Python 3.5 or later

### Setting up dev environment on LINUX
To set up your dev environment you will need to have the following installed:
  * Python 3 (Version 3.5 or later)

Steps to set up:
  * install virtual python tool: `apt-get install python3-venv`
  * clone this git repo
  * change into repo: `cd CITS3200`
  * set up virtual python and install required libraries with: `make virtual-python`

Once set up you can start an interactive python shell that uses the virtual python with

  `make ipython`
  
Or you call the main method of main.py with

  `make main`
