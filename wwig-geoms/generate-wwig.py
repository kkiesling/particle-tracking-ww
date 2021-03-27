import sys
import os
import meshio
from pymoab import core, tag
from IsogeomGenerator import driver, isg, ivdb

# to run:
# generate_isogeom full [wwinp-mesh].vtk ww_n_[ID] -gl ratio -lx [MIN] [MAX] \
# -N [RATIO] -db [GROUP NUM] - t E_LOW_BOUND [E_LOW] - t E_UP_BOUND [E_HI] -g wwn_[ID].h5m - v


def get_upper_bounds(fh5m):

    mb = core.Core()
    mb.load_file(fh5m)
    rs = mb.get_root_set()
    all_tags = mb.tag_get_tags_on_entity(rs)

    for tag in all_tags:
        name = tag.get_name()
        if name == 'n_e_upper_bounds':
            e_bounds = mb.tag_get_data(tag, rs)
            return sorted(e_bounds[0], reverse=True)


def get_data(fvtk, e_bounds):

    wwig_info = {}
    mf = meshio.read(fvtk)

    for i in range(len(e_bounds)):
        info = {}
        ID = '{:03d}'.format(i)
        dataname = 'ww_n_' + ID
        mindata = min(mf.cell_data['hexahedron'][dataname])
        maxdata = max(mf.cell_data['hexahedron'][dataname])
        e_max = e_bounds[i]
        if i == len(e_bounds) - 1:
            e_min = 0.0
        else:
            e_min = e_bounds[i+1]

        info['e_min'] = e_min
        info['e_max'] = e_max
        info['name'] = dataname
        info['w_min'] = mindata
        info['w_max'] = maxdata

        wwig_info[ID] = info

    return wwig_info


def generate_wwigs(wwig_info, fvtk, ratio, norm):

    for ID, info in wwig_info.items():

        # generate levels
        minN = info['w_min'] * ratio
        maxN = info['w_max']
        levels = driver.generate_levels(ratio, minN, maxN, mode='ratio')

        # generate volumes from visit
        data = info['name']
        db = os.getcwd() + '/' + ID
        iv = ivdb.IvDb(levels=levels, data=data, db=db)
        driver.generate_volumes(iv, fvtk)

        # create isogeom with moab
        ig = isg.IsGm(ivdb=iv)
        sname = 'wwn_' + ID + '.h5m'
        tags = {'E_LOW_BOUND': info['e_min'],
                'E_UP_BOUND': info['e_max']}
        driver.create_geometry(ig, tag_for_viz=True, tags=tags, norm=norm, sname=sname)


if __name__ == '__main__':

    # get file (expanded_tags.vtk, mesh_with_tags.h5m)
    ratio = float(sys.argv[1])
    norm = float(sys.argv[2])
    fvtk = sys.argv[3]
    fh5m = sys.argv[4]

    e_bounds = get_upper_bounds(fh5m)

    wwig_info = get_data(fvtk, e_bounds)

    generate_wwigs(wwig_info, fvtk, ratio, norm)
