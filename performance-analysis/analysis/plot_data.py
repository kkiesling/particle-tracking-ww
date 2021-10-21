import sys
import os
from matplotlib import legend
import pandas as pd
import glob
import matplotlib.pyplot as plt

colors = {0: '#FF4242', 1: '#235FA4', 2: '#6FDE6E', 'cwwm': '#E8F086',
          'analog': '#0A284B', 'reference': '#A691AE'}
markers = {0: 'x', 1: 'x', 2: 'x', 'cwwm': 'o',
           'analog': 'd', 'reference': 'D'}
energy_groups = [0, 1, 2]
ratios = [5, 6, 7, 8, 9, 10]
dpi = 600


def plot_interior_averages(df, refine):
    # x-axis = smoothing factor
    # y-axis = roughness / default
    # one line per energy group
    # one plot per ratio [5 -> 10]

    positions = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]]
    fig, ax = plt.subplots(nrows=2, ncols=3, sharex=True,
                           sharey=True, figsize=(9, 6))

    if refine == 'coarseness':
        refine_key = 'dc'
        title = 'Average Coarseness'
        xlabel = 'Decimation Factor'
        ylabel = 'Triangle Density'
    elif refine == 'roughness':
        refine_key = 'sm'
        title = 'Average Roughness'
        xlabel = 'Smoothing Factor'
        ylabel = 'Roughness'

    for i, r in enumerate(ratios):
        pr = positions[i][0]
        pc = positions[i][1]

        # get factor applied
        df_sub = df.loc[df['mode'] == refine_key].loc[df['ratio'] == r]

        # get default averages
        df_default = df.loc[df['mode'] == 'default'].loc[df['ratio'] == r]

        for e in energy_groups:
            # default wwig value
            default_val = df_default.loc[
                df_default['energy group'] == e][
                    'interior average {}'.format(refine)]

            # get applied factors and measurements (compared to default)
            df_sub_sub = df_sub.loc[df_sub['energy group'] == e]
            factor_list = df_sub_sub['factor']
            interior_averages = df_sub_sub[
                'interior average {}'.format(refine)] / float(default_val)

            # only need legend labels one time
            if i == 0:
                leg = '$E_{}$'.format(e)
            else:
                leg = ''

            # plot energy group
            ax[pr][pc].plot(
                factor_list, interior_averages, linestyle='',
                marker=markers[e], color=colors[e], label=leg)

        # set title and axes labels
        ax[pr][pc].set_title('Ratio = {}'.format(r), fontsize='small')

        # set x label one time on center plot
        if pr == 1 and pc == 1:
            ax[pr][pc].set_xlabel(xlabel)

    # labels
    fig.legend(bbox_to_anchor=(0.95, 0), loc='lower right', ncol=3,
               fontsize='x-small', title='Energy Group')
    fig.suptitle(title)
    fig.text(0.01, 0.5, ylabel, va='center', rotation='vertical')
    plt.tight_layout(pad=2.7, w_pad=.5)

    save_name = 'interior_averages_{}.png'.format(refine)
    plt.savefig(save_name)


if __name__ == '__main__':

    fpath = sys.argv[1]  # path folder of csv files

    # get all output data
    all_data_files = glob.glob(fpath + '/*_data.csv')
    df_output = pd.concat((
        pd.read_csv(f, header=0, index_col=0) for f in all_data_files),
        sort=False, ignore_index=True)

    # get all wwig measurement data
    all_wwig_files = glob.glob(fpath + '/wwig_*_measurements.csv')
    df_refinement = pd.concat((
        pd.read_csv(f, header=0, index_col=0) for f in all_wwig_files),
        sort=False, ignore_index=True)

    # plot average interior roughness and coarseness
    plot_interior_averages(df_refinement, 'roughness')
    plot_interior_averages(df_refinement, 'coarseness')

    plt.show()
