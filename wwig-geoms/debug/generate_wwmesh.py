from pyne.mesh import Mesh, NativeMeshTag
import numpy as np

start = 0.
x1 = 10.
x2 = x1 + 15.
end = x2 + 10.

xcoords = np.linspace(start, end, num=(end - start)/2, endpoint=True)
ycoords = np.linspace(-5., 5., num=5, endpoint=True)
zcoords = np.linspace(-5., 5., num=5, endpoint=True)
coords = [xcoords, ycoords, zcoords]

m = Mesh(structured_coords=coords, structured=True, mats=None)
m.ww = NativeMeshTag(size=1, dtype=float)

idx = 0
values = []
for x in xcoords[1:]:
    for y in ycoords[1:]:
        for z in zcoords[1:]:
            if x <= x1:
                val = 1.
            elif x >= x2:
                val = 1000.
            else:
                val = 1000. * (x - x1) / (x2 - x1)

            values.append(val)
            idx += 1

m.ww[:] = values

m.write_hdf5('debug-wwinp.h5m')
