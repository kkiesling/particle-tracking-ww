import sys
import os
import pandas as pd


def query_size(fdir, ratio):
    all_data = []
    size_total = 0.
    for group in range(27):
        data = {}
        ID = '{:03d}'.format(group)
        fpath = fdir + '/geoms/wwn_{}.h5m'.format(ID)
        print(fpath)
        data['group'] = int(group)
        data['ratio'] = int(ratio)
        # get file size
        fsize = os.path.getsize(fpath) / (1024.**2)
        data['size'] = fsize
        size_total += fsize
        print(data)
        all_data.append(data)

    data = {}
    data['group'] = 'total'
    data['ratio'] = int(ratio)
    data['size'] = size_total
    all_data.append(data)

    return all_data


if __name__ == "__main__":

    fdec = sys.argv[1]  # path to wwig ratio folder

    complete_data = []
    # decimated data
    for rdir in os.listdir(fdec):
        fdir = fdec + '/' + rdir
        ratio = rdir[1:]
        all_data = query_size(fdir, ratio)
        complete_data.extend(all_data)

    all_data_df = pd.DataFrame(complete_data)
    all_data_df.to_csv('csv/wwig_ratio_size.csv',
                       index_label='i')
