from pyne.mesh import Mesh, NativeMeshTag


# mesh divisions
cx = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]
cy = [-2.5, 2.5]
cz = [-2.5, 2.5]

# create mesh
m = Mesh(structured=True, structured_coords=[cx, cy, cz])

# tag with values
m.tag('ww_n', tagtype=NativeMeshTag, size=1, dtype=float)
vals = [0.5, 0.1, 0.02, 0.004, 0.0008]
m.ww_n[:] = vals

m.write_hdf5('ww-mesh.h5m', write_mats=False)
