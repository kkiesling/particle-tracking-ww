import sys
import os
from pymoab import core, tag

def get_upper_bounds(fh5m):

    mb = core.Core()
    mb.load_file(fh5m)
    rs = mb.get_root_set()
    all_tags = mb.tag_get_tags_on_entity(rs)

    for tag in all_tags:
        name = tag.get_name()
        if name == 'n_e_upper_bounds':
            e_bounds = mb.tag_get_data(tag, rs)
            return sorted(e_bounds[0], reverse=False)


if __name__ == '__main__':

    # get file (expanded_tags.vtk, mesh_with_tags.h5m)
    fh5m = sys.argv[1]

    e_bounds = get_upper_bounds(fh5m)
    print(e_bounds)
