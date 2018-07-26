import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import skansensor as ss

raw_dropsense = ss.read_dropsense('./1811/Sense.MTA')
raw_picarro = ss.read_picarro('./1811/Picarro.dat')

data_fitted = ss.fit(raw_picarro, raw_dropsense)

def plot_two_graphs():
    fig, ax1 = plt.subplots()

    ax1.plot(data['time'], data['data_dropsense'], c='r')
    ax1.set_title('Dropsense vs Piccaro')
    ax1.set_xlabel('Time in seconds')
    ax1.set_ylabel('\xb5amp', color='r')
    ax1.tick_params('y', colors='r')

    ax2 = ax1.twinx()
    ax2.plot(data['time'], data['data_picarro'], c='b')
    ax2.set_ylabel('ppm', color='b')
    ax2.tick_params('y', colors='b')

    plt.show()

def plot_mamp_vs_ppm():
    quotiont = data_fitted['data_dropsense']/data_fitted['data_picarro']
    plt.plot(data_fitted['data_picarro'], quotiont)
    plt.show() 
