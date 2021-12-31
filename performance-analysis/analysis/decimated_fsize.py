import sys
import os
import pandas as pd
from pymoab import core, types


def count_verts(fpath):

    mb = core.Core()
    mb.load_file(fpath)
    rs = mb.get_root_set()
    all_verts = mb.get_entities_by_type(rs, types.MBVERTEX)
    all_edges = mb.get_entities_by_type(rs, types.MBTRI)

    return len(all_verts), len(all_edges)


def query_size(fdir, factor):
    all_data = []
    size_total = 0.
    vertex_count = 0
    edge_count = 0
    for group in range(27):
        data = {}
        ID = '{:03d}'.format(group)
        if float(factor) > 0.0:
            fpath = fdir + '/wwn_{}_noviz.h5m'.format(ID)
        else:
            fpath = fdir + '/wwn_{}.h5m'.format(ID)
        data['group'] = int(group)
        data['dc factor'] = float(factor)
        # get file size
        fsize = os.path.getsize(fpath) / (1024.**2)
        data['size'] = fsize
        size_total += fsize
        num_verts, num_edges = count_verts(fpath)
        data['verts'] = num_verts
        data['edges'] = num_edges
        vertex_count += num_verts
        edge_count += num_edges
        all_data.append(data)
    
    data = {}
    data['group'] = 'total'
    data['dc factor'] = float(factor)
    data['size'] = size_total
    data['verts'] = vertex_count
    data['edges'] = edge_count
    all_data.append(data)

    return all_data


if __name__ == "__main__":

    fdec = sys.argv[1]  # path to wwig decimation folder
    fdef = sys.argv[2]  # path to default geoms

    complete_data = []
    # decimated data
    for factor in os.listdir(fdec):
        if factor == 'all_viz':
            continue
        fdir = fdec + '/' + factor
        all_data = query_size(fdir, factor)
        complete_data.extend(all_data)
    # default data (r8)
    default_data = query_size(fdef, 0.0)

    complete_data.extend(default_data)

    all_data_df = pd.DataFrame(complete_data)
    all_data_df.to_csv('csv/wwig_decimation_size.csv',
                       index_label='i')
