# Dependencies
from time import sleep
from threading import Thread
import sys

# Custom thread
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is None:
            return

        self._return = self._target()

    def join(self, *args):
        Thread.join(self, *args)
        return self._return

# Colours
class colours:
    '''Colors class:reset all colors with colors.reset; two
    sub classes fg for foreground
    and bg for background; use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
    underline, reverse, strike through,
    and invisible work with the main class i.e. colors.bold'''
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
 
    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
 
    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

# Suspense print
def s_print(text: str, delay: float = 1, regularDelay: float = 0.05, reset=True):
    # Loop through each character
    for character in text:
        # Matches a suspense character
        if (character in [".", "!", "?"]):
            sleep(delay)
        else:
            sleep(regularDelay)

        # Print
        print(character, end="", flush=True)
    sleep(delay)

    # New line + reset
    print(colours.reset if reset else "")


# Time limited input
def time_input(text: str, timeout: float = 2):
    # Get user response
    print(text, flush=True)
    response = ThreadWithReturnValue(target=sys.stdin.readline)
    response.start()
    inp = response.join(timeout)

    # Return
    return None if (inp is None) else inp.strip()