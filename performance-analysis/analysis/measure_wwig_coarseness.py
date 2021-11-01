import dagmc_stats.DagmcFile as df
import dagmc_stats.DagmcQuery as dq
import sys
import os
from pymoab import types
import pandas as pd


def query_coarseness(fdir, factor):
    all_data = []
    group_ave = []
    size_total = 0.
    for group in range(27):
        data = {}
        ID = '{:03d}'.format(group)
        fpath = fdir + '/wwn_{}.h5m'.format(ID)
        dgf = df.DagmcFile(fpath)
        dgq = dq.DagmcQuery(dgf)
        dgq.calc_coarseness()
        print('average coarseness {} {}: {}'.format(
            factor, ID, dgq._global_averages['coarseness_ave']))
        data['average coarseness'] = dgq._global_averages['coarseness_ave']
        data['group'] = int(group)
        data['dc factor'] = float(factor)
        # get file size
        fsize = os.path.getsize(fpath) / (1024.**2)
        data['size'] = fsize
        size_total += fsize
        all_data.append(data)
        group_ave.append(dgq._global_averages['coarseness_ave'])

    ave = sum(group_ave) / float(len(group_ave))
    print('factor average coarseness {}: {}'.format(factor, ave))
    data = {}
    data['average coarseness'] = ave
    data['group'] = 'total'
    data['dc factor'] = float(factor)
    data['size'] = size_total
    all_data.append(data)

    return all_data


if __name__ == "__main__":

    fdec = sys.argv[1]  # path to wwig decimation folder
    fdef = sys.argv[2]  # path to default geoms

    complete_data = []
    # decimated data
    for factor in os.listdir(fdec):
        fdir = fdec + '/' + factor
        all_data = query_coarseness(fdir, factor)
        complete_data.extend(all_data)
    # default data (r8)
    default_data = query_coarseness(fdef, 1.0)

    complete_data.extend(default_data)

    all_data_df = pd.DataFrame(complete_data)
    all_data_df.to_csv('csv/wwig_coarseness_measurements.csv',
                       index_label='i')
