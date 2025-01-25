COLOR_RED = "#FF0000"
COLOR_BLACK = "#000000"
COLOR_WHITE = "#FFFFFF"
COLOR_GREEN = "#008000"
COLOR_UPDATED = "#DC6601" 
COLOR_RT_BG = "#E0E0FF"
COLOR_DT_BG = "#F0F0F0"
COLOR_CS_BG = "#E7FFF7"
COLOR_WW_BG = "#FFFdE7"
COLOR_PU_BG = "#FFFFE0"

IMG_SIZE = (25, 25)

POP_WIDTH = 350
POP_HEIGHT = 300
SAVE_WIDTH = 500
SAVE_HEIGHT = 400
LOGIN_WIDTH = 400
LOGIN_HEIGHT = 300
MAIN_WINDOW_WIDTH = 1300
MAIN_WINDOW_HEIGHT = 800
HELP_WIDTH = 800
HELP_HEIGHT = 650
PARALLEL_OFFSET = 13
STATE_RADIUS = 30

RUN_PAUSES_MS = 600

EMPTY_SETUP = "State: ???"

# Logger
LOG_DIR = 'logs'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
ERROR_LOG = "error_log.log"
OTHER_LOG = "app_log.log"

from enum import Enum
class AppMode(Enum):
    RUNNING = 0
    DRAWING = 1
    FINISHED = 2