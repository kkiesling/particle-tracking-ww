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


def plot_tally_ratios(df_output, pltratio=True, n_sigma=n_sigma):

    plt.figure()

    xmax = 11  # for location of the analog and cwwm results

    ref_tally = df_output.loc[df_output['mode'] ==
                              'reference']['tally total']
    ref_err = df_output.loc[df_output['mode'] ==
                            'reference']['error total']

    cwwm_tally = df_output.loc[df_output['mode'] ==
                               'cwwm']
    ana_tally = df_output.loc[df_output['mode'] ==
                              'analog']

    if pltratio:
        ref_tally_plt = np.full(2, 1)
        ref_sigma_plt_p = np.full(
            2, float(1 + ref_err * n_sigma))
        ref_sigma_plt_n = np.full(
            2, float(1 - ref_err * n_sigma))
    else:
        ref_tally_plt = np.full(2, float(ref_tally))
        ref_sigma_plt_p = np.full(
            2, float(ref_tally + ref_err * ref_tally * n_sigma))
        ref_sigma_plt_n = np.full(
            2, float(ref_tally - ref_err * ref_tally * n_sigma))

    # get tally results
    df_sub2 = df_output.loc[df_output['mode'] == 'wwig'].loc[
        df_output['tally total'].notnull()]
    tally_vals = df_sub2[['tally total', 'error total', 'ratio']]

    # tally ratio
    if pltratio:
        tally_vals['tally ratio total'] = tally_vals['tally total'] / \
            float(ref_tally)
        cwwm_tally['tally ratio total'] = cwwm_tally['tally total'] / \
            float(ref_tally)
        ana_tally['tally ratio total'] = ana_tally['tally total'] / \
            float(ref_tally)

    # plot raw values
    if pltratio:
        m2 = float(ref_tally)
        e2 = float(ref_err)

        # wwig
        m1 = tally_vals['tally total']
        e1 = tally_vals['error total']
        s1 = m1 * e1
        s2 = m2 * e2
        yerr = np.sqrt((s1 / m2)**2 + (m1 * s2 / (m2 * m2))**2) * n_sigma

        # cwwm
        m1 = cwwm_tally['tally total']
        e1 = cwwm_tally['error total']
        s1 = m1 * e1
        s2 = m2 * e2
        y_cwwm_err = np.sqrt((s1 / m2)**2 + (m1 * s2 / (m2 * m2))**2) * n_sigma

        # analog
        m1 = ana_tally['tally total']
        e1 = ana_tally['error total']
        s1 = m1 * e1
        s2 = m2 * e2
        y_ana_err = np.sqrt((s1 / m2)**2 + (m1 * s2 / (m2 * m2))**2) * n_sigma
    else:
        yerr = tally_vals['tally total'] * tally_vals['error total'] * n_sigma
        y_cwwm_err = cwwm_tally['total tally'] * \
            cwwm_tally['error total'] * n_sigma
        y_ana_err = ana_tally['total tally'] * \
            ana_tally['error total'] * n_sigma

    if pltratio:
        y = tally_vals['tally ratio total']
        cwwm_y = cwwm_tally['tally ratio total']
        ana_y = ana_tally['tally ratio total']
    else:
        y = tally_vals['tally total']
        cwwm_y = cwwm_tally['tally total']
        ana_y = ana_tally['tally total']

    plt.errorbar(tally_vals['ratio'], y, yerr=yerr,
                 marker='d', lw=lw, capsize=cs, ls='',
                 color=colors[0], label='WWIG')
    plt.errorbar([xmax], cwwm_y, yerr=y_cwwm_err,
                 marker='o', lw=lw, capsize=cs, ls='',
                 color=colors['cwwm'], label='CWWM')
    plt.errorbar([xmax], ana_y, yerr=y_ana_err,
                 marker='o', lw=lw, capsize=cs, ls='',
                 color=colors['analog'], label='Analog')
    plt.plot([ratios[0], xmax], ref_tally_plt,
             color=colors['reference'], ls='-', lw=lw, label='Reference')
    plt.plot([ratios[0], xmax], ref_sigma_plt_n,
             color=colors['reference'], ls=':', lw=lw,
             label='Reference $\pm {} \sigma$'.format(n_sigma))
    plt.plot([ratios[0], xmax], ref_sigma_plt_p,
             color=colors['reference'], ls=':', lw=lw, label='')

    # labels
    ylabel = 'Tally'
    xlabel = 'WWIG spacing ratio'
    title = 'Cell Tally Results, ${}\sigma$'.format(n_sigma)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='best', ncol=2,
               fontsize='x-small')
    plt.tight_layout()

    save_name = 'images/surface_tally_results_ratios_{}.png'.format(n_sigma)
    plt.savefig(save_name)


def plot_ww_efficiency(df_output):
    # plot as a function of the ratio

    fig, ax = plt.subplots(nrows=2, ncols=2, sharex=True,
                           sharey=False, figsize=(9, 6))

    df_wwig = df_output.loc[df_output['mode'] ==
                            'wwig'].loc[~df_output['ratio'].isnull()]
    df_cwwm = df_output.loc[df_output['mode'] == 'cwwm']
    cwwm_ww = np.full(2, float(df_cwwm['WW check efficiency']))
    cwwm_lt = np.full(2, float(df_cwwm['Splits < C_u']))
    cwwm_eq = np.full(2, float(df_cwwm['Splits = C_u']))
    cwwm_gt = np.full(2, float(df_cwwm['Splits > C_u']))

    # plot overall efficiency
    ax[0][0].plot([5, 10], cwwm_ww, marker='', ls=':', label='CWWM')
    ax[0][0].plot(df_wwig['ratio'], df_wwig['WW check efficiency'],
                  marker='d', ls='', label='WWIG')
    ax[0][0].set_title('Total WW Efficiency', fontsize='small')

    ax[0][1].plot([5, 10], cwwm_lt, marker='', ls=':')
    ax[0][1].plot(df_wwig['ratio'], df_wwig['Splits < C_u'],
                  marker='d', ls='', label='')
    ax[0][1].set_title('$N_{splits}$ < C_u', fontsize='small')

    ax[1][0].plot([5, 10], cwwm_eq, marker='', ls=':')
    ax[1][0].plot(df_wwig['ratio'], df_wwig['Splits = C_u'],
                  marker='d', ls='', label='')
    ax[1][0].set_title('$N_{splits}$ = C_u', fontsize='small')

    ax[1][1].plot([5, 10], cwwm_gt, marker='', ls=':')
    ax[1][1].plot(df_wwig['ratio'], df_wwig['Splits > C_u'],
                  marker='d', ls='', label='')
    ax[1][1].set_title('$N_{splits}$ > C_u', fontsize='small')

    # labels
    ylabel = 'Efficiency'
    title = 'Weight Window Efficiency'
    fig.suptitle(title)
    fig.text(0.01, 0.5, ylabel, va='center', rotation='vertical')
    fig.text(0.5, 0.01, 'WWIG Ratio', ha='center')
    fig.legend(bbox_to_anchor=(0.9, 0), loc='lower right', ncol=2,
               fontsize='x-small')
    plt.tight_layout(pad=2.7, w_pad=.5)

    save_name = 'images/ww_efficiency_ratios.png'
    plt.savefig(save_name)


if __name__ == '__main__':

    fpath = sys.argv[1]  # path folder of csv files

    # get all output data
    all_data_files = glob.glob(fpath + '/*_data.csv')
    df_output = pd.concat((
        pd.read_csv(f, header=0, index_col=0) for f in all_data_files),
        sort=False, ignore_index=True)

    print(df_output.keys())

    # plot tally results
    plot_tally_ratios(df_output, pltratio=True, n_sigma=1)
    plot_tally_ratios(df_output, pltratio=True, n_sigma=2)
    plot_tally_ratios(df_output, pltratio=True, n_sigma=3)

    # plot ww efficiencies
    plot_ww_efficiency(df_output)

    plt.show()
