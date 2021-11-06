from operator import sub
from pyne import mesh
import sys
import os
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


wwig_colors = ['#F3B4CB', '#EA84AA', '#FF5A96', '#FF0A64', '#C11D59',
               '#86284A', '#653345', '#67072A', '#3C0346', '#60226B',
               '#831596', '#814A8A', '#B106CE', '#BE58D0', '#DF9EEA',
               '#F6C1FF']
colors = {'wwig': '#C11D59', 'analog': '#7CC145',
          'cwwm': '#247F03', 'reference': '#24E2A5'}


def plot_dens_pdf(bins, data, title, color):
    vals = np.clip(data, bins[0], bins[-1])
    sns.distplot(vals, kde=True, hist=False, norm_hist=True,
                 color=color, label=title)


def plot_dens_cdf(bins, data, title, color):
    vals = list(np.clip(data, bins[0], bins[-1]))
    vals = np.clip(data, bins[0], bins[-1])
    sns.distplot(vals, kde=True, hist=False, norm_hist=True,
                 color=color, label=title, kde_kws={"cumulative": True})


def get_data(fh5m):
    m = mesh.Mesh(mesh=fh5m, structured=True)
    data = m.neutron_result_total_rel_error[:]
    return data


def get_name(fh5m):
    """Strings for title and save names."""
    name = fh5m.split('_')[0]
    if name == 'analog':
        label = 'Analog'
    elif name == 'cwwm':
        label = 'CWWM'
    elif name == 'reference':
        label = 'Reference'
    return name, label


if __name__ == '__main__':

    legends = {}
    all_data = {}

    results_dir = sys.argv[1]
    bins = np.linspace(0.0, 1.0, num=11)

    # plot analog, ref, and cwwm
    for mode in ['analog', 'reference', 'cwwm']:
        fh5m = mode + '_meshtal.h5m'
        fpath = results_dir + '/' + mode + '/' + fh5m
        name, label = get_name(fh5m)
        data = get_data(fpath)
        plot_dens_pdf(bins, data, label, colors[name])

    # plot wwig ratios in list
    ratio_dir = results_dir + '/wwigs/ratios/'
    for ratio in range(5, 11):
        fh5m = 'ratio_{}_meshtal.h5m'.format(ratio)
        fpath = ratio_dir + '/r{}/'.format(ratio) + fh5m
        data = get_data(fpath)
        label = 'WWIG r={}'.format(ratio)
        color = wwig_colors[ratio - 5]
        plot_dens_pdf(bins, data, label, color)

    plt.xlim([0, bins[-1]])
    plt.xlabel('Relative Error R')
    plt.ylabel('Number of mesh voxels')
    plt.title('Relative Error\n Probability Distribution Function')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('images/rel-error-PDF.png')
    plt.clf()

    # plot analog, ref, and cwwm
    for mode in ['analog', 'reference', 'cwwm']:
        fh5m = mode + '_meshtal.h5m'
        fpath = results_dir + '/' + mode + '/' + fh5m
        name, label = get_name(fh5m)
        data = get_data(fpath)
        plot_dens_cdf(bins, data, label, colors[name])

    # plot wwig ratios in list
    for ratio in range(5, 11):
        fh5m = 'ratio_{}_meshtal.h5m'.format(ratio)
        fpath = ratio_dir + '/r{}/'.format(ratio) + fh5m
        data = get_data(fpath)
        label = 'WWIG r={}'.format(ratio)
        color = wwig_colors[ratio - 5]
        plot_dens_cdf(bins, data, label, color)

    plt.xlim([0, bins[-1]])
    plt.xlabel('Relative Error R')
    plt.ylabel('Fraction of mesh voxel <= R')
    plt.title('Relative Error\n Cumulative Distribution Function')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('images/rel-error-CDF.png')
    plt.clf()

    # plot wwig as a function of decimation factor
    deci_dir = results_dir + '/wwigs/decimate/'
    for factor in range(1, 9):
        fh5m = 'decimate_0.{}_meshtal.h5m'.format(factor)
        fpath = deci_dir + '/0.{}/'.format(factor) + fh5m
        data = get_data(fpath)
        label = 'f=0.{}'.format(factor)
        color = wwig_colors[factor - 1]
        plot_dens_pdf(bins, data, label, color)

    plt.xlim([0, bins[-1]])
    plt.xlabel('Relative Error R')
    plt.ylabel('Number of mesh voxels')
    plt.title('Decimation Relative Error\n Probability Distribution Function')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('images/rel-error-PDF-deci.png')
    plt.clf()

    for factor in range(1, 9):
        fh5m = 'decimate_0.{}_meshtal.h5m'.format(factor)
        fpath = deci_dir + '/0.{}/'.format(factor) + fh5m
        data = get_data(fpath)
        label = 'f={}'.format(factor)
        color = wwig_colors[factor - 1]
        plot_dens_cdf(bins, data, label, color)

    plt.xlim([0, bins[-1]])
    plt.xlabel('Relative Error R')
    plt.ylabel('Fraction of mesh voxel <= R')
    plt.title('Decimation Relative Error\n Cumulative Distribution Function')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('images/rel-error-CDF-deci.png')
    plt.clf()

    # plot wwig as a function of roughness perturbation
    deci_dir = results_dir + '/wwigs/rough/'
    flist = [0.1, 0.2, 0.3, 0.5, 0.6, 0.7,
             0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
    for factor in flist:
        fh5m = 'rough_{}_meshtal.h5m'.format(factor)
        fpath = deci_dir + '/{}/'.format(factor) + fh5m
        data = get_data(fpath)
        label = 'p={}'.format(factor)
        color = wwig_colors[int(factor * 10 - 1)]
        plot_dens_pdf(bins, data, label, color)

    plt.xlim([0, bins[-1]])
    plt.xlabel('Relative Error R')
    plt.ylabel('Number of mesh voxels')
    plt.title('Roughness Relative Error\n Probability Distribution Function')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('images/rel-error-PDF-rough.png')
    plt.clf()

    for factor in flist:
        fh5m = 'rough_{}_meshtal.h5m'.format(factor)
        fpath = deci_dir + '/{}/'.format(factor) + fh5m
        data = get_data(fpath)
        label = 'p={}'.format(factor)
        color = wwig_colors[int(factor * 10 - 1)]
        plot_dens_cdf(bins, data, label, color)

    plt.xlim([0, bins[-1]])
    plt.xlabel('Relative Error R')
    plt.ylabel('Fraction of mesh voxel <= R')
    plt.title('Roughness Relative Error\n Cumulative Distribution Function')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('images/rel-error-CDF-rough.png')
    plt.clf()
