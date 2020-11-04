from pathlib import Path
import matplotlib
class Colors:
    RESET = '\033[0m'
    DARK = '\033[30m'
    RESET_FOREGROUND = '\033[39m'
    RESET_BACKGROUND = '\033[49m'

    class Backgrounds:
        YELLOW = '\033[43m'
        WHITE = '\033[47m'
        RED = '\033[41m'
        GREEN = '\033[42m'
        BLUE = '\033[44m'
        MAGENTA = '\033[45m'
        CYAN = '\033[46m'

class Symbols:
    HOR = '─'
    VER = '│'
    RTOP = '┐'
    RBOT = '┘'

COLORS = [Colors.Backgrounds.RED, Colors.Backgrounds.GREEN, Colors.Backgrounds.YELLOW, Colors.Backgrounds.BLUE, Colors.Backgrounds.MAGENTA, Colors.Backgrounds.CYAN]

DIRS = {'DATA': '../data/', 'IMG': '../img/'}
for d in DIRS.values():
    Path(d).mkdir(parents=True, exist_ok=True)

columns = ['#Generation','Best genome','Best fitness','Mean fitness']

# Execution parameters

NUM_EXECUTIONS = 10

matplotlib.rc('xtick', labelsize=14) 
matplotlib.rc('ytick', labelsize=14) 
matplotlib.rc('font', size=14) 
matplotlib.rc('axes', labelsize=14) 
matplotlib.rc('lines', linewidth=3) 
