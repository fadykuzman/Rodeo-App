from tkinter import *
from tkinter import ttk, filedialog, messagebox
import functions as f


if __name__ == "__main__":
    _root = Tk()
    _root.title('Potentiostat App')
    
    # Main Frame
    _mainframe = ttk.Frame(_root, padding=(5, 5, 5, 5))
    _mainframe.grid(row=0, column=0, sticky=(N, S, E, W))

        # Time Frame. Top Right.
        
        # variables frame. under time, left, 2/3 of right space, 1/4 of upper space
    _vars_frame = ttk.LabelFrame(
        _mainframe,
        text= 'Test Variables',
        padding=(5, 5, 5, 5))
    _vars_frame.grid(row=1, column=0, sticky=(N, S, W, E))     
        # Potentiostats frame
    _pot_frame = ttk.LabelFrame(
        _mainframe,
        text = 'Available Potentiostats',
        padding=(5, 5, 5, 5))
    
    _pot_frame.grid(row=1, column=1, sticky=(N, S))
    
            # List of Potentiostats
    _pot_list_frame = ttk.Frame(_pot_frame, padding=(5, 5, 5, 5))
    _pot_list_frame.grid(row=0, column=0, sticky=(N, S, W, E))
            # update Potentiostat list Button
    _pot_btn = ttk.Button(
        _pot_list_frame, text='Fetch Poties', command = f.fetch_ports)
    _pot_btn.grid(row=1, column=0, sticky=S, pady=5)
        #Graph frame
   
    # _pot_frame = ttk.LabelFrame(
    #    _mainframe, text='Available Potentiostats', padding = '9 0 0 0')
    #_pot_frame.grid(row=1, column=0, sticky=(E, W))
    #_pot_frame.columnconfigure(0, weight=1)
    #_pot_frame.rowconfigure(0, weight=1)

    #_pot = StringVar()
    #_pot.set('Potentiostats')
    #_pot_entry = ttk.Entry(
    #    _pot_frame, width=40, textvariable= _pot)
    #_pot_entry.grid(row=0, column=0, sticky=(E, W, S, N), padx=5)
    #_fetch_btn = ttk.Button(
    #   _pot_frame, text= 'Fetch Potentiostats', command= fetch_ports)
    #_fetch_btn.grid(row=0, column=1, sticky=W, padx=5)

    #_pot_radio_frame = ttk.Frame(_mainframe)
    #_pot_radio_frame.grid(row=2, column=0, sticky=(N,S))
    
    #_pot_choice_lbl = ttk.Label(
    #    _pot_radio_frame, text= "Choose the Potentiostats you want to use")
    #_pot_choice_lbl.grid(row=0, column=0, padx=5, pady=5)

