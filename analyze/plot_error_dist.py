from pyne import mesh
import sys
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


def plot_dens_pdf(bins, data, title, color):
    vals = np.clip(data, bins[0], bins[-1])
    sns.distplot(vals, kde=True, hist=False,
             color = color, label=title)

def plot_dens_cdf(bins, data, title, color):
    vals = list(np.clip(data, bins[0], bins[-1]))
    vals = np.clip(data, bins[0], bins[-1])
    sns.distplot(vals, kde=True, hist=False,
             color = color, label=title, kde_kws={"cumulative": True})

def get_data(zfile):
    """Get only data that is not -1"""

    zmesh = mesh.Mesh(mesh=zfile)
    zvals = zmesh.neutron_result_total_rel_error[zmesh.neutron_result_total_rel_error[:] > 0]
    #zvals[zvals[:] == 0] = -1
    print(zvals)
    return zvals


def get_name(meshfile):
    """Strings for title and save names."""

    name = meshfile.split('/')[1].split('-')[0]

    if name == 'analog':
        title = 'Analog'
    elif name == 'wwinp':
        title = 'Cartesian WW Mesh'
    elif name == 'wwig':
        title = 'WWIG'
    else:
        title = 'results'

    return name, title


if __name__ == '__main__':

    legends = []
    zdata = []

    # zmesh == regular meshtal files

    for zfile in sys.argv[1:]:
        save_name, title = get_name(zfile)
        legends.append(title)
        zvals = get_data(zfile)
        zdata.append(zvals)

    colors = ['r', 'b', 'g']
    bins = np.linspace(0, 1, num=51)

    # plot PDFs
    for i, zvals in enumerate(zdata):
        plot_dens_pdf(bins, zvals, legends[i], colors[i])

    plt.xlim([0, bins[-1]])
    plt.xlabel('relative error R')
    plt.ylabel('PDF')
    plt.title('Relative Error\n Probability Distribution Function')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('rel-error-PDF.png')
    plt.clf()

    # # plot CDFs
    # for i, zvals in enumerate(zdata):
    #     plot_dens_cdf(bins, zvals, legends[i], colors[i])
    #
    # plt.xlim([0, bins[-1]])
    # plt.xlabel('relative error R')
    # plt.ylabel('CDF')
    # plt.title('Relative Error\n Cumulative Distribution Function')
    # plt.legend(loc='best')
    # plt.tight_layout()
    # #plt.savefig('rel-error-CDF.png')
    # plt.clf()

    plt.show()
