import os, sys, logging, errno, ast, psutil
from ConfigParser import SafeConfigParser

# Parse config file
parser = SafeConfigParser()
parser.read('../config_EPIC.txt')

###############################################################################
# Constants
#
#
###############################################################################
SKIP = 10
SKIP_SCN = 14

###############################################################################
# User modifiable values
#
#
###############################################################################
SOIL          = 'ssurgo' # Should be same as SSURGO python code
SLLIST        = parser.get('PARAMETERS','SLLIST')
PROJECT_NAME  = parser.get('PROJECT','project_name')
TAG           = parser.get('PROJECT','OUT_TAG')
START_YR      = parser.getint('GET_OUTPUT','START_YR')
END_YR        = parser.getint('GET_OUTPUT','END_YR')
ACN_PARAMS    = ast.literal_eval(parser.get('GET_OUTPUT','ACN_PARAMS'))
ACM_PARAMS    = ast.literal_eval(parser.get('GET_OUTPUT','ACM_PARAMS'))
ACY_PARAMS    = ast.literal_eval(parser.get('GET_OUTPUT','ACY_PARAMS'))
DGN_PARAMS    = ast.literal_eval(parser.get('GET_OUTPUT','DGN_PARAMS'))
ATG_PARAMS    = ast.literal_eval(parser.get('GET_OUTPUT','ATG_PARAMS'))
ANN_PARAMS    = ast.literal_eval(parser.get('GET_OUTPUT','ANN_PARAMS'))
SCN_PARAMS    = ast.literal_eval(parser.get('GET_OUTPUT','SCN_PARAMS'))
GET_PARAMS    = ast.literal_eval(parser.get('RUN_EPIC','EPICOUT_FLS'))
EXTR_YRS      = ast.literal_eval(parser.get('GET_OUTPUT','EXTR_YRS'))
DO_FOLDER     = parser.getboolean('PROJECT','DO_FOLDER')
FOLDER_PATH   = parser.get('PROJECT','FOLDER_PATH')
dominant      = parser.get('PARAMETERS','dominant')

OUT_TAG   = parser.get('PROJECT', 'OUT_TAG')
base_dir  = parser.get('PATHS','base_dir') + os.sep
epic_dir  = base_dir + os.sep + 'EPIC' + os.sep + PROJECT_NAME + os.sep
sims_dir  = epic_dir + os.sep + 'simulations' # Stores simulations
anly_dir  = epic_dir + os.sep + 'analysis' + os.sep + TAG + os.sep
db_dir    = anly_dir + os.sep + 'databases' # Store sqlite databases
csv_dir   = anly_dir + os.sep + 'csvs' # Store EPIC output csvs
gis_dir   = anly_dir + os.sep + 'gis' # Store gis analysis
sgo_dir   = parser.get('PATHS', 'out_dir') + os.sep + parser.get('PROJECT', 'project_name') + os.sep + 'Data' + os.sep +\
            SOIL + os.sep
IPCC_FILE = parser.get('POST_PROCESS', 'GIS_DIR') + os.sep + parser.get('POST_PROCESS', 'IPCC_carbon_2000_path') + os.sep \
            + parser.get('POST_PROCESS', 'IPCC_carbon_2000_file')
zone_data = parser.get('POST_PROCESS', 'GIS_DIR') + os.sep + parser.get('POST_PROCESS', 'zone_data')

# Maximum number of cpus to use at a time
max_threads = psutil.cpu_count() - 1

###############################################################################
#
#
#
###############################################################################
def make_dir_if_missing(d):
    try:
        os.makedirs(d)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

# Create directories
make_dir_if_missing(epic_dir)
make_dir_if_missing(anly_dir)
make_dir_if_missing(db_dir)
make_dir_if_missing(csv_dir)
make_dir_if_missing(gis_dir)

# Logging
LOG_FILENAME   = epic_dir+os.sep+'Log_Read_'+TAG+'.txt'
logging.basicConfig(filename = LOG_FILENAME, level=logging.INFO,\
                    format='%(asctime)s    %(levelname)s %(module)s - %(funcName)s: %(message)s',\
                    datefmt="%Y-%m-%d %H:%M:%S") # Logging levels are DEBUG, INFO, WARNING, ERROR, and CRITICAL
  