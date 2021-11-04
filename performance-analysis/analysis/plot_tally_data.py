import sys
import numpy as np
from matplotlib import legend
import pandas as pd
import glob
import matplotlib.pyplot as plt


# colors: '#FF4242' '#A691AE' '#235FA4' '#E8F086',
#         '#0A284B' '#6FDE6E' '#0A284B'
colors = {'wwig': '#FF4242', 'analog': '#E8F086',
          'cwwm': '#0A284B', 'reference': '#6FDE6E'}
markers = {'wwig': 'd', 'cwwm': 'o',
           'analog': 'x', 'reference': 'X'}
ratios = [5, 6, 7, 8, 9, 10]
dpi = 600
lw = .9  # line width for plots
cs = 5  # error bar cap size
n_sigma = 1


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
                 marker=markers['wwig'], lw=lw, capsize=cs, ls='',
                 color=colors['wwig'], label='WWIG')
    plt.errorbar([xmax], cwwm_y, yerr=y_cwwm_err,
                 marker=markers['cwwm'], lw=lw, capsize=cs, ls='',
                 color=colors['cwwm'], label='CWWM')
    plt.errorbar([xmax], ana_y, yerr=y_ana_err,
                 marker=markers['analog'], lw=lw, capsize=cs, ls='',
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
    title = 'Surface Tally Results, ${}\sigma$'.format(n_sigma)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='best', ncol=2,
               fontsize='x-small')
    plt.tight_layout()

    save_name = 'images/surface_tally_results_ratios_{}.png'.format(n_sigma)
    plt.savefig(save_name)


def plot_tally_refinement(df_output, df_measure, refinement,
                          pltratio=True, n_sigma=n_sigma):

    # reference
    ref_tally = df_output.loc[df_output['mode'] ==
                              'reference']['tally total']
    ref_err = df_output.loc[df_output['mode'] ==
                            'reference']['error total']
    ref_tally_plt = np.full(2, float(ref_tally))
    ref_sigma_plt_p = np.full(
        2, float(ref_tally + ref_err * ref_tally * n_sigma))
    ref_sigma_plt_n = np.full(
        2, float(ref_tally - ref_err * ref_tally * n_sigma))

    if refinement == 'coarseness':
        measurement = 'average coarseness'
        refine_key = 'dc factor'
        output_key = 'decimation'
        xlabel = 'Triangle Density'
    elif refinement == 'roughness':
        measurement = 'average roughness'
        refine_key = 'perturbation'
        output_key = 'perturbation'
        xlabel = 'Surface Roughness'

    # get the output data for total tally
    df_tally = df_output.loc[~df_output[output_key].isnull()][
        ['tally total', 'error total', output_key]]

    # get measurement data for total only
    df_refine = df_measure.loc[df_measure['group'] == 'total'][
        [refine_key, measurement]]

    # join with the measurement tally on the output_key and refine_key
    df = pd.merge(df_tally, df_refine, how='left', left_on=[
                  output_key], right_on=[refine_key])

    plt.figure()
    plt.errorbar(df[measurement], df['tally total'],
                 yerr=df['tally total'] * df['error total'],
                 marker=markers['wwig'], lw=lw, capsize=cs, ls='',
                 color=colors['wwig'], label='WWIG')
    xmin = min(df[measurement])
    xmax = max(df[measurement])
    plt.plot([xmin, xmax], ref_tally_plt,
             color=colors['reference'], ls='-', lw=lw, label='Reference')
    plt.plot([xmin, xmax], ref_sigma_plt_n,
             color=colors['reference'], ls=':', lw=lw,
             label='Reference $\pm {} \sigma$'.format(n_sigma))
    plt.plot([xmin, xmax], ref_sigma_plt_p,
             color=colors['reference'], ls=':', lw=lw, label='')

    # labels
    ylabel = 'Tally'
    title = 'Surface Tally Results'
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    save_name = 'images/tally_vs_{}.png'.format(refinement)
    plt.savefig(save_name)


def plot_ww_efficiency_ratio(df_output):
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
    ax[0][0].plot([5, 10], cwwm_ww, marker='', ls=':',
                  label='CWWM', color=colors['cwwm'])
    ax[0][0].plot(df_wwig['ratio'], df_wwig['WW check efficiency'],
                  marker=markers['wwig'], ls='', label='WWIG',
                  color=colors['wwig'])
    ax[0][0].set_title('Total WW Efficiency', fontsize='small')

    ax[0][1].plot([5, 10], cwwm_lt, marker='', ls=':', color=colors['cwwm'])
    ax[0][1].plot(df_wwig['ratio'], df_wwig['Splits < C_u'],
                  marker=markers['wwig'], ls='', label='',
                  color=colors['wwig'])
    ax[0][1].set_title('$N_{splits}$ < C_u', fontsize='small')

    ax[1][0].plot([5, 10], cwwm_eq, marker='', ls=':', color=colors['cwwm'])
    ax[1][0].plot(df_wwig['ratio'], df_wwig['Splits = C_u'],
                  marker=markers['wwig'], ls='', label='',
                  color=colors['wwig'])
    ax[1][0].set_title('$N_{splits}$ = C_u', fontsize='small')

    ax[1][1].plot([5, 10], cwwm_gt, marker='', ls=':', color=colors['cwwm'])
    ax[1][1].plot(df_wwig['ratio'], df_wwig['Splits > C_u'],
                  marker=markers['wwig'], ls='', label='',
                  color=colors['wwig'])
    ax[1][1].set_title('$N_{splits}$ > C_u', fontsize='small')

    # labels
    ylabel = 'Efficiency'
    title = 'Weight Window Efficiency'
    fig.suptitle(title)
    fig.text(0.01, 0.5, ylabel, va='center', rotation='vertical')
    fig.text(0.5, 0.01, 'WWIG Surface Spacing Ratio', ha='center')
    fig.legend(bbox_to_anchor=(0.9, 0), loc='lower right', ncol=2,
               fontsize='x-small')
    plt.tight_layout(pad=2.7, w_pad=.5)

    save_name = 'images/ww_efficiency_ratios.png'
    plt.savefig(save_name)


def plot_ww_efficiency_refine(df_output, df_rough):
    # plot as a function of the ratio

    fig, ax = plt.subplots(nrows=2, ncols=2, sharex=True,
                           sharey=False, figsize=(9, 6))

    df_out = df_output.loc[
        df_output['mode'] == 'wwig'].loc[
            ~df_output['perturbation'].isnull()]
    df_refine = df_rough.loc[df_rough['group'] == 'total'][
        ['average roughness', 'perturbation']]
    df_wwig = pd.merge(df_out, df_refine, how='left',
                       left_on=['perturbation'], right_on=['perturbation'])

    # df_cwwm = df_output.loc[df_output['mode'] == 'cwwm']
    # cwwm_ww = np.full(2, float(df_cwwm['WW check efficiency']))
    # cwwm_lt = np.full(2, float(df_cwwm['Splits < C_u']))
    # cwwm_eq = np.full(2, float(df_cwwm['Splits = C_u']))
    # cwwm_gt = np.full(2, float(df_cwwm['Splits > C_u']))
    # xmin = min(df_wwig['average roughness'])
    # xmax = max(df_wwig['average roughness'])

    # plot overall efficiency
    # ax[0][0].plot([xmin, xmax], cwwm_ww, marker='', ls=':',
    #               label='CWWM', color=colors['cwwm'])
    ax[0][0].plot(df_wwig['average roughness'], df_wwig['WW check efficiency'],
                  marker=markers['wwig'], ls='',
                  label='WWIG', color=colors['wwig'])
    ax[0][0].set_title('Total WW Efficiency', fontsize='small')

    # ax[0][1].plot([xmin, xmax], cwwm_lt, marker='',
    #               ls=':', color=colors['cwwm'])
    ax[0][1].plot(df_wwig['average roughness'], df_wwig['Splits < C_u'],
                  marker=markers['wwig'], ls='', label='',
                  color=colors['wwig'])
    ax[0][1].set_title('$N_{splits}$ < C_u', fontsize='small')

    # ax[1][0].plot([xmin, xmax], cwwm_eq, marker='',
    #               ls=':', color=colors['cwwm'])
    ax[1][0].plot(df_wwig['average roughness'], df_wwig['Splits = C_u'],
                  marker=markers['wwig'], ls='', label='',
                  color=colors['wwig'])
    ax[1][0].set_title('$N_{splits}$ = C_u', fontsize='small')

    # ax[1][1].plot([xmin, xmax], cwwm_gt, marker='',
    #               ls=':', color=colors['cwwm'])
    ax[1][1].plot(df_wwig['average roughness'], df_wwig['Splits > C_u'],
                  marker=markers['wwig'], ls='', label='',
                  color=colors['wwig'])
    ax[1][1].set_title('$N_{splits}$ > C_u', fontsize='small')

    # labels
    ylabel = 'Efficiency'
    title = 'Weight Window Efficiency'
    fig.suptitle(title)
    fig.text(0.01, 0.5, ylabel, va='center', rotation='vertical')
    fig.text(0.5, 0.01, 'Average Surface Roughness', ha='center')
    # fig.legend(bbox_to_anchor=(0.9, 0), loc='lower right', ncol=2,
    #            fontsize='x-small')
    plt.tight_layout(pad=2.7, w_pad=.5)

    save_name = 'images/ww_efficiency_roughness.png'
    plt.savefig(save_name)


def plot_fom(df_output, df_measure, refinement):
    if refinement == 'coarseness':
        measurement = 'average coarseness'
        refine_key = 'dc factor'
        output_key = 'decimation'
        xlabel = 'Triangle Density'
    elif refinement == 'roughness':
        measurement = 'average roughness'
        refine_key = 'perturbation'
        output_key = 'perturbation'
        xlabel = 'Surface Roughness'

    # get the output data for total tally
    df_tally = df_output.loc[~df_output[output_key].isnull()][
        ['fom', output_key, 'cpu time']]

    # get measurement data for total only
    df_refine = df_measure.loc[df_measure['group'] == 'total'][
        [refine_key, measurement]]

    # join with the measurement tally on the output_key and refine_key
    df = pd.merge(df_tally, df_refine, how='left', left_on=[
                  output_key], right_on=[refine_key])

    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True,
                           sharey=False, figsize=(5, 6))

    ax[0].plot(df[measurement], df['fom'], marker=markers['wwig'], ls='',
               color=colors['wwig'], label='WWIG')
    ax[0].set_ylabel('FOM')
    ax[1].plot(df[measurement], df['cpu time'], marker=markers['wwig'], ls='',
               color=colors['wwig'], label='WWIG')
    ax[1].set_ylabel('CPU time (min)')

    # labels
    title = 'Figure of Merit'
    plt.title(title)
    plt.xlabel(xlabel)
    plt.tight_layout()
    save_name = 'images/fom_{}.png'.format(refinement)
    plt.savefig(save_name)


def plot_relative_error_ratio(df_output):
    plt.figure()

    xmax = 11  # for location of the analog, reference, and cwwm results
    ref_err = df_output.loc[df_output['mode'] == 'reference']['error total']
    cwwm_err = df_output.loc[df_output['mode'] == 'cwwm']['error total']
    ana_err = df_output.loc[df_output['mode'] == 'analog']['error total']
    ref_err_plt = np.full(2, float(ref_err))
    cwwm_err_plt = np.full(2, float(cwwm_err))
    ana_err_plt = np.full(2, float(ana_err))

    # get wwig relative errors
    df_sub2 = df_output.loc[df_output['mode'] == 'wwig'].loc[
        df_output['tally total'].notnull()]
    wwig_err = df_sub2[['error total', 'ratio']]

    plt.plot(wwig_err['ratio'], wwig_err['error total'],
             marker=markers['wwig'],
             color=colors['wwig'], ls='', lw=lw, label='WWIG')
    plt.plot([ratios[0], xmax], ref_err_plt,
             color=colors['reference'], ls=':', lw=lw, label='Reference')
    plt.plot([ratios[0], xmax], cwwm_err_plt,
             color=colors['cwwm'], ls=':', lw=lw,
             label='CWWM')
    plt.plot([ratios[0], xmax], ana_err_plt,
             color=colors['analog'], ls=':', lw=lw, label='Analog')

    # labels
    ylabel = 'Relative Error'
    xlabel = 'WWIG spacing ratio'
    title = 'Surface Tally Relative Error'
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='best', ncol=2,
               fontsize='x-small')
    plt.tight_layout()

    save_name = 'images/relative_error_surface_ratios.png'
    plt.savefig(save_name)


def plot_relative_error_refine(df_output, df_measure, refinement):
    if refinement == 'coarseness':
        measurement = 'average coarseness'
        refine_key = 'dc factor'
        output_key = 'decimation'
        xlabel = 'Triangle Density'
    elif refinement == 'roughness':
        measurement = 'average roughness'
        refine_key = 'perturbation'
        output_key = 'perturbation'
        xlabel = 'Surface Roughness'

    plt.figure()

    ref_err = df_output.loc[df_output['mode'] == 'reference']['error total']
    cwwm_err = df_output.loc[df_output['mode'] == 'cwwm']['error total']
    ana_err = df_output.loc[df_output['mode'] == 'analog']['error total']
    ref_err_plt = np.full(2, float(ref_err))
    cwwm_err_plt = np.full(2, float(cwwm_err))
    ana_err_plt = np.full(2, float(ana_err))

    # get wwig relative errors
    # get the output data for total tally
    df_tally = df_output.loc[~df_output[output_key].isnull()][
        ['error total', output_key]]

    # get measurement data for total only
    df_refine = df_measure.loc[df_measure['group'] == 'total'][
        [refine_key, measurement]]

    # join with the measurement tally on the output_key and refine_key
    wwig_err = pd.merge(df_tally, df_refine, how='left', left_on=[
                        output_key], right_on=[refine_key])

    xmin = min(wwig_err[measurement])
    xmax = max(wwig_err[measurement])

    plt.plot(wwig_err[measurement], wwig_err['error total'],
             marker=markers['wwig'],
             color=colors['wwig'], ls='', lw=lw, label='WWIG')
    plt.plot([xmin, xmax], ref_err_plt,
             color=colors['reference'], ls=':', lw=lw, label='Reference')
    plt.plot([xmin, xmax], cwwm_err_plt,
             color=colors['cwwm'], ls=':', lw=lw,
             label='CWWM')
    plt.plot([xmin, xmax], ana_err_plt,
             color=colors['analog'], ls=':', lw=lw, label='Analog')

    # labels
    ylabel = 'Relative Error'
    title = 'Surface Tally Relative Error'
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='best', ncol=2,
               fontsize='x-small')
    plt.tight_layout()

    save_name = 'images/relative_error_surface_{}.png'.format(refinement)
    plt.savefig(save_name)


if __name__ == '__main__':

    # get all output data
    all_data_files = glob.glob('csv/*_data.csv')
    df_output = pd.concat((
        pd.read_csv(f, header=0, index_col=0) for f in all_data_files),
        sort=False, ignore_index=True)

    # get coarseness data
    fdeci = 'csv/wwig_coarseness_measurements.csv'
    df_coarse = pd.read_csv(fdeci, header=0, index_col=0)

    # get roughness data
    all_rough_files = glob.glob('csv/wwig_roughness_measurements_*.csv')
    df_rough = pd.concat((
        pd.read_csv(f, header=0, index_col=0) for f in all_rough_files),
        sort=False, ignore_index=True)

    print(df_output.keys())
    print(df_coarse.keys())
    print(df_rough.keys())

    # plot tally results - as a function of wwig surface spacing
    plot_tally_ratios(df_output, pltratio=True, n_sigma=1)
    plot_tally_ratios(df_output, pltratio=True, n_sigma=2)
    plot_tally_ratios(df_output, pltratio=True, n_sigma=3)

    # plot ww efficiencies
    plot_ww_efficiency_ratio(df_output)

    # plot tally results vs coarseness / coarseness
    plot_tally_refinement(df_output, df_coarse, 'coarseness')
    plot_tally_refinement(df_output, df_rough, 'roughness')

    # ww efficiency vs roughness
    plot_ww_efficiency_refine(df_output, df_rough)

    # plot fom vs coarseness / coarseness
    plot_fom(df_output, df_coarse, 'coarseness')
    plot_fom(df_output, df_rough, 'roughness')

    # plot relative error for surface tally
    plot_relative_error_ratio(df_output)
    plot_relative_error_refine(df_output, df_coarse, 'coarseness')
    plot_relative_error_refine(df_output, df_rough, 'roughness')

    plt.show()
