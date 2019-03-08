from pyne import mesh
import sys
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

# Read in mesh files
ref_file = sys.argv[1]
comp_file = sys.argv[2]
ref_mesh = mesh.StatMesh(mesh=ref_file, structured=True)
ref_copy = mesh.StatMesh(mesh=ref_file, structured=True)
comp_mesh = mesh.StatMesh(mesh=comp_file, structured=True)

ref_name = ref_file.split("/")[1].split("-")[0]
comp_name = comp_file.split("/")[1].split("-")[0]

# eliminate any zero results from the refrence and compare mesh
comp_mesh.neutron_result[comp_mesh.neutron_result[:] == 0.0] = np.nan
ref_mesh.neutron_result[ref_mesh.neutron_result[:] == 0.0] = np.nan
ref_copy.neutron_result[ref_copy.neutron_result[:] == 0.0] = np.nan

# get new delta mesh: delta = (ref - comp)/ref
delta_mesh = ref_mesh.__isub__(comp_mesh).__idiv__(ref_copy)

# get absolute value of all values
delta_mesh.neutron_result[:] = np.absolute(delta_mesh.neutron_result[:])

# eliminate any nan or inf results (set to nonsensical number)
# (need numbers to make the mesh for plotting, but get eliminated for
# PDF and CDF later)
delta_mesh.neutron_result[np.isnan(delta_mesh.neutron_result[:])] = -1.0
delta_mesh.neutron_result[np.isinf(delta_mesh.neutron_result[:])] = -1.0

# get z values
z_values = delta_mesh.neutron_result[:]/delta_mesh.neutron_result_rel_error[:]
z_values[np.isnan(z_values[:])] = -1.0
z_values[np.isinf(z_values[:])] = -1.0

# make new z mesh
c = np.linspace(-15, 15, num=61)
z_coords = [c, c, c]
z_mesh = mesh.Mesh(structured_coords=z_coords, structured=True)
z_mesh.tag('zval', size=1, tagtype='nat_mesh', dtype=np.float)
z_mesh.zval[:] = z_values[:]

save_name = ref_name + '-' + comp_name
z_mesh.write_hdf5(save_name + '-zval.h5m', write_mats=False)
delta_mesh.write_hdf5(save_name + '-delta.h5m', write_mats=False)
