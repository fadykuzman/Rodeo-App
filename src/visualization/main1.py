import tkinter as tk
from tkinter import ttk
from threading import Thread
import matplotlib
#matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2TkAgg)
from labelinput import LabelInput
from potentiostat import Potentiostat
from readpot import read_pot as rp

class TestForm(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.inputs = {}
        self.pots = {}
        self.parameter_pot = {}
        self.reset()

        ### Parameters Main Frame ###
        params_input = tk.LabelFrame(
            self, text='Test Parameters')
        
        ### Potentiostats List ###
        self.pots_list = tk.LabelFrame(self,
            text='Potentiostats List')
          
        for i, (_id, _p) in zip(
            range(len(pots)), pots.items()):
            pot_name = ttk.Label(self.pots_list,
                text='{}'.format(_id))
            pot_name.grid(row=i, column=0, padx=5, pady=5)
        self.pots_list.grid(row=1, column=1, padx=5)
        
        ps = [p for k, p in pots.items()]
        ### Test Choice Frame ###
        self.test_param = tk.Frame(params_input)
            
        self.inputs['test_name'] = LabelInput(
            self.test_param, 'Test Name',
            ttk.Combobox, input_var=tk.StringVar(),
            input_args={
                'values':ps[0].get_test_names(),
                'width': 10})
        self.inputs['test_name'].grid(
            row=0, column=0, columnspan=2, pady=5)
        self.test_param.grid(row=0, column=0, padx=5, pady=5)

        ### Common Parameters Frame ###
        self.common_params = tk.Frame(params_input)
        self.inputs['curr_range'] = LabelInput(
            self.common_params, 'Current Range',
            ttk.Combobox, input_var=tk.StringVar(),
            input_args={
                'values': ps[0].get_all_curr_range(),
                'width': 7})
        self.inputs['curr_range'].grid(
            row=0, column=0, columnspan=2, pady=5)
        self.inputs['output_volt'] = LabelInput(
            self.common_params, 'Output Voltage',
            ttk.Combobox, input_var=tk.StringVar(),
            input_args={
                'values': ps[0].get_all_volt_range(),
                'width': 7})
        self.inputs['output_volt'].grid(
            row=1, column=0, columnspan=2, pady=5)
        self.common_params.grid(
            row=1, column=0, padx=5, pady=5) 

        ### Specific Parameters Frame ###
        self.specific_params = tk.LabelFrame(params_input,
            text='Quiet Phase')
        self.inputs['quietTime'] = LabelInput(
            self.specific_params, 'quietTime (ms)',
            tk.Spinbox, input_var=tk.IntVar(),
            input_args={'from_': 0, 'to':'infinity', 'increment':1,
                        'width': 7})
        self.inputs['quietTime'].grid(
            row=0, column=0, padx=5, pady=5)
        self.inputs['quietValue'] = LabelInput(
            self.specific_params, 'quietValue (V)',
            tk.Spinbox, input_var=tk.DoubleVar(),
            input_args={'from_':0.0, 'to': 10.0, 'increment': .001,
                        'width': 7})
        self.inputs['quietValue'].grid(
            row=1, column=0, padx=5, pady=5)
        self.specific_params.grid(
            row=2, column=0, padx=5, pady=5)
       
        ### Duration and Sample Rate Frame ###
        self.d_s_rate_frame = tk.LabelFrame(params_input,
            text='Duration and Sample Rate')
        self.inputs['run_duration'] = LabelInput(
            self.d_s_rate_frame, 'Run Duration (ms)',
            input_args={'width': 7},
            input_var=tk.IntVar()) 
        self.inputs['run_duration'].grid(
            row=0, column=0, padx=5, pady=5)
        self.inputs['sample_rate'] = LabelInput(
            self.d_s_rate_frame, 'Sample Rate (/s)',
            input_args={'width': 7},
            input_var=tk.IntVar())
        self.inputs['sample_rate'].grid(
            row=1, column=0, columnspan=2, padx=5, pady=5)
        self.d_s_rate_frame.grid(
            row=1, column=1, padx=5, pady=5)

        ### Steps Values and Duration ###
        self.steps_frame = tk.LabelFrame(params_input,
            text='Steps')
            ### Step 1 Frame ###
        self.step1_frame = tk.LabelFrame(self.steps_frame,
            text='Step 1')
        self.inputs['step1_volt'] = LabelInput(self.step1_frame,
           'Volt (V)', input_args={'width': 7},
            input_var=tk.DoubleVar())
        self.inputs['step1_volt'].grid(
            row=0, column=0, padx=5, pady=5)
        self.inputs['step1_duration'] = LabelInput(self.step1_frame,
            'Duration (ms)', input_args={'width': 7},
            input_var=tk.IntVar())
        self.inputs['step1_duration'].grid(
            row=1, column=0, padx=5, pady=5)
        self.step1_frame.grid(
            row=0, column=0, padx=5, pady=5)
            ### Step 2 Frame ###
        self.step2_frame = tk.LabelFrame(self.steps_frame,
            text='Step 2')
        self.inputs['step2_volt'] = LabelInput(self.step2_frame,
            'Volt (V)', input_args={'width': 7},
            input_var=tk.DoubleVar())
        self.inputs['step2_volt'].grid(
            row=0, column=0, padx=5, pady=5)
        self.inputs['step2_duration'] = LabelInput(self.step2_frame,
            'Duration (ms)', input_args={'width': 7},
            input_var=tk.IntVar())
        self.inputs['step2_duration'].grid(
            row=1, column=0, padx=5, pady=5)
        self.step2_frame.grid(
            row=0, column=1, padx=5, pady=5)
        self.steps_frame.grid(
            row=2, column=1, columnspan=2, padx=5, pady=5)

        ### Electrode Frame ###
        self.electrode_frame = tk.LabelFrame(params_input,
           text='Electrode / Electrolyte')
        self.inputs['electrode'] = LabelInput(
            self.electrode_frame, 'Type',
            input_var=tk.StringVar())
        self.inputs['electrode'].grid(
             row=0, column=2, padx=5, pady=5)
        self.electrode_frame.grid(
             row=1, column=2, padx=5, pady=5)

        ### Start Stop Button Frame ###
        self.strt_stp = tk.Frame(self)
        
        self.strt_btn = ttk.Button(
            self.strt_stp, text='Start Run',
            command=self.start_run)
        self.strt_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.stop_btn = ttk.Button(
            self.strt_stp, text='Stop Run', 
            command=self.stop_run)
        self.stop_btn.grid(row=0, column=1, padx=5, pady=5)
       
        self.strt_stp.grid(row=2, column=0)

        params_input.grid(
            row=1, column=0, pady=5, 
            sticky=(tk.W, tk.E, tk.N, tk.S))

        ### Graphing Frame ###
        

    def start_run(self):
        for k, p in pots.items():
            thread = Thread(target=rp.chronoamperometry,
                args=(p,),
                kwargs={
                    'test_name': self.get()['test_name'], 
                    'curr_range': self.get()['curr_range'],
                    'out_volt_range': self.get()['output_volt'],
                    'sample_rate': self.get()['sample_rate'],
                    'quietTime': self.get()['quietTime'],
                    'quietValue': self.get()['quietValue'],
                    'step1_volt': self.get()['step1_volt'],
                    'step1_duration': self.get()['step1_duration'],
                    'step2_volt': self.get()['step2_volt'],
                    'step2_duration': self.get()['step2_duration'],
                    'run_duration': self.get()['run_duration'],
                    'electrode': self.get()['electrode']
                })
            thread.start()
 
    def stop_run(self):
        for k, p in pots.items():
            thread = Thread(target=p.stop_test)
            thread.start() 

    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    def reset(self):
        for widget in self.inputs.values():
            widget.set('')

class YieldChartView(tk.Frame):
    
    def __init__(self, parent, x_axis, y_axis, title):
        super().__init__(parent)
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.toolbar = navigationToolbar2TkAgg(self.canvas, self)
        self.canvas.get_tk_widget().grid()
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes.set_xlabel(x_axis)
        self.axes.set_ylabel(y_label)
        self.axes.set_title(title)
        self.lines = []
        self.line_labels = []

    def draw_line(self, data, color, label):
        x, y = zip(*data)
        line = self.axes.plot(x, y, c=color, label=label)
        self.lines.append(line)
        self.line_labels.append(label)
        self.axes.legend(self.lines, self.line_labels)


class MainApplication(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Rodeo Potentiostat App')
        #self.resizable(width=False, height=False)
        ttk.Label(self, text='SKAN Rodeo Potentiostat Application',
            font=('TkDefault', 16)).grid(row=0)
        self.testform = {}
        
        if len(pots) == 0:
            ttk.Label(self, text='No Potentiostats are available'
            ).grid(row=1)
            refresh_form = ttk.Button(self, text='Refresh',
                command=self.update)
            refresh_form.grid(row=2)
        #for i, (_id, p) in zip(range(len(pots)), pots.items()):
        self.testform = TestForm(self)
        self.testform.grid(
            row=1, column=0, padx=10, pady=10)
        
        #popup = tk.Toplevel()
        #chart = YieldChartView(popup,
            

pots = rp.read_pots()

if __name__ == '__main__':
    mainapp = MainApplication()
    mainapp.mainloop()
