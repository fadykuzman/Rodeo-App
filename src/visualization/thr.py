from threading import Thread
from datetime import datetime
from potentiostat import Potentiostat
import read_pot as rp


pots = rp.read_pots()

for k, p in pots.items():
    print('{} starts at {}'.format(k, datetime.now()))
    thread1 = Thread(target=rp.chronoamperometry, args=(p,))
    thread1.start()
    print('{} ends at {}'.format(k, datetime.now()))

