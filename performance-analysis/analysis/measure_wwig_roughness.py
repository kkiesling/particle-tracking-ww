import dagmc_stats.DagmcFile as df
import dagmc_stats.DagmcQuery as dq
import sys
import os
from pymoab import types
import pandas as pd


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


def query_roughness(fdir, factor):
    all_data = []
    group_ave = []
    for group in range(27):
        data = {}
        ID = '{:03d}'.format(group)
        fpath = fdir + '/wwn_{}.h5m'.format(ID)
        dgf = df.DagmcFile(fpath)
        interior_surfs = get_interior_surfs(dgf)
        dgq = dq.DagmcQuery(dgf, meshset=interior_surfs)
        dgq.calc_roughness()
        print('average roughness {} {}: {}'.format(
            factor, ID, dgq._global_averages['roughness_ave']))
        data['average roughness'] = dgq._global_averages['roughness_ave']
        data['group'] = int(group)
        data['perturbation'] = float(factor)
        all_data.append(data)
        group_ave.append(dgq._global_averages['roughness_ave'])

    ave = sum(group_ave) / float(len(group_ave))
    print('factor average roughness {}: {}'.format(factor, ave))
    data = {}
    data['average roughness'] = ave
    data['group'] = 'total'
    data['perturbation'] = float(factor)
    all_data.append(data)

    return all_data


if __name__ == "__main__":

    fdir = sys.argv[1]  # path to a single factor folder
    factor_string = fdir.strip('/').split('/')[-1]
    print(factor_string)

    if factor_string == 'geoms':
        factor = 0.0
    else:
        factor = float(factor_string)
    all_data = query_roughness(fdir, factor)

    all_data_df = pd.DataFrame(all_data)
    all_data_df.to_csv('csv/wwig_roughness_measurements_{}.csv'.format(factor),
                       index_label='i')
