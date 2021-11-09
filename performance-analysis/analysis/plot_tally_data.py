import sys
import numpy as np
from matplotlib import legend
import pandas as pd
import glob
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter

colors = {'wwig': '#C11D59', 'analog': '#7CC145',
          'cwwm': '#247F03', 'reference': '#24E2A5'}
markers = {'wwig': 'd', 'cwwm': 'o',
           'analog': 'x', 'reference': 'X'}
ratios = [5, 6, 7, 8, 9, 10]
dpi = 600
lw = .9  # line width for plots
cs = 5  # error bar cap size
n_sigma = 1


def plot_tally_cwwm(df_output, refinement, df_measure=None, pltratio=True,
                    n_sigma=n_sigma):

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
    elif refinement == 'ratio':
        measurement = 'ratio'
        output_key = 'ratio'
        xlabel = 'WWIG Surface Spacing Ratio'

    plt.figure()

    ref_tally = df_output.loc[df_output['mode'] ==
                              'cwwm']['tally total']
    ref_err = df_output.loc[df_output['mode'] ==
                            'cwwm']['error total']

    # get reference values
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

    tally_vals = df_output.loc[df_output[output_key].notnull()][
        ['tally total', 'error total', output_key]]

    if df_measure is not None:
        # get measurement data for total only
        df_refine = df_measure.loc[df_measure['group'] == 'total'][
            [refine_key, measurement]]
        tally_vals = pd.merge(tally_vals, df_refine, how='left', left_on=[
            output_key], right_on=[refine_key])

    # tally ratio
    if pltratio:
        tally_vals['tally ratio total'] = tally_vals['tally total'] / \
            float(ref_tally)

    # get error bars for ratio
    if pltratio:
        m2 = float(ref_tally)
        e2 = float(ref_err)

        # wwig
        m1 = tally_vals['tally total']
        e1 = tally_vals['error total']
        s1 = m1 * e1
        s2 = m2 * e2
        yerr = np.sqrt((s1 / m2)**2 + (m1 * s2 / (m2 * m2))**2) * n_sigma

    else:
        yerr = tally_vals['tally total'] * tally_vals['error total'] * n_sigma

    if pltratio:
        y = tally_vals['tally ratio total']
    else:
        y = tally_vals['tally total']

    xmax = max(tally_vals[measurement])
    xmin = min(tally_vals[measurement])

    plt.errorbar(tally_vals[measurement], y, yerr=yerr,
                 marker=markers['wwig'], lw=lw, capsize=cs, ls='',
                 color=colors['wwig'], label='WWIG/CWWM')

    plt.plot([xmin, xmax], ref_tally_plt,
             color=colors['cwwm'], ls='-', lw=lw, label='WWIG/CWWM$= 1$')
    plt.plot([xmin, xmax], ref_sigma_plt_n,
             color=colors['cwwm'], ls=':', lw=lw,
             label='WWIG/CWWM $=1 \pm {} \sigma$'.format(n_sigma))
    plt.plot([xmin, xmax], ref_sigma_plt_p,
             color=colors['cwwm'], ls=':', lw=lw, label='')

    # labels
    ylabel = 'Tally (WWIG/CWWM)'
    title = 'Surface Tally Results'
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='best', ncol=1,
               fontsize='x-small')
    plt.tight_layout()

    save_name = 'images/surface_tally_results_cwwm_ratios_{}_{}.png'.format(
        n_sigma, refinement)
    plt.savefig(save_name)


def plot_tally(df_output, refinement, df_measure=None, pltratio=True,
               n_sigma=n_sigma):

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
    elif refinement == 'ratio':
        measurement = 'ratio'
        output_key = 'ratio'
        xlabel = 'WWIG Surface Spacing Ratio'

    plt.figure()

    ref_tally = df_output.loc[df_output['mode'] ==
                              'reference']['tally total']
    ref_err = df_output.loc[df_output['mode'] ==
                            'reference']['error total']

    cwwm_tally = df_output.loc[df_output['mode'] ==
                               'cwwm']
    ana_tally = df_output.loc[df_output['mode'] ==
                              'analog']

    # get reference values
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

    tally_vals = df_output.loc[df_output[output_key].notnull()][
        ['tally total', 'error total', output_key]]

    if df_measure is not None:
        # get measurement data for total only
        df_refine = df_measure.loc[df_measure['group'] == 'total'][
            [refine_key, measurement]]
        tally_vals = pd.merge(tally_vals, df_refine, how='left', left_on=[
            output_key], right_on=[refine_key])

    # tally ratio
    if pltratio:
        tally_vals['tally ratio total'] = tally_vals['tally total'] / \
            float(ref_tally)
        cwwm_tally['tally ratio total'] = cwwm_tally['tally total'] / \
            float(ref_tally)
        ana_tally['tally ratio total'] = ana_tally['tally total'] / \
            float(ref_tally)

    # get error bars for ratio
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

    if refinement == 'roughness':
        ext = 1.03
    else:
        ext = 1.1
    xmax = max(tally_vals[measurement]) * ext
    xmin = min(tally_vals[measurement])

    plt.errorbar(tally_vals[measurement], y, yerr=yerr,
                 marker=markers['wwig'], lw=lw, capsize=cs, ls='',
                 color=colors['wwig'], label='WWIG/Ref')
    plt.errorbar([xmax], cwwm_y, yerr=y_cwwm_err,
                 marker=markers['cwwm'], lw=lw, capsize=cs, ls='',
                 color=colors['cwwm'], label='CWWM/Ref')
    plt.errorbar([xmax], ana_y, yerr=y_ana_err,
                 marker=markers['analog'], lw=lw, capsize=cs, ls='',
                 color=colors['analog'], label='Analog/Ref')
    plt.plot([xmin, xmax], ref_tally_plt,
             color=colors['reference'], ls='-', lw=lw, label='E/Ref$=1$')
    plt.plot([xmin, xmax], ref_sigma_plt_n,
             color=colors['reference'], ls=':', lw=lw,
             label='E/Ref $\pm {} \sigma$'.format(n_sigma))
    plt.plot([xmin, xmax], ref_sigma_plt_p,
             color=colors['reference'], ls=':', lw=lw, label='')

    # labels
    ylabel = 'Tally (Experimental/Reference)'
    title = 'Surface Tally Results'
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='best', ncol=2,
               fontsize='x-small')
    plt.tight_layout()

    save_name = 'images/surface_tally_results_ratios_{}_{}.png'.format(
        n_sigma, refinement)
    plt.savefig(save_name)


def plot_ww_efficiency(df_output, refinement, df_measure=None):
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
    elif refinement == 'ratio':
        measurement = 'ratio'
        output_key = 'ratio'
        xlabel = 'WWIG Surface Spacing Ratio'

    if df_measure is not None:
        df_out = df_output.loc[
            df_output['mode'] == 'wwig'].loc[
                df_output[output_key].notnull()]
        df_refine = df_measure.loc[df_measure['group'] == 'total'][
            [measurement, refine_key]]
        df_wwig = pd.merge(df_out, df_refine, how='left',
                           left_on=[output_key], right_on=[refine_key])
    else:
        df_wwig = df_output.loc[df_output['mode'] ==
                                'wwig'].loc[df_output[output_key].notnull()]

    # plot
    fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True,
                           sharey=False, figsize=(5, 8))

    ax[0].plot(df_wwig[measurement], df_wwig['Splits < C_u'],
               marker=markers['wwig'], ls='', label='WWIG',
               color=colors['wwig'])
    ax[0].set_ylabel('$f_{< C_U}$')

    ax[1].plot(df_wwig[measurement], df_wwig['Splits = C_u'],
               marker=markers['wwig'], ls='', label='',
               color=colors['wwig'])
    ax[1].set_ylabel('$f_{= C_U}$')

    ax[2].plot(df_wwig[measurement], df_wwig['Splits > C_u'],
               marker=markers['wwig'], ls='', label='',
               color=colors['wwig'])
    ax[2].set_xlabel(xlabel)
    ax[2].set_ylabel('$f_{> C_U}$')

    if df_measure is None:
        # also plot cwwm results
        xmax = max(df_wwig[output_key])
        xmin = min(df_wwig[output_key])
        df_cwwm = df_output.loc[df_output['mode'] == 'cwwm']
        cwwm_lt = np.full(2, float(df_cwwm['Splits < C_u']))
        cwwm_eq = np.full(2, float(df_cwwm['Splits = C_u']))
        cwwm_gt = np.full(2, float(df_cwwm['Splits > C_u']))
        ax[0].plot([xmin, xmax], cwwm_lt, marker='',
                   ls=':', color=colors['cwwm'], label='CWWM')
        ax[1].plot([xmin, xmax], cwwm_eq, marker='',
                   ls=':', color=colors['cwwm'])
        ax[2].plot([xmin, xmax], cwwm_gt, marker='',
                   ls=':', color=colors['cwwm'])
        fig.legend(bbox_to_anchor=(0.5, 0), loc='lower center', ncol=2,
                   fontsize='x-small')

    # labels
    title = 'Splitting Efficiency'
    fig.suptitle(title, fontsize='x-large')
    fig.tight_layout(pad=2.5, h_pad=0)
    save_name = 'images/ww_efficiency_{}.png'.format(refinement)
    plt.savefig(save_name)

    save_name = 'images/split_efficiency_{}.png'.format(refinement)
    plt.savefig(save_name)

    # overall efficiency
    fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True,
                           sharey=False, figsize=(6, 8))

    # plot overall efficiency
    ax[0].plot(df_wwig[measurement], df_wwig['WW check efficiency'],
               marker=markers['wwig'], ls='',
               label='Overall Efficiency', color=colors['wwig'])
    ax[0].set_ylabel('$\eta_{ww}$')

    ax[1].plot(df_wwig[measurement], df_wwig['total ww checks'] / 10**6,
               marker=markers['reference'], ls='',
               label='Total Checks', color=colors['wwig'])
    ax[1].set_ylabel(r'Total WW Checks ($\times 10^6$)')

    ax[2].plot(df_wwig[measurement], df_wwig['total splits'] / 10**6,
               marker=markers['cwwm'], ls='',
               label='Splits', color=colors['reference'])
    ax[2].set_xlabel(xlabel)
    ax[2].set_ylabel(r'Splits ($\times 10^6$)')

    ax2 = ax[2].twinx()
    ax2.plot(df_wwig[measurement],
             df_wwig['total stochastic termination'] / 10**6,
             marker=markers['analog'], ls='',
             label='Stochatistic Termination', color=colors['analog'])
    ax2.set_ylabel(r'Stochastic Termination ($\times 10^6$)')

    if df_measure is None:
        # also plot cwwm results
        xmax = max(df_wwig[output_key])
        xmin = min(df_wwig[output_key])
        df_cwwm = df_output.loc[df_output['mode'] == 'cwwm']
        cwwm_ww = np.full(2, float(df_cwwm['WW check efficiency']))
        cwwm_total = np.full(2, float(df_cwwm['total ww checks'] / 10**6))
        cwwm_splits = np.full(2, float(df_cwwm['total splits'] / 10**6))
        cwwm_term = np.full(
            2, float(df_cwwm['total stochastic termination'] / 10**6))
        ax[0].plot([xmin, xmax], cwwm_ww, marker='',
                   ls=':', color=colors['cwwm'], label='CWWM')
        ax[1].plot([xmin, xmax], cwwm_total, marker='',
                   ls=':', color=colors['cwwm'], label='')
        ax[2].plot([xmin, xmax], cwwm_splits, marker='',
                   ls=':', color=colors['cwwm'], label='')
        ax2.plot([xmin, xmax], cwwm_term, marker='',
                 ls='', color=colors['cwwm'], label='')

    title = 'Weight Window Efficiency'
    fig.suptitle(title, fontsize='x-large')
    fig.legend(bbox_to_anchor=(0.5, 0), loc='lower center', ncol=5,
               fontsize='x-small')
    fig.tight_layout(pad=2.5, h_pad=0)
    save_name = 'images/ww_efficiency_{}.png'.format(refinement)
    plt.savefig(save_name)

    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    if df_measure is None:
        # also plot cwwm results
        xmax = max(df_wwig[output_key])
        xmin = min(df_wwig[output_key])
        df_cwwm = df_output.loc[df_output['mode'] == 'cwwm']
        cwwm_create = np.full(2, float(df_cwwm['ww creation']) / 10**5)
        cwwm_loss = np.full(2, float(df_cwwm['ww loss']) / 10**5)
        ax.plot([xmin, xmax], cwwm_create, marker='',
                ls=':', color=colors['cwwm'], label='CWWM')
        ax2.plot([xmin, xmax], cwwm_loss, marker='',
                 ls='', color=colors['cwwm'], label='')

    ax.plot(df_wwig[measurement], df_wwig['ww creation'] / 10**5,
            marker=markers['wwig'], ls='',
            label='Creation', color=colors['wwig'])
    ax.set_ylabel(r'Neutron Creation ($\times 10^5$)')
    ax.set_xlabel(xlabel)
    ax2.plot(df_wwig[measurement],
             df_wwig['ww loss'] / 10**5,
             marker=markers['analog'], ls='',
             label='Loss', color=colors['analog'])
    ax2.set_ylabel(r'Neutron Loss ($\times 10^5$)')

    fig.suptitle('Neutron Creation/Loss by Weight Window')
    fig.legend(bbox_to_anchor=(0.5, 0), loc='lower center', ncol=3,
               fontsize='x-small')
    fig.tight_layout(pad=2.5)
    save_name = 'images/ww_creationloss_{}.png'.format(refinement)
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
    df_tally = df_output.loc[df_output[output_key].notnull()][
        ['fom', output_key, 'cpu time', 'error total', 'vov']]

    df_tally['fom error'] = (2. * df_tally['vov']**0.5) / \
        (df_tally['error total']**2 * df_tally['cpu time'])

    # get measurement data for total only
    df_refine = df_measure.loc[df_measure['group'] == 'total'][
        [refine_key, measurement]]

    # join with the measurement tally on the output_key and refine_key
    df = pd.merge(df_tally, df_refine, how='left', left_on=[
                  output_key], right_on=[refine_key])

    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True,
                           sharey=False, figsize=(5, 6))

    ax[0].errorbar(df[measurement], df['fom'], yerr=df['fom error'],
                   marker=markers['wwig'], ls='', lw=lw, capsize=cs,
                   color=colors['wwig'], label='WWIG')
    ax[0].set_ylabel('Figure of Merit')
    ax[1].plot(df[measurement], df['cpu time'], marker=markers['wwig'], ls='',
               color=colors['wwig'], label='WWIG')
    ax[1].set_ylabel('CPU time (min)')

    # labels
    title = 'Performance'
    plt.suptitle(title)
    plt.xlabel(xlabel)
    plt.tight_layout(pad=2.7, w_pad=.5)
    save_name = 'images/fom_{}.png'.format(refinement)
    plt.savefig(save_name)


def plot_fom_ratio(df_output):

    # get the output data for total tally
    df = df_output.loc[df_output['ratio'].notnull()][
        ['fom', 'ratio', 'cpu time', 'error total', 'vov']]

    df['fom error'] = (2. * df['vov']**0.5) / \
        (df['error total']**2 * df['cpu time'])

    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True,
                           sharey=False, figsize=(5, 6))

    ax[0].errorbar(df['ratio'], df['fom'], yerr=df['fom error'],
                   marker=markers['wwig'], ls='', lw=lw, capsize=cs,
                   color=colors['wwig'], label='WWIG')
    ax[0].set_ylabel('Figure of Merit')
    ax[1].plot(df['ratio'], df['cpu time'], marker=markers['wwig'], ls='',
               color=colors['wwig'], label='WWIG')
    ax[1].set_ylabel('CPU time (min)')

    # labels
    title = 'Performance'
    plt.suptitle(title)
    plt.xlabel('WWIG Surface Spacing Ratio')
    plt.tight_layout(pad=2.7, w_pad=.5)
    save_name = 'images/fom_ratio.png'
    plt.savefig(save_name)


def plot_relative_error(df_output, refinement, df_measure=None):
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
    elif refinement == 'ratio':
        measurement = 'ratio'
        output_key = 'ratio'
        xlabel = 'WWIG Surface Spacing Ratio'

    plt.figure()

    ref_err = df_output.loc[df_output['mode'] ==
                            'reference'][['error total', 'vov']]
    cwwm_err = df_output.loc[df_output['mode'] ==
                             'cwwm'][['error total', 'vov']]
    ana_err = df_output.loc[df_output['mode'] ==
                            'analog'][['error total', 'vov']]
    # get error of relative error
    ref_err['vov error'] = ref_err['vov']**0.5 * ref_err['error total']
    cwwm_err['vov error'] = cwwm_err['vov']**0.5 * cwwm_err['error total']
    ana_err['vov error'] = ana_err['vov']**0.5 * ana_err['error total']

    # get measurement data for total only
    if df_measure is not None:
        df_out = df_output.loc[
            df_output['mode'] == 'wwig'].loc[
                df_output[output_key].notnull()]
        df_refine = df_measure.loc[df_measure['group'] == 'total'][
            [measurement, refine_key]]
        df_wwig = pd.merge(df_out, df_refine, how='left',
                           left_on=[output_key], right_on=[refine_key])
    else:
        df_wwig = df_output.loc[df_output['mode'] ==
                                'wwig'].loc[df_output[output_key].notnull()]

    wwig_err = df_wwig[['error total', measurement, 'vov']]
    wwig_err['vov error'] = wwig_err['vov']**0.5 * wwig_err['error total']

    if refinement == 'roughness':
        ext = 1.03
    else:
        ext = 1.1
    xmax = max(wwig_err[measurement]) * ext

    plt.errorbar(wwig_err[measurement], wwig_err['error total'],
                 yerr=wwig_err['vov error'],
                 marker=markers['wwig'],
                 color=colors['wwig'], ls='', lw=lw, capsize=cs,
                 label='WWIG')
    plt.errorbar([xmax], ref_err['error total'], yerr=ref_err['vov error'],
                 color=colors['reference'], ls='-', lw=lw, label='Reference',
                 marker=markers['reference'], capsize=cs)
    plt.errorbar([xmax], cwwm_err['error total'], yerr=cwwm_err['vov error'],
                 color=colors['cwwm'], ls='-', lw=lw, label='CWWM',
                 marker=markers['cwwm'], capsize=cs)
    plt.errorbar([xmax], ana_err['error total'], yerr=ana_err['vov error'],
                 color=colors['analog'], ls='-', lw=lw, label='Analog',
                 marker=markers['analog'], capsize=cs)

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

    # update the perturbation/decimation info on the r=8 ratio entry
    df_output.loc[df_output['ratio'] == 8, 'perturbation'] = 0.0
    df_output.loc[df_output['ratio'] == 8, 'decimation'] = 0.0

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

    # plot tally results
    # plot_tally(df_output, 'ratio', pltratio=True, n_sigma=1)
    # plot_tally(df_output, 'ratio', pltratio=True, n_sigma=2)
    plot_tally(df_output, 'ratio', pltratio=True, n_sigma=3)

    # plot_tally(df_output, 'roughness',
    #            df_measure=df_rough, pltratio=True, n_sigma=1)
    # plot_tally(df_output, 'roughness',
    #            df_measure=df_rough, pltratio=True, n_sigma=2)
    plot_tally(df_output, 'roughness',
               df_measure=df_rough, pltratio=True, n_sigma=3)

    # plot_tally(df_output, 'coarseness',
    #            df_measure=df_coarse, pltratio=True, n_sigma=1)
    # plot_tally(df_output, 'coarseness',
    #            df_measure=df_coarse, pltratio=True, n_sigma=2)
    plot_tally(df_output, 'coarseness',
               df_measure=df_coarse, pltratio=True, n_sigma=3)

    # plot tally results
    # plot_tally_cwwm(df_output, 'ratio', pltratio=True, n_sigma=1)
    # plot_tally_cwwm(df_output, 'ratio', pltratio=True, n_sigma=2)
    plot_tally_cwwm(df_output, 'ratio', pltratio=True, n_sigma=3)

    # plot_tally_cwwm(df_output, 'roughness',
    #                 df_measure=df_rough, pltratio=True, n_sigma=1)
    # plot_tally_cwwm(df_output, 'roughness',
    #                 df_measure=df_rough, pltratio=True, n_sigma=2)
    plot_tally_cwwm(df_output, 'roughness',
                    df_measure=df_rough, pltratio=True, n_sigma=3)

    # plot_tally_cwwm(df_output, 'coarseness',
    #                 df_measure=df_coarse, pltratio=True, n_sigma=1)
    # plot_tally_cwwm(df_output, 'coarseness',
    #                 df_measure=df_coarse, pltratio=True, n_sigma=2)
    plot_tally_cwwm(df_output, 'coarseness',
                    df_measure=df_coarse, pltratio=True, n_sigma=3)

    # plot ww efficiencies
    plot_ww_efficiency(df_output, 'ratio')
    plot_ww_efficiency(df_output, 'roughness', df_measure=df_rough)
    plot_ww_efficiency(df_output, 'coarseness', df_measure=df_coarse)

    # plot fom vs coarseness / coarseness
    plot_fom(df_output, df_coarse, 'coarseness')
    plot_fom(df_output, df_rough, 'roughness')
    plot_fom_ratio(df_output)

    # plot relative error for surface tally
    plot_relative_error(df_output, 'ratio')
    plot_relative_error(df_output, 'coarseness', df_measure=df_coarse)
    plot_relative_error(df_output, 'roughness', df_measure=df_rough)

    plt.show()
