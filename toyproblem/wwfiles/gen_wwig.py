import vol as v

g = v.IsoVolume()
g.generate_levels(4, 8.e-7, 1.7e-6, log=False)
g.generate_volumes('./mesh_ww_tags.vtk', 'ww_n')
g.create_geometry(tag_groups=True, tag_for_viz=True, norm=1.890744809e+05)
g.write_geometry(sname='wwig.h5m')
g.write_geometry(sname='wwig.vtk')
