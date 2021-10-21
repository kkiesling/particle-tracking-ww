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
    exterior_surfs = []
    for surf in all_surfs:
        surf_type = gfile._my_moab_core.tag_get_data(surf_type_tag, surf)
        if surf_type == 'interior':
            interior_surfs.append(surf)
        else:
            exterior_surfs.append(surf)

    return interior_surfs, exterior_surfs


def query_coarseness(gfile, interior_surfs, exterior_surfs, data):
    gq_i = dq.DagmcQuery(gfile, meshset=interior_surfs)
    gq_i.calc_coarseness()
    print('average coarseness (interior): {}'.format(
        gq_i._global_averages['coarseness_ave']))
    data['interior average coarseness'] = \
        gq_i._global_averages['coarseness_ave']

    # query coarseness on the exterior only
    gq_e = dq.DagmcQuery(gfile, meshset=exterior_surfs)
    gq_e.calc_coarseness()
    print('average coarseness (exterior): {}'.format(
        gq_e._global_averages['coarseness_ave']))
    data['exterior average coarseness'] = \
        gq_e._global_averages['coarseness_ave']

    # query coarseness on full geom
    gq = dq.DagmcQuery(gfile)
    gq.calc_coarseness()
    print('average coarseness (total): {}'.format(
        gq._global_averages['coarseness_ave']))
    data['total average coarseness'] = \
        gq._global_averages['coarseness_ave']

    coarse_list = []
    for i, surf in enumerate(interior_surfs):
        print('interior surface {}'.format(i))
        gq_s = dq.DagmcQuery(gfile, meshset=surf)
        gq_s.calc_coarseness()
        print('coarseness surf {}: {}'.format(
            i, gq_s._global_averages['coarseness_ave']))
        coarse_list.append(gq_s._global_averages['coarseness_ave'])
    # must be a set in order to add as a single item to dataframe
    data['interior coarseness'] = set(coarse_list)

    return data


def query_roughness(gfile, interior_surfs, data):

    # get roughness of interior surfs (total)
    gq_i = dq.DagmcQuery(gfile, meshset=interior_surfs)
    gq_i.calc_roughness()
    print('average roughness (all interior): {}'.format(
        gq_i._global_averages['roughness_ave']))
    data['interior average roughness'] = \
        gq_i._global_averages['roughness_ave']
    # get roughness and coarseness on each interior surf individually
    rough_list = []
    for i, surf in enumerate(interior_surfs):
        print('interior surface {}'.format(i))
        gq_s = dq.DagmcQuery(gfile, meshset=surf)
        gq_s.calc_roughness()
        print('roughness surf {}: {}'.format(
            i, gq_s._global_averages['roughness_ave']))
        rough_list.append(gq_s._global_averages['roughness_ave'])
    # must be a set in order to add as a single item to dataframe
    data['interior roughness'] = set(rough_list)
    return data


def iterate_ratios(fdir, mode, factor=None):

    ratio_data = []

    for rdir in os.listdir(fdir):
        ratio = int(rdir[1:])
        rpath = fdir + '/' + rdir

        for f in os.listdir(rpath):
            # don't analyze the viz ones or any vtks
            if f.split('.')[-1] != 'h5m':
                continue
            if 'noviz' not in f:
                continue
            fpath = rpath + '/' + f
            print(fpath)

            # initialize row for dataframe
            data = {}
            data['ratio'] = ratio
            data['mode'] = mode
            data['factor'] = factor
            egroup = int(f.split('_')[1])
            data['energy group'] = egroup

            # get file size
            fsize = os.path.getsize(fpath) / (1024.**2)
            data['size'] = fsize
            print('file size (MB): {}'.format(fsize))

            # make dagmcfile obj and get list of interior/exterior surfs
            gfile = df.DagmcFile(fpath)
            interior_surfs, exterior_surfs = get_interior_surfs(gfile)
            data['num interior surfs'] = len(interior_surfs)

            # query on the interior surfs only
            if mode in ['dc', 'default']:
                data = query_coarseness(
                    gfile, interior_surfs, exterior_surfs, data)

            if mode in ['sm', 'default']:
                data = query_roughness(
                    gfile, interior_surfs, data)

            # add data to full list
            ratio_data.append(data)

    return ratio_data


if __name__ == "__main__":

    fdir = sys.argv[1]  # folder to all wwigs '../wwigs/'

    # folders of wwigs to iterate over:
    folders = ['dc', 'sm', 'default']
    for mode in folders:
        all_data = []
        new_dir = fdir + '/' + mode
        if mode in ['dc', 'sm']:
            for factor_dir in os.listdir(new_dir):
                factor = float(factor_dir.split('0')[-1])
                factor_dir_long = new_dir + '/' + factor_dir

                ratio_data = iterate_ratios(factor_dir_long,
                                            mode, factor=factor)
                all_data.extend(ratio_data)
        else:
            ratio_data = iterate_ratios(new_dir, mode)
            all_data.extend(ratio_data)

        all_data_df = pd.DataFrame(all_data)
        all_data_df.to_csv('csv/wwig_{}_measurements.csv'.format(mode),
                           index_label='i')
