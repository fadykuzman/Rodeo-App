from potentiostat import Potentiostat
from time import time
import os
import pandas as pd

def read_pots():
    devlist = os.listdir('/dev')

    coms = [c for c in devlist if c.startswith('ttyACM')]

    pots = {}
    for c in coms:
        p = Potentiostat('/dev/{}'.format(c))
        _id = p.get_device_id()
        if p not in pots:
            pots['pot{}'.format(_id)] = p
    return pots

pots = read_pots()

def chronoamperometry(p, **params):

    duration_min = params.get('duration', 1)    
    quietValue = params.get('quietValue', 0.05)
    quietTime = params.get('quietTime', 0) 
    duration = 60 * 1000 * duration_min
    step = [[duration, quietValue],[duration, quietValue]]
    curr_range = params.get('curr_range','100uA')
    test_name = params.get('test_name', 'chronoamp')

    param = {
     'quietValue': quietValue,
     'quietTime': quietTime,
     'step': step
        }

### Setting Parameters ###
    p.set_param(test_name, param)
    p.set_curr_range(curr_range)
    p.set_sample_rate(params.get('sample_rate',1))

    t, v, c = p.run_test(test_name, display='pbar')
    
    d = {
        'time': t,
        'voltage': v,
        'current': c,
        'quietValue': quietValue,
        'quietTime': quietTime,
        'duration': duration,
        'curr_range': curr_range,
        'test_name': test_name,
        'potentio_id': p.get_device_id(),
        'electrode': params.get('electrode', None)
         }
 
    df = pd.DataFrame(d)
    try:
        df.to_csv('./data_chronoamp.csv',mode='a', header=False)
    except:
        df.to_csv('./data_chronoamp.csv')

def cyclic_voltammetry(p, **params):
    # getting Parameters
    quietValue = params.get('quietValue', 0)
    quietTime = params.get('quietTime', 0)
    minVolt = params.get('minVolt', -0.2)
    maxVolt = params.get('maxVolt', 1)
    scanRate = params.get('scanRate', 0.1)
    numCycles = params.get('numCycles', 10)
    shift = params.get('shift', 0.0)
    curr_range = params.get('curr_range', '100uA')
    test_name = params.get('test_name', 'cyclic')
  
    amplitude = 0.5 * ((maxVolt) - (minVolt))
    offset = 0.5 * ((maxVolt) + (minVolt))
    period = int(4 * params.get('periodfactor', 1000) * amplitude / scanRate)

    param = {
        'quietValue': quietValue,
        'quietTime': quietTime,
        'amplitude': amplitude,
        'offset': offset,
        'period': period,
        'numCycles': numCycles,
        'shift': shift
        }

    # setting parameters
    p.set_param(test_name, param)
    p.set_curr_range(curr_range)
    p.set_sample_rate(10)
    # running
    t, v, c = p.run_test(test_name)
    print('Time {0}, Voltage {1}, Current {2}'
          .format(t, v, c)) 
    d = {
        'time': t,
        'voltage': v,
        'current': c,
        'quietValue': quietValue,
        'quietTime': quietTime,
        'amplitude': amplitude,
        'offset': offset,
        'period': period,
        'numCycles': numCycles,
        'shift': shift,
        'test_name': test_name,
        'potentio_id': p.get_device_id(),
        'electrode': params.get('electrode', None)
         }
    df = pd.DataFrame(d)
    try:
        df.to_csv('./data_cv.csv',mode='a', header=False)
    except:
        df.to_csv('./data_cv.csv')


#def export_data()
