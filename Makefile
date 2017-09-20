PIP = virtual_python/bin/pip

# use this target to set up the virtual python for the project
virtual_python: requirements.txt
	python3 -m venv ./virtual_python
	$(PIP) install -q -r requirements.txt

# use this target enter an interactive python shell using the virtual python
ipython:
	virtual_python/bin/ipython

# start the main method in main.py
main:
	virtual_python/bin/python software_name/main.py
