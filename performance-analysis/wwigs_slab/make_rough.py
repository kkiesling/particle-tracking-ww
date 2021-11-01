import sys
import glob
from pymoab import core, types
import random
import numpy as np


def get_interior_surfs(mb):
    """get only the set of surfaces that are interior"""
    rs = mb.get_root_set()
    # get necessary tag information
    dim_tag = mb.tag_get_handle('GEOM_DIMENSION', size=1,
                                tag_type=types.MB_TYPE_INTEGER,
                                storage_type=types.MB_TAG_SPARSE,
                                create_if_missing=False)
    surf_type_tag = \
        mb.tag_get_handle('SURF_TYPE', size=32,
                          tag_type=types.MB_TYPE_OPAQUE,
                          storage_type=types.MB_TAG_SPARSE,
                          create_if_missing=False)
    all_surfs = mb.get_entities_by_type_and_tag(rs, types.MBENTITYSET,
                                                dim_tag, [2])
    interior_surfs = []
    for surf in all_surfs:
        surf_type = mb.tag_get_data(surf_type_tag, surf)
        if surf_type == 'interior':
            interior_surfs.append(surf)

    return interior_surfs


def perturb_verts(mb, surfs, geom_ext, pertub_max):
    # perturb vertices by some amount (maximum perturb_max) in the x
    # direction

    for surf in surfs:
        # get all vertices
        all_verts = mb.get_entities_by_type(surf, types.MBVERTEX)

        for vert in all_verts:
            coords = mb.get_coords(vert)
            if (coords[0] in geom_ext['x']) or \
               (coords[1] in geom_ext['y']) or \
               (coords[2] in geom_ext['z']):
                # don't perturb edge verts
                continue

            perturbation = random.random() * 2. + -abs(pertub_max)
            new_x = coords[0] + perturbation
            new_coords = np.array([new_x, coords[1], coords[2]])
            mb.set_coords(vert, new_coords)

    return mb


if __name__ == '__main__':
    # for each h5m group file, load file, perturb interior surfs, rewrite file

    fpath = 'r8/geoms/'
    all_wwigs = glob.glob(fpath + '/*.h5m')

    pertub_max = float(sys.argv[1])

    # geometric extents
    geom_ext = {'x': [-25, 25], 'y': [50, 50], 'z': [50, 50]}

    for f in all_wwigs:

        # load into pymoab instance
        mb = core.Core()
        mb.load_file(f)

        # get interior surfs
        interior = get_interior_surfs(mb)

        mb = perturb_verts(mb, interior, geom_ext, pertub_max)

        sname = 'rougher/{}/'.format(pertub_max) + f.split('/')[-1]
        mb.write_file(sname)
