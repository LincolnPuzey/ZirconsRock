import os

# Use this file to declare any 'hard-coded' values that are used in the program.
# Use ALL_CAPS_AND_UNDERSCORES for variable names
# Then import them into whatever part of the program they are needed in.

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
INPUT_DIR = CUR_DIR + '/../test_files/inputs'
OUTPUT_DIR = CUR_DIR + '/../test_files/outputs'

# Variables used in TE.py:
BeginningCell = "Element"  # cell where program begins reading
EndingCell = ""  # cell where program ends reading
SheetName = "TrElem"
allChondriteElements = ['La139', 'Ce140', 'Pr141', 'Nd146', 'Sm147', 'Eu151', 'Gd157', 'Th232', 'Dy163', 'Y89', 'Ho165',
                        'Er166', 'U238', 'Yb173', 'Lu175', 'Hf178', 'Nb93', 'Ta181', 'Ti49', 'P31', 'Tb159', 'Tm169']
ChondriteValues = [0.237, 0.613, 0.0928, 0.457, 0.148, 0.0563, 0.199, 0.0294, 0.246, 1.57, 0.0546, 0.16, 0.0074, 0.161,
                   0.0246, 0.103, 0.24, 0.0136, 440, 1080, 0.0361, 0.0247]

# colors and markers used for line graphs
LINE_COLORS = [
    '#CC3300',  # dark red
    '#558000',  # dark green
    '#00FF99',  # aqua green
    '#00B3B3',  # dark aqua
    '#E6E600',  # dark yellow
    '#0066CC',  # blue
    '#6600FF',  # blue-purple
    '#B800E6',  # purple
    '#FF0080',  # pink
    '#661A00',  # brown
    '#000000',  # black
    '#FF6600',  # orange
    '#FF1A1A',  # red
]
LINE_MARKERS = [
    'square',
    'diamond',
    'x',
    'circle',
    'triangle',
    'plus',
    'star',
]
# colors and markers used for scatterplots and convex hulls for each class of CART1
CLASSES = [
    "Carbonite",
    "Granitoid(>5% SiO2)",
    "Granitoid (70-75% SiO2)",
    "Granitoid (>65% SiO2)",
    "Syenite",
    "Kimberlite",
    "Ne-syenite&Syenite Pegmatites",
    "Syenite/Monzonite",
    "Dolerite",
    "Basalt"
]
CLASS_COLORS = {
    CLASSES[0]: '#CC3300',  # dark red
    CLASSES[1]: '#669900',  # dark green
    CLASSES[2]: '#00CC66',  # aqua green
    CLASSES[3]: '#00B3B3',  # dark aqua
    CLASSES[4]: '#E6E600',  # dark yellow
    CLASSES[5]: '#0066CC',  # blue
    CLASSES[6]: '#6600FF',  # blue-purple
    CLASSES[7]: '#B800E6',  # purple
    CLASSES[8]: '#B30059',  # dark pink
    CLASSES[9]: '#661A00',  # brown
}
CLASS_MARKERS = {
    CLASSES[0]: {'type': 'square',    'size': 7, 'border': {'color': CLASS_COLORS.get(CLASSES[0], '#000000')}, 'fill': {'color': CLASS_COLORS.get(CLASSES[0], '#000000')}},
    CLASSES[1]: {'type': 'diamond',   'size': 7, 'border': {'color': CLASS_COLORS.get(CLASSES[1], '#000000')}, 'fill': {'color': CLASS_COLORS.get(CLASSES[1], '#000000')}},
    CLASSES[2]: {'type': 'diamond',   'size': 7, 'border': {'color': CLASS_COLORS.get(CLASSES[2], '#000000')}, 'fill': {'color': CLASS_COLORS.get(CLASSES[2], '#000000')}},
    CLASSES[3]: {'type': 'diamond',   'size': 7, 'border': {'color': CLASS_COLORS.get(CLASSES[3], '#000000')}, 'fill': {'color': CLASS_COLORS.get(CLASSES[3], '#000000')}},
    CLASSES[4]: {'type': 'x',         'size': 7, 'border': {'color': CLASS_COLORS.get(CLASSES[4], '#000000')}, },
    CLASSES[5]: {'type': 'circle',    'size': 7, 'border': {'color': CLASS_COLORS.get(CLASSES[5], '#000000')}, 'fill': {'color': CLASS_COLORS.get(CLASSES[5], '#000000')}},
    CLASSES[6]: {'type': 'triangle',  'size': 7, 'border': {'color': CLASS_COLORS.get(CLASSES[6], '#000000')}, 'fill': {'color': CLASS_COLORS.get(CLASSES[6], '#000000')}},
    CLASSES[7]: {'type': 'plus',      'size': 7, 'border': {'color': CLASS_COLORS.get(CLASSES[7], '#000000')}, },
    CLASSES[8]: {'type': 'star',      'size': 7, 'border': {'color': CLASS_COLORS.get(CLASSES[8], '#000000')}, },
    CLASSES[9]: {'type': 'long_dash', 'size': 7, 'border': {'color': CLASS_COLORS.get(CLASSES[9], '#000000')}, 'fill': {'color': CLASS_COLORS.get(CLASSES[9], '#000000')}},
}
# Used for generating charts and convex hull images
CHART_WIDTH = 1100
CHART_HEIGHT = 660
# expressed as percentages of CHART_WIDTH and CHART_HEIGHT
PLOT_X_OFFSET = 0.1
PLOT_Y_OFFSET = 0.07
PLOT_WIDTH = 0.65
PLOT_HEIGHT = 0.8
# where to store convex hull image file
CONVEX_HULL_IMAGE_DIR = "convex_hull"
CONVEX_HULL_IMAGE_FILE = "{}_convexhull.png"

# File path for chondrite_values.csv
CHONDRITE_FILE = INPUT_DIR + '/chondrite_values.csv'

# Filepaths for pickled objects
GUI_TEMPS_DIR = './gui/temps'
UPB_INPUT_FILEPATHS = GUI_TEMPS_DIR + '/upb_input_filepaths.pkl'
UPB_OUTPUT_FILEPATH = GUI_TEMPS_DIR + '/upb_output_filepath.pkl'
UPB_OUTPUT_FILENAME = GUI_TEMPS_DIR + '/upb_output_filename.pkl'
UPB_OUTPUT_DIR = GUI_TEMPS_DIR + '/upb_output_dir.pkl'
TE_INPUT_FILEPATHS = GUI_TEMPS_DIR + '/te_input_filepaths.pkl'
TE_OUTPUT_FILEPATH = GUI_TEMPS_DIR + '/te_output_filepath.pkl'
TE_OUTPUT_FILENAME = GUI_TEMPS_DIR + '/te_output_filename.pkl'
TE_OUTPUT_DIR = GUI_TEMPS_DIR + '/te_output_dir.pkl'

UPB_NORMALISING = GUI_TEMPS_DIR + '/upb_normalising.pkl'
UPB_CONTROLS = GUI_TEMPS_DIR + '/upb_controls.pkl'
UPB_UNKNOWNS = GUI_TEMPS_DIR + '/upb_unknown.pkl'

TE_CONTROLS = GUI_TEMPS_DIR + '/te_controls.pkl'
TE_UNKNOWNS = GUI_TEMPS_DIR + '/te_unknown.pkl'

MIN_WINDOW_WIDTH = 400
MIN_WINDOW_HEIGHT = 400
INITIAL_WINDOW_WIDTH = 450
INITIAL_WINDOW_HEIGHT = 500

# # Temporary: List of TE input filepaths for testing
# TEMP_TE_INPUT_FILEPATHS = [INPUT_DIR + '/Dec04_RUN1_TE.csv',
#                       INPUT_DIR + '/Dec04_RUN2_TE.csv',
#                       INPUT_DIR + '/Dec04_RUN3_TE.csv',
#                       INPUT_DIR + '/Dec04_RUN4_TE.csv']
#
# # Temporary: List of UPb input filepaths for testing
# TEMP_UPB_INPUT_FILEPATHS = [INPUT_DIR + '/Dec04_RUN1_UPb.csv',
#                        INPUT_DIR + '/Dec04_RUN2_UPb.csv',
#                        INPUT_DIR + '/Dec04_RUN3_UPb.csv',
#                        INPUT_DIR + '/Dec04_RUN4_UPb.csv']
#
# # Temporary: TE output filepath for testing
# TEMP_TE_OUTPUT_FILEPATH = OUTPUT_DIR + '/test_te_output.xlsx'
#
# # Temporary: UPb output filepath for testing
# TEMP_UPB_OUTPUT_FILEPATH = OUTPUT_DIR + '/test_upb_output.xlsx'
#
# # Temporary: List of normalising and control standards for testing
# TEMP_NORMALISING_STANDARDS = ['INT2', 'INT1']
# TEMP_CONTROL_STANDARDS =['STDGJ', '91500','MT']
