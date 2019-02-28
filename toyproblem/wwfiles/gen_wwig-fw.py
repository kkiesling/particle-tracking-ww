import vol as v

g = v.IsoVolume()
g.generate_levels(6, 0.01, 0.18, log=False)
g.generate_volumes('./wwmesh-point.vtk', 'ww_n')
g.create_geometry(tag_groups=True, tag_for_viz=True, norm=2.078987641)
g.write_geometry(sname='wwig-point.h5m')
g.write_geometry(sname='wwig-point.vtk')
