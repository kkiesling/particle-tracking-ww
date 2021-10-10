from pyne import mesh
import sys
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


def plot_dens_pdf(bins, data, title, color):
    vals = np.clip(data, bins[0], bins[-1])
    sns.distplot(vals, kde=True, hist=True, norm_hist=True,
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


def get_name(meshfile):
    """Strings for title and save names."""

    # name = meshfile.split('/')[1].split('-')[0]
    # if name == 'analog':
    #     title = 'Analog'
    # elif name == 'wwinp':
    #     title = 'Cartesian WW Mesh'
    # elif name == 'wwig':
    #     title = 'WWIG'

    name = 'rel_err_plot'
    title = 'relative error'

    return name, title


if __name__ == '__main__':

    legends = []
    all_data = []

    # files should be the h5m files for the meshtally

    for fh5m in sys.argv[1:]:
        save_name, title = get_name(fh5m)
        legends.append(title)
        data = get_data(fh5m)
        all_data.append(data)

    colors = ['r', 'b', 'g']
    bins = np.linspace(0.0, 1.0, num=11)

    # plot PDFs
    for i, data in enumerate(all_data):
        plot_dens_pdf(bins, data, legends[i], colors[i])

    plt.xlim([0, bins[-1]])
    plt.xlabel('relative error R')
    plt.ylabel('PDF')
    plt.title('Relative Error\n Probability Distribution Function')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('rel-error-PDF.png')
    plt.clf()

    # plot CDFs
    for i, data in enumerate(all_data):
        plot_dens_cdf(bins, data, legends[i], colors[i])

    plt.xlim([0, bins[-1]])
    plt.xlabel('relative error R')
    plt.ylabel('CDF')
    plt.title('Relative Error\n Cumulative Distribution Function')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('rel-error-CDF.png')
    plt.clf()

    #plt.show()
