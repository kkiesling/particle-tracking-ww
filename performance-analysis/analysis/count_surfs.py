import dagmc_stats.DagmcFile as df
import sys
import os
from pymoab import types
import pandas as pd
import matplotlib.pyplot as plt


def get_interior_surfs(gfile):
    """get only the set of surfaces that are interior"""
    all_surfs = gfile.entityset_ranges['surfaces']
    surf_type_tag = \
        gfile._my_moab_core.tag_get_handle('SURF_TYPE', size=32,
                                           tag_type=types.MB_TYPE_OPAQUE,
                                           storage_type=types.MB_TAG_SPARSE,
                                           create_if_missing=False)
    interior_surfs = []
    for surf in all_surfs:
        surf_type = gfile._my_moab_core.tag_get_data(surf_type_tag, surf)
        if surf_type == 'interior':
            interior_surfs.append(surf)

    return interior_surfs


def query_surfs(fdir, ratio):
    all_data = []
    total = 0
    for group in range(27):
        data = {}
        ID = '{:03d}'.format(group)
        fpath = fdir + '/wwn_{}.h5m'.format(ID)
        dgf = df.DagmcFile(fpath)
        interior_surfs = get_interior_surfs(dgf)
        data['num interior'] = len(interior_surfs)
        total += len(interior_surfs)
        data['group'] = int(group)
        data['ratio'] = ratio
        all_data.append(data)

    data = {}
    data['num interior'] = total
    data['group'] = 'total'
    data['ratio'] = ratio
    all_data.append(data)

    return all_data


def plot_surfs(df, group=None):

    df_total = df.loc[df['group'] == 'total']
    plt.plot(df_total['ratio'], df_total['num interior'], marker='o', ls='')
    plt.show()


if __name__ == "__main__":

    fdir = sys.argv[1]  # path to ratio dir

    all_data = []
    for rdir in os.listdir(fdir):
        ratio = int(rdir[1:])
        fpath = fdir + '/' + rdir + '/geoms/'

        data = query_surfs(fpath, ratio)
        all_data.extend(data)

    all_data_df = pd.DataFrame(all_data)
    #print(all_data_df)

    all_data_df.to_csv('csv/ratio_surfs.csv', index_label='i')

    plot_surfs(all_data_df)

