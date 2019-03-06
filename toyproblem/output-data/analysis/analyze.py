from pyne import mesh
import sys
import numpy as np

from matplotlib import pyplot as plt

# Read in mesh files
ref_file = sys.argv[1]
comp_file = sys.argv[2]
ref_mesh = mesh.Mesh(mesh=ref_file, structured=True)
ref_copy = mesh.Mesh(mesh=ref_file, structured=True)
comp_mesh = mesh.Mesh(mesh=comp_file, structured=True)

ref_name = ref_file.split("/")[1].split("-")[0]
comp_name = comp_file.split("/")[1].split("-")[0]

# get new delta mesh
delta_mesh = ref_mesh.__isub__(comp_mesh).__idiv__(ref_copy)

# get all elements in delta_mesh and take absolute value
new_vals = np.array([])
for i in delta_mesh.neutron_result[:]:
    if np.isnan(i) or np.isinf(i):
        i = -1.0
    else:
        i = abs(i)
    new_vals = np.append(new_vals, i)

# get z values
new_error = delta_mesh.neutron_result_rel_error[:]
z_values = new_vals/new_error
new_z = np.array([])
for i in z_values:
    if np.isinf(i):
        i = -1.0
    new_z = np.append(new_z, i)

# make new z mesh
c = np.linspace(-15, 15, num=61)
z_coords = [c, c, c]
z_mesh = mesh.Mesh(structured_coords=z_coords, structured=True)
z_mesh.tag('zval', size=1, tagtype='nat_mesh', dtype=np.float)
z_mesh.zval[:] = new_z[:]

save_name = ref_name + '-' + comp_name
z_mesh.write_hdf5(save_name + '.h5m', write_mats=False)

# remove -1 values from data (nonsensical)
z_vals = np.array([])
for i in new_z:
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
bins = np.linspace(0, 5, num=11)
pdf, axpdf = plt.subplots(figsize=(9, 6))
_, bins, patches = plt.hist(np.clip(z_vals, bins[0], bins[-1]),
    bins=bins, normed=True, color='#3782CC')
xlabels = bins[1:].astype(str)
xlabels[-1] += '+'
axpdf.set_xticklabels(xlabels)
plt.xlim([0, 5])
plt.ylim([0,.55])
plt.xticks(bins[1:])
plt.xlabel('Z value')
plt.title(title + '\n' + 'Z-Score PDF')
pdf.tight_layout()
plt.savefig(save_name + '-pdf.png')
#plt.show()

# CDF
bins = np.linspace(0, 5, num=11)
cdf, axcdf = plt.subplots(figsize=(9, 6))
_, bins, patches = plt.hist(np.clip(z_vals, bins[0], bins[-1]),
    bins=bins, cumulative=True, normed=True, color='#3782CC')
xlabels = bins[1:].astype(str)
xlabels[-1] += '+'
axcdf.set_xticklabels(xlabels)
plt.xlim([0, 5])
plt.ylim([0,1.0])
plt.xticks(bins[1:])
plt.xlabel('Z value')
plt.title(title + '\n' + 'Z-Score CDF')
cdf.tight_layout()
plt.savefig(save_name + '-cdf.png')
#plt.show()

