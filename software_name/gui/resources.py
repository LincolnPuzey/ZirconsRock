#padding=(left top right bottom)

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import StringVar

# For sticky geometry
from tkinter import N
from tkinter import S
from tkinter import E
from tkinter import W
from tkinter import CENTER

# For listBoxes
from tkinter import SINGLE
from tkinter import EXTENDED

# For scrollbars
from tkinter import VERTICAL
from tkinter import HORIZONTAL

# For images
from tkinter import PhotoImage

# For file I/O
from tkinter import filedialog
import subprocess
import platform

# For text widget
from tkinter import INSERT

import gui.styles as styles

from gui.widgets.button import Button
from gui.widgets.checkbutton import CustomCheckbutton
from gui.widgets.header import Header
from gui.widgets.content import Content
from gui.widgets.footer import Footer

from gui.pages.start import StartPage
from gui.pages.filter_standards import FilterStandardsPage
from gui.pages.input_output import InputOutputPage
from gui.pages.loading import LoadingPage
from gui.pages.finished import FinishedPage
