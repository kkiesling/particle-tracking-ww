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
            if e != 3:
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


def plot_cell_tally_refinement(df_refinement, df_output, refine):

    # I don't like these plots, but here we are..

    if refine == 'coarseness':
        refine_key = 'dc'
        xlabel = 'Triangle Density'
    elif refine == 'roughness':
        refine_key = 'sm'
        xlabel = 'Roughness'

    positions = [[0, 0], [0, 1], [1, 0], [1, 1]]
    fig, ax = plt.subplots(nrows=2, ncols=2, sharex=False,
                           sharey=False, figsize=(9, 6))

    for i, g in e_bounds.items():
        # subplot positions
        pr = positions[i][0]
        pc = positions[i][1]

        ref_tally = df_output.loc[df_output['mode'] ==
                                  'reference']['tally ' + g]
        ref_err = df_output.loc[df_output['mode'] ==
                                'reference']['error ' + g]
        ref_tally_plt = np.full(2, float(ref_tally))
        ref_sigma_plt_p = np.full(2, float(ref_tally + ref_err * ref_tally * n_sigma))
        ref_sigma_plt_n = np.full(2, float(ref_tally - ref_err * ref_tally * n_sigma))

        m_min = 1e300
        m_max = 0

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
                df_new = pd.merge(tally_vals, refine_vals, on='factor').sort_values(
                    'interior average ' + refine)

                if min(df_new['interior average ' + refine]) < m_min:
                    m_min = min(df_new['interior average ' + refine])
                if max(df_new['interior average ' + refine]) > m_max:
                    m_max = max(df_new['interior average ' + refine])

                if i == 0:
                    leg = '$r = {}$'.format(r)
                else:
                    leg = ''
                # plot raw values
                yerr = df_new['tally ' + g] * df_new['error ' + g] * n_sigma
                ax[pr][pc].errorbar(df_new['interior average ' + refine],
                                    df_new['tally ' + g], yerr=yerr,
                                    marker='d', lw=lw, capsize=cs, ls='',
                                    color=color_r[r], label=leg)
                ax[pr][pc].set_title('$E_{}$'.format(i))

            ax[pr][pc].plot([m_min, m_max], ref_tally_plt,
                            color=colors['reference'], ls='-', lw=lw)
            ax[pr][pc].plot([m_min, m_max], ref_sigma_plt_n,
                            color=colors['reference'], ls=':', lw=lw)
            ax[pr][pc].plot([m_min, m_max], ref_sigma_plt_p,
                            color=colors['reference'], ls=':', lw=lw)

    # labels
    ylabel = 'Tally'
    title = 'Cell Tally Results'
    fig.legend(bbox_to_anchor=(0.95, 0), loc='lower right', ncol=3,
               fontsize='x-small', title='Ratio')
    fig.suptitle(title)
    fig.text(0.01, 0.5, ylabel, va='center', rotation='vertical')
    fig.text(0.5, 0.01, xlabel, ha='center')
    plt.tight_layout(pad=2.7, w_pad=.5)

    save_name = 'raw_tally_results_{}.png'.format(refine)
    plt.savefig(save_name)


def plot_tally_ratios(df_output, pltratio=True, n_sigma=n_sigma):

    if pltratio:
        sharey = True
    else:
        sharey = False

    positions = [[0, 0], [0, 1], [1, 0], [1, 1]]
    fig, ax = plt.subplots(nrows=2, ncols=2, sharex=True,
                           sharey=sharey, figsize=(9, 6))

    for i, g in e_bounds.items():
        # subplot positions
        pr = positions[i][0]
        pc = positions[i][1]

        ref_tally = df_output.loc[df_output['mode'] ==
                                  'reference']['tally ' + g]
        ref_err = df_output.loc[df_output['mode'] ==
                                'reference']['error ' + g]

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
            df_output['refine'] == 'default'].loc[
                df_output['tally ' + g].notnull()]
        tally_vals = df_sub2[['tally ' + g, 'error ' + g, 'ratio']]

        # tally ratio
        if pltratio:
            tally_vals['tally ratio ' + g] = tally_vals['tally ' + g] / \
                float(ref_tally)

        # plot raw values
        if pltratio:
            m1 = tally_vals['tally ' + g]
            e1 = tally_vals['error ' + g]
            m2 = float(ref_tally)
            e2 = float(ref_err)
            s1 = m1 * e1
            s2 = m2 * e2
            yerr = np.sqrt((s1 / m2)**2 + (m1 * s2 / (m2 * m2))**2) * n_sigma
        else:
            yerr = tally_vals['tally ' + g] * tally_vals['error ' + g] * n_sigma

        if pltratio:
            y = tally_vals['tally ratio ' + g]
        else:
            tally_vals['tally ' + g]

        ax[pr][pc].errorbar(tally_vals['ratio'], y, yerr=yerr,
                            marker='d', lw=lw, capsize=cs, ls='',
                            color=colors[i], label='')
        ax[pr][pc].plot([ratios[0], ratios[-1]], ref_tally_plt,
                        color=colors['reference'], ls='-', lw=lw)
        ax[pr][pc].plot([ratios[0], ratios[-1]], ref_sigma_plt_n,
                        color=colors['reference'], ls=':', lw=lw)
        ax[pr][pc].plot([ratios[0], ratios[-1]], ref_sigma_plt_p,
                        color=colors['reference'], ls=':', lw=lw)

        if i == 3:
            title = '$E_{total}$'
        else:
            title = '$E_{}$'.format(i)
        ax[pr][pc].set_title(title)

    # labels
    ylabel = 'Tally'
    xlabel = 'WWIG spacing ratio'
    title = 'Cell Tally Results, ${}\sigma$'.format(n_sigma)
    #fig.legend(bbox_to_anchor=(0.95, 0), loc='lower right', ncol=3,
    #           fontsize='x-small', title='Energy Group')
    fig.suptitle(title)
    fig.text(0.01, 0.5, ylabel, va='center', rotation='vertical')
    fig.text(0.5, 0.01, xlabel, ha='center')
    plt.tight_layout(pad=2.7, w_pad=.5)

    save_name = 'raw_tally_results_ratios_{}.png'.format(n_sigma)
    plt.savefig(save_name)


def plot_ww_efficiency(df_output):
    # plot as a function of the ratio

    fig, ax = plt.subplots(nrows=2, ncols=2, sharex=True,
                           sharey=True, figsize=(9, 6))

    df_wwig = df_output.loc[df_output['mode'] == 'wwig'].loc[
        df_output['refine'] == 'default']
    df_cwwm = df_output.loc[df_output['mode'] == 'cwwm']
    cwwm_ww = np.full(2, float(df_cwwm['WW check efficiency']))
    cwwm_lt = np.full(2, float(df_cwwm['Splits < C_u']))
    cwwm_eq = np.full(2, float(df_cwwm['Splits = C_u']))
    cwwm_gt = np.full(2, float(df_cwwm['Splits > C_u']))

    # plot overall efficiency
    ax[0][0].plot([5, 10], cwwm_ww, marker='', ls=':')
    ax[0][0].plot(df_wwig['ratio'], df_wwig['WW check efficiency'],
                  marker='d', ls='')
    ax[0][0].set_title('Total Efficiency')

    ax[0][1].plot([5, 10], cwwm_lt, marker='', ls=':')
    ax[0][1].plot(df_wwig['ratio'], df_wwig['Splits < C_u'],
                  marker='d', ls='')
    ax[0][1].set_title('Splitting Efficiency, $N_{splits}$ < C_u')

    ax[1][0].plot([5, 10], cwwm_eq, marker='', ls=':')
    ax[1][0].plot(df_wwig['ratio'], df_wwig['Splits = C_u'],
                  marker='d', ls='')
    ax[1][0].set_title('Splitting Efficiency, $N_{splits}$ = C_u')

    ax[1][1].plot([5, 10], cwwm_gt, marker='', ls=':')
    ax[1][1].plot(df_wwig['ratio'], df_wwig['Splits > C_u'],
                  marker='d', ls='')
    ax[1][1].set_title('Splitting Efficiency, $N_{splits}$ > C_u')


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

    # plot tally results
    plot_tally_ratios(df_output, pltratio=True, n_sigma=1)
    plot_tally_ratios(df_output, pltratio=True, n_sigma=2)
    plot_tally_ratios(df_output, pltratio=True, n_sigma=3)

    # plot ww efficiencies
    plot_ww_efficiency(df_output)

    # plot average interior roughness and coarseness
    plot_interior_averages(df_refinement, 'roughness')
    plot_interior_averages(df_refinement, 'coarseness')

    # plot tally results as function of smoothness and roughness
    plot_cell_tally_refinement(df_refinement, df_output, 'roughness')
    plot_cell_tally_refinement(df_refinement, df_output, 'coarseness')

    plt.show()
