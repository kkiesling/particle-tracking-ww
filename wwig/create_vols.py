import vol as v
import os
import sys


def assign_info():
    info = {}
    for i in range(0,9):
        info[i] = {}

    info[0] = {'wmin': 11.06, 'wmax':1.7e30, 'data':'ww_p_000'}
    info[1] = {'wmin': 10.77, 'wmax':2.1e36, 'data':'ww_p_001'}
    info[2] = {'wmin': 10.29, 'wmax':3.1e21, 'data':'ww_p_002'}
    info[3] = {'wmin': 10.11, 'wmax':3.4e15, 'data':'ww_p_003'}
    info[4] = {'wmin': 10.15, 'wmax':1.9e13, 'data':'ww_p_004'}
    info[5] = {'wmin': 10.23, 'wmax':5.0e11, 'data':'ww_p_005'}
    info[6] = {'wmin': 10.30, 'wmax':5.2e10, 'data':'ww_p_006'}
    info[7] = {'wmin': 10.37, 'wmax':1.0e10, 'data':'ww_p_007'}
    info[8] = {'wmin': 10.45, 'wmax':2.32e9, 'data':'ww_p_008'}

    return info


def main():

    # VTK file of expanded WWINP mesh
    f = '/home/kkiesling/Pokeball/Documents/CNERG/ww-files/particle-tracking-ww/output/cadis/wwinp_expanded.vtk'

    # ratio between levels
    ratio = 100

    # multiply all values by:
    multiplier = 1.109792819e-09

    # dictionary of min/max vals for each energy group
    info = assign_info()

    # location to save
    database = '/home/kkiesling/Pokeball/Documents/CNERG/ww-files/particle-tracking-ww/wwig/'

    for i in range(len(info)):

        print("*************************************   Group {}".format(i))

        wmin = info[i]['wmin']*5.0
        db = database + '{}'.format(info[i]['data'])

        g = v.IsoVolume()
        g.generate_levels(ratio, wmin, info[i]['wmax'], ratio=True)
        g.generate_volumes(f, info[i]['data'], dbname=db)
        print(g.levels)
        #g.create_geometry(tag_groups=True, tag_for_viz=True, norm=multiplier, tol=0.2)
        #g.write_geometry(sname='{}.h5m'.format(info[i]['data']))
        #g.write_geometry(sname='{}.vtk'.format(info[i]['data']))


if __name__ == '__main__':
    main()
