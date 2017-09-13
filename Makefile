PIP = virtual-python/bin/pip

# use this target to set up the virtual python for the project
virtual-python: requirements.txt
	virtualenv virtual-python
	$(PIP) install -q -r requirements.txt

# use this target enter an interactive python shell using the virtual python
ipython:
	virtual-python/bin/ipython

# start the main method in main.py
main:
	virtual-python/bin/python software_name/main.py
