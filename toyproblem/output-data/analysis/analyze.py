from pyne import mesh
import sys
import numpy as np
import pdb
from matplotlib import pyplot as plt

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
z_mesh.write_hdf5(save_name + '.h5m', write_mats=False)

# remove -1 values from data (nonsensical)
z_vals = np.array([])
for i in z_values:
    if i != -1.0:
        z_vals = np.append(z_vals, i)


# plot normalized histogram (PDF and CDF)

# make title:
if ref_name == 'analog':
    first = 'Analog'
elif ref_name == 'wwinp':
    first = 'Cartesian WW Mesh'
elif ref_name == 'wwig':
    first = 'WWIG'

if comp_name == 'analog':
    second = 'Analog'
elif comp_name == 'wwinp':
    second = 'Cartesian WW Mesh'
elif comp_name == 'wwig':
    second = 'WWIG'

title = first + ' vs. ' + second

# PDF
bins = np.linspace(0, 10, num=101)
pdf, axpdf = plt.subplots(figsize=(9, 6))
_, bins, patches = plt.hist(np.clip(z_vals, bins[0], bins[-1]),
    bins=bins, normed=True, color='#3782CC', histtype='bar')
#xlabels = bins[1:-1:10].astype(str)
#xlabels[-1] += '+'
#axpdf.set_xticklabels(xlabels)
plt.xlim([0, 10])
plt.ylim([0, 1.0])
#plt.xticks(bins[1:-1:10])
plt.xlabel('Z value')
plt.title(title + '\n' + 'Z-Score PDF')
pdf.tight_layout()
plt.savefig(save_name + '-pdf.png')
#plt.show()

# CDF
bins = np.linspace(0, 10, num=101)
cdf, axcdf = plt.subplots(figsize=(9, 6))
_, bins, patches = plt.hist(np.clip(z_vals, bins[0], bins[-1]),
    bins=bins, cumulative=True, normed=True, color='#3782CC', histtype='bar')
#xlabels = bins[1:-1:10].astype(str)
#xlabels[-1] += '+'
#axcdf.set_xticklabels(xlabels)
plt.xlim([0, 10])
plt.ylim([0, 1.0])
#plt.xticks(bins[1:-1:10])
plt.xlabel('Z value')
plt.title(title + '\n' + 'Z-Score CDF')
cdf.tight_layout()
plt.savefig(save_name + '-cdf.png')
#plt.show()
