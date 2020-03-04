import vol as v
import os
import sys


def assign_info():
    info = {}
    for i in range(0,9):
        info[i] = {}

    info[0] = {'wmin': 11.06, 'wmax':1.0e30, 'data':'ww_p_000', 'ratio': 1000, 'el': 0.0, 'eu': 0.045}
    info[1] = {'wmin': 10.77, 'wmax':2.1e36, 'data':'ww_p_001', 'ratio': 50000, 'el': 0.045, 'eu': 0.1 }
    info[2] = {'wmin': 10.29, 'wmax':3.1e21, 'data':'ww_p_002', 'ratio': 1000 , 'el': 0.1, 'eu': 0.2}
    info[3] = {'wmin': 10.11, 'wmax':3.4e15, 'data':'ww_p_003', 'ratio': 1000 , 'el': 0.2, 'eu': 0.3}
    info[4] = {'wmin': 10.15, 'wmax':1.9e13, 'data':'ww_p_004', 'ratio': 100  , 'el': 0.3, 'eu': 0.4}
    info[5] = {'wmin': 10.23, 'wmax':5.0e11, 'data':'ww_p_005', 'ratio': 100  , 'el': 0.4, 'eu': 0.6}
    info[6] = {'wmin': 10.30, 'wmax':5.2e10, 'data':'ww_p_006', 'ratio': 100  , 'el': 0.6, 'eu': 0.8}
    info[7] = {'wmin': 10.37, 'wmax':1.0e10, 'data':'ww_p_007', 'ratio': 100  , 'el': 0.8, 'eu': 1.0}
    info[8] = {'wmin': 10.45, 'wmax':2.32e9, 'data':'ww_p_008', 'ratio': 100  , 'el': 1.0, 'eu': 1.33}

    return info


def main():

    # VTK file of expanded WWINP mesh
    f = '/home/kkiesling/Pokeball/Documents/CNERG/ww-files/particle-tracking-ww/output/cadis/wwinp_expanded.vtk'

    # ratio between levels
    # ratio = 100

    # multiply all values by:
    multiplier = 1.109792819e-09

    # dictionary of min/max vals for each energy group
    info = assign_info()

    # location to save
    database = '/home/kkiesling/Pokeball/Documents/CNERG/ww-files/particle-tracking-ww/wwig/'

    for i in range(0, len(info)):

        print("*************************************   Group {}".format(i))

        wmin = info[i]['wmin']*5.0
        db = database + '{}'.format(info[i]['data'])

        ratio = info[i]['ratio']

        g = v.IsoVolume()

        if i == 0:
            g.assign_levels([1.918e8, 1.385e19, 1.0e30])
        else:
            g.generate_levels(ratio, wmin, info[i]['wmax'], ratio=True)

        g.generate_volumes(f, info[i]['data'], dbname=db)
        #print(g.levels)
        g.create_geometry(info[i]['el'], info[i]['eu'], tag_groups=True, tag_for_viz=False, norm=multiplier, merge_tol=0.0049)
        g.write_geometry(sname='{}-noviz.h5m'.format(info[i]['data']))
        g.write_geometry(sname='{}-noviz.vtk'.format(info[i]['data']))


if __name__ == '__main__':
    main()
