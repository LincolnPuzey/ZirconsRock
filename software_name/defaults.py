import os

# Use this file to declare any 'hard-coded' values that are used in the program.
# Use ALL_CAPS_AND_UNDERSCORES for variable names
# Then import them into whatever part of the program they are needed in. eg:

SOME_VALUE = 10

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
INPUT_DIR = CUR_DIR + '/../test_files/inputs'
OUTPUT_DIR = CUR_DIR + '/../test_files/outputs'

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
NORMALISING_STANDARDS = ['STDGJ', '91500']
CONTROL_STANDARDS = ['MT','INT1']

# then in another file:
# from defaults import SOME_VALUE
