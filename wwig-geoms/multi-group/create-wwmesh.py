from pyne.mesh import Mesh, NativeMeshTag
import numpy as np

# mesh divisions
cx = np.linspace(0., 20., 21, endpoint=True)
cy = [-5., 5.]
cz = [-5., 5.]
num_mesh = (len(cx) - 1) * (len(cy) - 1) * (len(cz) - 1)

# ww values for each mesh voxel region
ww_vals = [0.1, 0.02, 0.004, 0.0008, 0.00016]

# x coordinates where each surface will be located, key is energy group id
w_loc = {0: [0, 1, 6, 11, 16, 20],  # E0
         1: [0, 2, 7, 12, 17, 20],  # E1
         2: [0, 3, 8, 13, 18, 20],  # E2
         3: [0, 4, 9, 14, 19, 20],  # E3
         4: [0, 5, 10, 15, 20]}     # E4
num_egrp = len(w_loc)

# create mesh for data population
m = Mesh(structured=True, structured_coords=[cx, cy, cz])

# create a data tag for ww_vals (vector)
m.tag('ww_n', tagtype=NativeMeshTag, size=len(w_loc), dtype=float)

# create array of values for each mesh voxel, 20 voxels, 5 vals per voxel
ww_data = np.zeros((num_mesh, num_egrp))
for grp, loc in w_loc.items():
    for i in range(len(loc)-1):
        start = loc[i]
        end = loc[i+1]
        for index in range(start, end):
            ww_data[index][grp] = ww_vals[i]

# populate data
m.ww_n[:] = ww_data

# save mesh
m.write_hdf5('ww-mesh.h5m', write_mats=False)

# To create wwig geoms:
# generate_isogeom full ww-mesh-expanded.vtk ww_n_004 -lv 0.06 0.012 0.0024 0.00048 -db e4 -t E_LOW_BOUND 9e-1 -t E_UP_BOUND 1.5 -g wwn_4.h5m -v
# e_bounds = [0, 1.5e-2, 1.5e-1, 4.e-1, 9.e-1, 1.5]
