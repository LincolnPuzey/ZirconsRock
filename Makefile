# Makefile for linux installation/setup

PIP = virtual_python/bin/pip

# use this target to set up the virtual python for the project
virtual_python: requirements.txt
	python3 -m venv ./virtual_python
	$(PIP) install -q -r requirements.txt

