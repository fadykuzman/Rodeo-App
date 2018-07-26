from potentiostat import Potentiostat
import read_pot as rp

def run_test(e1=None, e2=None):
    pots = rp.read_pots()

    for key, p in pots.items():
        if key == 'pot1': 
           initiate_test(p, e1)
        elif key == 'pot2':
           initiate_test(p, e2)

def initiate_test(p, e):
    rp.chronoamperometry(
        p,
        duration = 1,
        electrode=e)
    rp.cyclic_voltammetry(p, electrode=e)

