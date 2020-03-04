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

    zmesh = mesh.Mesh(mesh=zfile, structured=True)
    zvals = zmesh.zval[:]
    zvals = zvals[zvals != -1.0]

    return zvals


def get_name(zfile):
    """Strings for title and save names."""

    ref_name = zfile.split('-')[0]
    comp_name = zfile.split('-')[1]

    save_name = ref_name + '-' + comp_name

    if ref_name == 'analog':
        first = 'Analog'
    elif ref_name == 'wwinp':
        first = 'Cartesian WW Mesh'
    elif ref_name == 'wwig':
        first = 'WWIG'

    if comp_name == 'analog':
        second = 'Analog'
    elif comp_name == 'wwinp':
        second = 'Cartesian WW Mesh'
    elif comp_name == 'wwig':
        second = 'WWIG'

    title = first + ' vs. ' + second

    return save_name, title


def count_z(data):
    """get % for z <= 2"""

    nz = float(len(data))

    # CHANGE THIS VALUE FOR DIFFERENT SIGMA COUNT
    z2 = data[data <= 3.0]
    n2 = float(len(z2))
    percent = n2/nz*100.
    return percent


if __name__ == '__main__':

    legends = []
    zdata = []
    for zfile in sys.argv[1:]:
        save_name, title = get_name(zfile)
        legends.append(title)
        zvals = get_data(zfile)
        zdata.append(zvals)

    colors = ['r', 'b', 'g']
    bins = np.linspace(0, 3, num=51)

    # plot PDFs
    for i, zvals in enumerate(zdata):
        plot_dens_pdf(bins, zvals, legends[i], colors[i])

    plt.xlim([0, bins[-1]])
    plt.xlabel('z-score')
    plt.ylabel('PDF')
    plt.title('Z-Score Probability Distribution Function')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('PDF.png')
    plt.clf()

    # plot CDFs
    for i, zvals in enumerate(zdata):
        plot_dens_cdf(bins, zvals, legends[i], colors[i])

    plt.xlim([0, bins[-1]])
    plt.xlabel('z-score')
    plt.ylabel('CDF')
    plt.title('Z-Score Cumulative Distribution Function')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig('CDF.png')
    plt.clf()

    # count z value
    for zvals in zdata:
        p = count_z(zvals)
        print(p)
