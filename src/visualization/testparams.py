import tkinter as tk
from tkinter import ttk
from potentiostat import Potentiostat
from labelinput import LabelInput
import read_pot as rp

###################################################################
#############     Test Name and Current Range                   ###
#############     Potentiostat Parent Frame                     ###
###################################################################
class Test_(ttk.LabelFrame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ### Test Name ###
        self._test = tk.StringVar()
        self._test_name = LabelInput(
            self, 'Test Name', ttk.Combobox,
            input_args={'values': all_test_names},
            input_var=self._test)
        self._test_name.grid(row=0, column=0)

        

##################################################################
################# Common Test Parameters   #######################
##################################################################
class BasicParams_(Test_):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ### Current Range ###
        self._curr_range_value = tk.StringVar()
        self._curr_range = LabelInput(
            self, 'Current Range', ttk.Combobox,
            input_args={'values': all_curr_ranges},
            input_var=self._curr_range_value
            ).grid(row=1, column=0)

        ### quietTime ###
        self._qT_value = tk.IntVar()
        _quietTime = LabelInput(self, 'quietTime',
            input_var=self._qT_value
        ).grid(
            row=2, column=0)
        ### quietValue ###
        self._qV_value = tk.DoubleVar()
        _quietValue = LabelInput(self, 'quietValue',
            input_var=self._qV_value
        ).grid(row=3, column=0)
 
        ### Start Stop Test Button ###
        #_start_stop_btn = StartStop_(self).grid(
        #    row=5, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        
##################################################################
##################  Chronoamp Parameters Specific  ###############
##################  Frame ########################################
##################################################################
class Chronoamp_(BasicParams_):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ### duration ###
        self._duration_time = tk.IntVar()
        _duration = LabelInput(
            self, 'duration',
            input_var=self._duration_time).grid(row=4, column=0)

##################################################################
###############  Cyclic Voltametry Parameter  ####################
###############  Specific Frame  #################################
##################################################################
class CyclicVolt_(BasicParams_):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ### Maximum Value ###
        _max_value = LabelInput(
            self, 'max. Value',
            input_var=tk.StringVar()).grid(row=4, column=0)

##################################################################
####################  Start - Stop Test ##########################
##################################################################
class StartStop_(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.tvar = tk.StringVar()
        _start_stop_btn = ttk.Button(
            self, padding='5 5 5 5',
            textvariable=self.tvar,
            command=self.swap_state).grid(
                row= 0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
    
    def swap_state(self, **kwargs):
        p = Potentiostat('/dev/ttyACM0')

        if self.tvar.get() == 'Start Test Run':
            self.tvar.set('Stop Test Run')
            
            step = [[dt, qv],[dt, qv]]
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
        else:
            self.tvar.set('Start Test Run')
            p.stop_test()


#rp.read_pots()
p = Potentiostat('/dev/ttyACM0')
#all_test_names = pots[0].get_test_names()
all_test_names = p.get_test_names()
all_curr_ranges = p.get_all_curr_range()



