import vol as v

g = v.IsoVolume()
g.generate_levels(7, 1.e-6, 1.e-3, log=True)
g.generate_volumes('./ww_mesh.vtk', 'ww_n')
g.create_geometry(tag_groups=True, tag_for_viz=True)
g.write_geometry(sname='wwig.h5m')
g.write_geometry(sname='wwig.vtk')
