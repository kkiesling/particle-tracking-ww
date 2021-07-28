import sys
import os
import meshio
from pymoab import core, types
from IsogeomGenerator import driver, isg, ivdb
import numpy as np

# wwmesh file
fh5m = './debug-wwinp.h5m'
fvtk = './debug-wwinp.vtk'

# # analyze gradients?
# mb = core.Core()
# mb.load_file(fh5m)
# rs = mb.get_root_set()
# hexes = mb.get_entities_by_dimension(rs, 3)
# verts = mb.get_entities_by_dimension(rs, 0)
# wwtag = mb.tag_get_handle('ww', 1, types.MB_TYPE_DOUBLE,
#                           types.MB_TAG_DENSE, create_if_missing=False)
#
#
# for vert in verts:
#     # get adjacent hexes
#     adj_hexes = mb.get_adjacencies(vert, 3)
#     # get tag data on hexes
#     hex_vals = mb.tag_get_data(wwtag, adj_hexes)
#     # get average of hex vals and assign as vert val
#     vert_val = np.average(hex_vals)
#     mb.tag_set_data(wwtag, vert, vert_val)
#
# mb.write_file('wwmesh_verts.vtk')


# info about ww values
dname = 'ww'
ratio = 5
minval = 1
maxval = 1000

# generate levels
minN = minval * ratio
maxN = maxval
levels = driver.generate_levels(ratio, minN, maxN, mode='ratio')

# generate volumes from visit
db = os.getcwd() + '/dbg'.format(ratio)
iv = ivdb.IvDb(levels=levels, data=dname, db=db)
driver.generate_volumes(iv, fvtk)

# create isogeom with moab
ig = isg.IsGm(ivdb=iv)
sname = 'debug-wwig.vtk'
driver.create_geometry(ig, tag_for_viz=True, sname=sname)
print(ig.levels)
