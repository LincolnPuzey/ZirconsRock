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

# File path for chondrite_values.csv
CHONDRITE_FILE = INPUT_DIR + '/chondrite_values.csv'

# Temporary: List of TE input filepaths for testing
TE_INPUT_FILEPATHS = [INPUT_DIR + '/Dec04_RUN1_TE.csv',
                      INPUT_DIR + '/Dec04_RUN2_TE.csv',
                      INPUT_DIR + '/Dec04_RUN3_TE.csv',
                      INPUT_DIR + '/Dec04_RUN4_TE.csv']

# Temporary: List of UPb input filepaths for testing
UPB_INPUT_FILEPATHS = [INPUT_DIR + '/Dec04_RUN1_UPb.csv',
                       INPUT_DIR + '/Dec04_RUN2_UPb.csv',
                       INPUT_DIR + '/Dec04_RUN3_UPb.csv',
                       INPUT_DIR + '/Dec04_RUN4_UPb.csv']

# Temporary: TE output filepath for testing
TE_OUTPUT_FILEPATH = OUTPUT_DIR + '/test_te_output.xlsx'

# Temporary: UPb output filepath for testing
UPB_OUTPUT_FILEPATH = OUTPUT_DIR + '/test_upb_output.xlsx'

# Temporary: List of normalising and control standards for testing
NORMALISING_STANDARDS = ['INT2', 'INT1']
CONTROL_STANDARDS =['STDGJ', '91500','MT'] 
