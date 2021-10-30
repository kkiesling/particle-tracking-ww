import sys
import os
import meshio
from IsogeomGenerator import driver, isg, ivdb

# to run:
# generate_isogeom full [wwinp-mesh].vtk ww_n_[ID] -gl ratio -lx [MIN] [MAX] \
# -N [RATIO] -db [GROUP NUM] - t E_LOW_BOUND [E_LOW] - t E_UP_BOUND [E_HI] -g wwn_[ID].h5m - v

# to run this script w/ cadis:
# python ../generate_wwigs.py 5 4.026155758e-09 ../mesh_ww_tags.vtk
# python ../generate_wwigs.py RATIO NORM VTK


def get_data(fvtk, id_rng):

    wwig_info = {}
    mf = meshio.read(fvtk)

    for i in id_rng:
        info = {}
        ID = '{:03d}'.format(i)
        dataname = 'ww_n'
        mindata = min(mf.cell_data['hexahedron'][dataname])
        maxdata = max(mf.cell_data['hexahedron'][dataname])
        e_max = 20.
        e_min = 0.0

        info['e_min'] = float(e_min)
        info['e_max'] = float(e_max)
        info['name'] = dataname
        info['w_min'] = mindata
        info['w_max'] = maxdata

        wwig_info[ID] = info

    return wwig_info


def generate_wwigs(wwig_info, fvtk, ratio, norm, id_rng):

    for ID, info in wwig_info.items():

        if int(ID) in id_rng:
            print("GENERATING ID " + ID)
            # generate levels
            minN = info['w_min'] * float(ratio)
            maxN = info['w_max'] / float(ratio)
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

    id_rng = range(1)

    wwig_info = get_data(fvtk, id_rng)

    generate_wwigs(wwig_info, fvtk, ratio, norm, id_rng)
