import os
import numpy as np
from matplotlib import legend
import pandas as pd
import glob
import matplotlib.pyplot as plt

wwig_colors = ['#F3B4CB', '#EA84AA', '#FF5A96', '#FF0A64', '#C11D59',
               '#86284A', '#653345', '#67072A', '#3C0346', '#60226B',
               '#831596', '#814A8A', '#B106CE', '#BE58D0', '#DF9EEA',
               '#F6C1FF']
colors = {'wwig': '#C11D59', 'analog': '#7CC145',
          'cwwm': '#247F03', 'reference': '#24E2A5'}
markers = {'wwig': 'd', 'cwwm': 'o',
           'analog': 'x', 'reference': 'X'}
e_bounds = {0: '1.0000E-05', 1: '1.0000E-01', 2: '2.0000E+01', 3: 'total'}
ratios = [5, 6, 7, 8, 9, 10]
dpi = 600
lw = .9  # line width for plots
cs = 5  # error bar cap size
n_sigma = 3

fcwwm = '../inputs/wwinp_slab'
cwwm_size = os.path.getsize(fcwwm) / (1024.**2)


def plot_fsize(df):
    # plot total file size - decimated sizes only
    plt.figure()
    title = 'Memory Footprint'
    xlabel = r'Decimation Factor $d$'
    ylabel = 'Total File Size (MB)'

    plt.plot(df.loc[df['group'] == 'total']['dc factor'],
             df.loc[df['group'] == 'total']['size'],
             linestyle='', marker='d', color=colors['wwig'], label='WWIG')
    plt.plot([min(df['dc factor']), max(df['dc factor'])],
             [cwwm_size, cwwm_size],
             linestyle=':', marker='', color=colors['cwwm'], label='CWWM')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='best', ncol=2,
               fontsize='x-small')
    plt.tight_layout()

    save_name = 'images/fsize_decimated.png'
    plt.savefig(save_name)


def plot_fsize_ratio(df):
    # plot total file size - decimated sizes only
    plt.figure()
    title = 'Memory Footprint'
    xlabel = 'WWIG Surface Spacing Ratio'
    ylabel = 'Total File Size (MB)'

    plt.plot(df.loc[df['group'] == 'total']['ratio'],
             df.loc[df['group'] == 'total']['size'],
             linestyle='', marker='d', color=colors['wwig'], label='WWIG')
    plt.plot([min(df['ratio']), max(df['ratio'])],
             [cwwm_size, cwwm_size],
             linestyle=':', marker='', color=colors['cwwm'], label='CWWM')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='best', ncol=2,
               fontsize='x-small')
    plt.tight_layout()

    save_name = 'images/fsize_ratio.png'
    plt.savefig(save_name)


def plot_average_coarseness(df):
    # just plot averages for each decimation factor
    plt.figure()
    title = 'Mesh Coarseness'
    xlabel = r'Decimation Factor $d$'
    ylabel = 'Average Global Coarseness'

    plt.plot(df.loc[df['group'] == 'total']['dc factor'],
             df.loc[df['group'] == 'total']['average coarseness'],
             linestyle='', marker='d', color=colors['wwig'])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()

    save_name = 'images/average_coarseness.png'
    plt.savefig(save_name)


def subplot_roughness(df, group_min, group_max):
    fig, ax = plt.subplots(nrows=3, ncols=3, sharex=True,
                           sharey=False, figsize=(9, 9))
    positions = [[0, 0], [0, 1], [0, 2],
                 [1, 0], [1, 1], [1, 2],
                 [2, 0], [2, 1], [2, 2]]
    for i, group in enumerate(range(group_min, group_max)):
        pr = positions[i][0]
        pc = positions[i][1]
        df_sub = df.loc[df['group'] == str(group)]
        ax[pr][pc].plot(df_sub['perturbation'],
                        df_sub['average roughness'],
                        linestyle='', marker='d', color=colors['wwig'])
        title_str = 'E_{}'.format(group)
        ax[pr][pc].set_title('$E_{' + str(group) + '}$')

    save_name = 'images/group_roughness_{}_{}.png'.format(group_min, group_max)
    plt.savefig(save_name)


def plot_roughness_per_group(df):
    # measured roughness vs applied perturbation
    subplot_roughness(df, 0, 9)
    subplot_roughness(df, 9, 18)
    subplot_roughness(df, 18, 27)


def plot_average_roughness(df):
    plt.figure()
    title = 'Surface Roughness\n' + '(artificial roughness)'
    xlabel = r'Maximum Perturbation $\delta$'
    ylabel = 'Average Global Roughness'

    plt.plot(df.loc[df['group'] == 'total']['perturbation'],
             df.loc[df['group'] == 'total']['average roughness'],
             linestyle='', marker='d', color=colors['wwig'])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim((0.18, 0.32))
    plt.tight_layout()

    save_name = 'images/average_roughness.png'
    plt.savefig(save_name)


def plot_average_roughness_smoothed(df):
    plt.figure()
    title = 'Surface Roughness\n' + '(after smoothing)'
    xlabel = r'Number of smoothing iterations'
    ylabel = 'Average Global Roughness'

    plt.plot(df.loc[df['group'] == 'total'].loc[df['iterations'] <= 10].loc[df['iterations'] > 1]['iterations'],
             df.loc[df['group'] == 'total'].loc[df['iterations'] <= 10].loc[df['iterations'] > 1]['average roughness'],
             linestyle='', marker='d', color=colors['wwig'])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim((0.18, 0.32))
    plt.tight_layout()

    save_name = 'images/average_roughness_smoothed.png'
    plt.savefig(save_name)


if __name__ == '__main__':

    # coarseness
    fdeci = 'csv/wwig_coarseness_measurements.csv'
    df_deci = pd.read_csv(fdeci, header=0, index_col=0)
    print(df_deci.keys())
    plot_average_coarseness(df_deci)
    plot_fsize(df_deci)

    # get all wwig roughness measurement data
    all_rough_files = glob.glob('csv/wwig_roughness_measurements_*.csv')
    df_rough = pd.concat((
        pd.read_csv(f, header=0, index_col=0) for f in all_rough_files),
        sort=False, ignore_index=True)
    print(df_rough.keys())

    plot_roughness_per_group(df_rough)
    plot_average_roughness(df_rough)

    all_smooth_files = glob.glob('csv/wwig_roughness_smoothed_s01*.csv')
    df_smooth = pd.concat((
        pd.read_csv(f, header=0, index_col=0) for f in all_smooth_files),
        sort=False, ignore_index=True)
    df_smooth.iterations.fillna(df_smooth.perturbation, inplace=True)
    del df_smooth['perturbation']
    print(df_smooth.keys())
    plot_average_roughness_smoothed(df_smooth)

    fratio = 'csv/wwig_ratio_size.csv'
    df_ratio = pd.read_csv(fratio, header=0, index_col=0)
    print(df_ratio.keys())
    plot_fsize_ratio(df_ratio)

    plt.show()
