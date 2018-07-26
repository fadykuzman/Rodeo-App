from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os
from potentiostat import Potentiostat
from functools import wraps

def not_connected(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        coms = func(*args, **kwargs)
        no_coms = len(coms)
        if no_coms == 0:
            'No Potentiostats Connected'
        else:
            return coms
    return wrapper

@not_connected
def fetch_coms():
    ls = os.listdir('/dev')
    coms = [p for p in ls if p.startswith('ttyACM')]
    return coms

def fetch_ports():
    coms = fetch_coms()
    pots = {}
    for c in coms:
        p = Potentiostat('/dev/{}'.format(c))
        if p not in pots:
            pots['pot{}'.format(p.get_device_id())] = p
    for k, p in pots.items():
        _pot_radio = ttk.Radiobutton(
            parent, text = p)
        _pot_radio.grid(
            row=0, column=1)

