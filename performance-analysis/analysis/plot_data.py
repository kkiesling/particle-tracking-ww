import sys
import numpy as np
from matplotlib import legend
import pandas as pd
import glob
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame

colors = {0: '#FF4242', 1: '#235FA4', 2: '#6FDE6E', 'cwwm': '#E8F086',
          'analog': '#0A284B', 'reference': '#A691AE'}
markers = {0: 'x', 1: 'x', 2: 'x', 'cwwm': 'o',
           'analog': 'd', 'reference': 'D'}
e_bounds = {0: '1.0000E-05', 1: '1.0000E-01', 2: '2.0000E+01'}
ratios = [5, 6, 7, 8, 9, 10]
dpi = 600


def calc_ratios(m1, e1, m2, e2):
    # m1 = experiment
    # m2 = accepted

    #ratios = m1 / m2
    s1 = m1 * e1
    s2 = m2 * e2
    sigma_ratio = np.sqrt((s1 / m2)**2 + (m1 * s2 / (m2 * m2))**2)

    return sigma_ratio


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

        for e in e_bounds.keys():
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


def plot_cell_tally(df_refinement, df_output, refine):
    if refine == 'coarseness':
        refine_key = 'dc'
    elif refine == 'roughness':
        refine_key = 'sm'

    # x = refinement measurement
    # y = cell tally / reference - per energy group

    positions = [[0, 0], [0, 1], [1, 0], [1, 1]]
    fig, ax = plt.subplots(nrows=2, ncols=2, sharex=False,
                           sharey=False, figsize=(9, 6))

    groups = list(e_bounds.values()) + ['total']
    for i, g in e_bounds.items():
        # subplot positions
        pr = positions[i][0]
        pc = positions[i][1]

        ref_tally = df_output.loc[df_output['mode'] ==
                                  'reference']['tally ' + g]
        ref_err = df_output.loc[df_output['mode'] ==
                                'reference']['error ' + g]

        # get refinement measurements
        if g != 'total':
            for r in ratios:
                df_sub1 = df_refinement.loc[
                    df_refinement['energy group'] == i].loc[
                        df_refinement['ratio'] == r].loc[
                            df_refinement['mode'].isin(
                                [refine_key, 'default'])]

                # replace the NaN value for default with value 1 so it
                # can be merged later
                df_sub1['factor'] = df_sub1['factor'].replace(np.nan, 1.0)
                refine_vals = df_sub1[['factor', 'interior average ' + refine]]

                # get tally results
                df_sub2 = df_output.loc[df_output['mode'] == 'wwig'].loc[
                    df_output['ratio'] == r].loc[
                        df_output['refine'].isin([refine_key, 'default'])].loc[
                            df_output['tally ' + g].notnull()]
                tally_vals = df_sub2[['refine', 'factor',
                                      'tally ' + g, 'error ' + g]]

                # merge so we match the correct tally to refinement
                df_new = pd.merge(tally_vals, refine_vals, on='factor')
                print(df_new)


if __name__ == '__main__':

    fpath = sys.argv[1]  # path folder of csv files

    # get all output data
    all_data_files = glob.glob(fpath + '/*_data.csv')
    df_output = pd.concat((
        pd.read_csv(f, header=0, index_col=0) for f in all_data_files),
        sort=False, ignore_index=True)

    print(df_output.keys())

    # get all wwig measurement data
    all_wwig_files = glob.glob(fpath + '/wwig_*_measurements.csv')
    df_refinement = pd.concat((
        pd.read_csv(f, header=0, index_col=0) for f in all_wwig_files),
        sort=False, ignore_index=True)

    print(df_refinement.keys())

    # plot average interior roughness and coarseness
    plot_interior_averages(df_refinement, 'roughness')
    plot_interior_averages(df_refinement, 'coarseness')

    # plot tally results as function of smoothness and roughness
    plot_cell_tally(df_refinement, df_output, 'roughness')
    plot_cell_tally(df_refinement, df_output, 'coarseness')

    #plt.show()
