import sys
import numpy as np
from matplotlib import legend
import pandas as pd
import glob
import matplotlib.pyplot as plt

colors = {0: '#FF4242', 1: '#235FA4', 2: '#6FDE6E', 'cwwm': '#E8F086',
          'analog': '#0A284B', 'reference': '#A691AE', 3: '#0A284B'}
color_r = {5: '#FF4242', 6: '#235FA4', 7: '#6FDE6E', 8: '#E8F086',
           9: '#0A284B', 10: '#A691AE'}
markers = {0: 'x', 1: 'x', 2: 'x', 'cwwm': 'o',
           'analog': 'd', 'reference': 'D'}
e_bounds = {0: '1.0000E-05', 1: '1.0000E-01', 2: '2.0000E+01', 3: 'total'}
ratios = [5, 6, 7, 8, 9, 10]
dpi = 600
lw = .9  # line width for plots
cs = 5  # error bar cap size
n_sigma = 3


def plot_fsize(df):
    # plot total file size
    plt.figure()
    title = 'File Size'
    xlabel = 'Decimation Factor'
    ylabel = 'Total File Size (MB)'

    plt.plot(df.loc[df['group'] == 'total']['dc factor'],
             df.loc[df['group'] == 'total']['size'],
             linestyle='', marker='d', color=colors[0])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()

    save_name = 'fsize_decimated.png'
    plt.savefig(save_name)
    # eventually need to add line for WWINP file size!!


def plot_average_coarseness(df):
    # just plot averages for each decimation factor
    plt.figure()
    title = 'Average Coarseness'
    xlabel = 'Decimation Factor'
    ylabel = 'Triangle Density'

    plt.plot(df.loc[df['group'] == 'total']['dc factor'],
             df.loc[df['group'] == 'total']['average coarseness'],
             linestyle='', marker='d', color=colors[0])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()

    save_name = 'average_coarseness.png'
    plt.savefig(save_name)


if __name__ == '__main__':

    fdeci = 'csv/wwig_coarseness_measurements.csv'
    df_deci = pd.read_csv(fdeci, header=0, index_col=0)

    print(df_deci.keys())
    plot_average_coarseness(df_deci)
    plot_fsize(df_deci)

    plt.show()
