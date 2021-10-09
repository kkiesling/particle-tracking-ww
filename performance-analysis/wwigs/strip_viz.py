import os
import sys
import numpy as np
from pymoab import core, types, rng

# get filename & load it
filename = sys.argv[1]
mb = core.Core()
mb.load_file(filename)
rs = mb.get_root_set()

# triangles and tag name
all_tris = mb.get_entities_by_type(rs, types.MBTRI)
all_tags = mb.tag_get_tags_on_entity(all_tris[0])
non_names = ['GEOM_DIMENSION', 'GLOBAL_ID',
               'CATEGORY', 'GEOM_SENSE_2', 'SURF_TYPE']
data_name = None
for tag in all_tags:
    tag_name = tag.get_name()
    if tag_name not in non_names:
        data_name = tag_name
        break

if data_name is not None:
    data_tag = mb.tag_get_handle(data_name, size=1,
                                 tag_type=types.MB_TYPE_DOUBLE,
                                 storage_type=types.MB_TAG_SPARSE,
                                 create_if_missing=False)
    # delete the data from triangles only
    # some triangles (errors) may not have the viz tag, so need
    # to do try/except to prevent errors.
    for tri in all_tris:
        try:
            mb.tag_delete_data(data_tag, tri)
        except:
            pass

# write new file
sname = filename.split('.')[0] + '_noviz.h5m'
mb.write_file(sname)
