############################################
#  SKAN Sensor Potentiostat Interface App  #
############################################

import tkinter as tk
from tkinter import ttk
from time import time
import testparams
from read_pot import read_pots
from labelinput import LabelInput
from potentiostat import Potentiostat


################################################################
#################### Header Frame ##############################
################################################################
class Header_(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ### Date and Time ###
        _date = LabelInput(
            self, 'Date and Time', ttk.Label).grid(row=0, column=0)

        ### Time Count Down ###
        _timectdn = LabelInput(
            self, 'Time Count Down',
            ttk.Label).grid(row=0, column=2)

################################################################
#################### Parameters Frame ##########################
################################################################
class Parameters_(ttk.LabelFrame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        _px1 = testparams.Test_(self, text='Potx1')
        _px1.grid(row=0, column=0)
        self.test_name = _px1._test.get()
        if self.test_name == 'chronoamp':
            _px = testparams.Chronoamp_(
                self, text='Potx'
            )
            _px.grid(
                row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
            _px_btn = ttk.Button(self, text='Start Test Run',
            command=lambda: swap_state(
                dt=_px._duration_time.get(),
                qv=_px._qV_value.get(),
                qt=_px._qT_value.get(),
                test_name=_px._test.get()
                )
            )   
            _px_btn.grid(row=2, column=0)

        _py = testparams.CyclicVolt_(
            self, text='Poty'
        ).grid(
            row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))

################################################################
##################### Potentiostats Frame ######################
################################################################
class Potentiostats_(ttk.LabelFrame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._pots = {}
        #self._status = tk.BooleanVar()
        for row, (_id, _pot) in zip(
            range(len(pots)),enumerate(pots)):
            _pot_id = 'Pot{}'.format(_id)
            self._pots[_pot_id] = LabelInput(
                self, _pot_id, input_class=ttk.Checkbutton,
            ).grid(row=row, column=0)
        

        ### Button to Update available Potentiostats ###
        #_update_btn = ttk.Button(self, text='Update')
        #_update_btn.grid(row=4, column=0, sticky=(tk.W, tk.E))

pots = read_pots()
################################################################
##################### Graph Frame ##############################
################################################################
class Graph_(ttk.Frame):
     
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

################################################################
#################### Save Data Frame ###########################
################################################################
class SaveData_(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

################################################################
#################### Main Application ##########################
################################################################
class PotentiostatApplication(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Potentiostat App')
        self.geometry('900x600')

        #Header
        Header_(self).grid(
            row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        
        #Parameters
        Parameters_(self, text='Test Parameters').grid(
            row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        
        #Potentiostat
        Potentiostats_(
            self, text='Available Potentiostats').grid(
                row=1, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        
        #Graph
        Graph_(self).grid(
            row=2, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))

        self.columnconfigure(0, weight=1)
        

def swap_state(**kwargs):
        p = Potentiostat('/dev/ttyACM0')

        #if self.tvar.get() == 'Start Test Run':
        #    self.tvar.set('Stop Test Run')
        dt = kwargs.get('dt', 3000)
        qv = kwargs.get('qv', 0)
        qt = kwargs.get('qt', 0)
        test_name = kwargs.get('test_name', 'chronoamp')
        curr_range = kwargs.get('curr_range', '100uA')
        step = [[dt, qv],[dt,qv]]
        param = {
            'quietValue': qv,
            'quietTime': qt,
            'step':step
        }
        p.set_param(test_name, param)
        p.set_curr_range(curr_range)
        p.set_sample_rate(1)
        t, v, c = p.run_test(test_name, param=param, display='pbar')
        print(t, v, c)
        #else:
        #    self.tvar.set('Start Test Run')
        #    p.stop_test()
 
if __name__ == '__main__':
    _app = PotentiostatApplication()
    _app.mainloop()
