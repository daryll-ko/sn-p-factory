from functools import partial
import colorama
from termcolor import colored

colorama.init()

tblue = partial(colored, color="blue")
tcyan = partial(colored, color="cyan")
tgreen = partial(colored, color="green")
tred = partial(colored, color="red")
tyellow = partial(colored, color="yellow")
