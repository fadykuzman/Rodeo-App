import read_pot as rp
import numpy as np

np_range_list = list(np.arange(-0.047, 0.053, 0.0001))
volt_range_list = list(map(lambda x: round(x, 4), np_range_list))

pots = rp.read_pots()

for _id, p in pots.items():
    if _id == 'pot2':
        curr_range = p.get_all_curr_range()
        for curr in curr_range:
            for v in volt_range_list:
                if curr == '1uA':
                    v = v
                elif curr == '10uA':
                    v *= 10
                elif curr == '100uA':
                    v *= 100
                elif curr == '1000uA':
                    v *= 1000
                rp.chronoamperometry(p,
                    step1_volt=v,
                    step1_duration=2000, 
                    curr_range=curr, 
                    electrode='2.2kOhm',
                    sample_rate=4,
                    run_duration=2000,
                    filename='./calibration.csv')
