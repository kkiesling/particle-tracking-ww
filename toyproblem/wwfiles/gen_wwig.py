import vol as v

g = v.IsoVolume()
g.generate_levels(7, 1.e-5, 0.1, log=True)
g.generate_volumes('./ww_mesh.vtk', 'ww_n')
g.create_geometry(tag_groups=True, tag_for_viz=True, norm=1.990133553e3)
g.write_geometry(sname='wwig.h5m')
g.write_geometry(sname='wwig.vtk')
