import numpy as np
import matplotlib.pyplot as plt
from numpy.core.defchararray import array


def calc_sigmas(means, errors, num):
    sigma_upper = means + (means * errors) * num
    sigma_lower = means - (means * errors) * num

    return sigma_upper, sigma_lower


def calc_ratios(m1, e1, m2, e2):
    # m1 = experiment
    # m2 = accepted

    ratios = m1 / m2
    s1 = m1 * e1
    s2 = m2 * e2
    sigma_ratio = np.sqrt((s1 / m2)**2 + (m1 * s2 / (m2 * m2))**2)

    return ratios, sigma_ratio


# colors
colors = {'wwig': '#C11D59', 'analog': '#7CC145',
          'cwwm': '#247F03', 'reference': '#24E2A5'}
markers = {'wwig': 'd', 'cwwm': 'o',
           'analog': 'x', 'reference': 'X'}
cs = 5  # capsize
dpi = 300

# data
energy = np.array([1.5e-2, 1.5e-1, 4e-1, 9e-1, 1.5])
anlg_res = np.array([4.19235E-06, 2.27496E-05, 3.90809E-05, 6.81679E-05, 8.01488E-05])
anlg_err = np.array([0.1128, 0.0489, 0.0460, 0.0126, 0.0090])
cwwm_res = np.array([7.38633E-06, 2.34374E-05, 3.67348E-05, 6.90740E-05, 7.95049E-05])
cwwm_err = np.array([0.3354, 0.0264, 0.0188, 0.0213,0.0051])
wwig_res = np.array([4.84762E-06, 2.48953E-05, 3.78083E-05, 6.97355E-05, 7.98754E-05])
wwig_err = np.array([0.0471, 0.0180, 0.0104, 0.0065, 0.0050])
#refr_res = np.array([4.37739E-06, 2.40461E-05, 3.88683E-05, 6.94041E-05, 7.95136E-05])
#refr_err = np.array([0.0438, 0.0248, 0.0231, 0.0078, 0.0023])

wwig_cwwm_ratio, wwig_cwwm_sigma = calc_ratios(
    wwig_res, wwig_err, cwwm_res, cwwm_err)
wwig_anlg_ratio, wwig_anlg_sigma = calc_ratios(
    wwig_res, wwig_err, anlg_res, anlg_err)

# plot wwig/cwwm
plt.errorbar(energy, wwig_cwwm_ratio, yerr=wwig_cwwm_sigma, label='$WWIG/CWWM$',
             ls='', marker=markers['wwig'], lw=.9,
             color=colors['wwig'], capsize=cs)
plt.errorbar(energy, wwig_anlg_ratio, yerr=wwig_anlg_sigma, label='$WWIG/Analog$',
             ls='', marker=markers['analog'], lw=.9,
             color=colors['analog'], capsize=cs)

plt.xlabel('Energy Group Upper Bound')
plt.ylabel('Neutron Flux Ratio')
plt.title('Point Detector Tally Results')
#plt.legend(bbox_to_anchor=(0.5, -.21),
#           loc='lower center', ncol=6, fontsize='x-small')
plt.legend(loc='best', fontsize='x-small')
plt.tight_layout()
plt.savefig('verif_tally_results.png', dpi=dpi)


wwig_total = {'res': 2.17162E-04, 'err': 0.0038}
cwwm_total = {'res': 2.16137E-04, 'err': 0.0140}
anlg_total = {'res': 2.14340E-04, 'err': 0.0112}

wwig_cwwm_total_ratio, wwig_cwwm_total_sigma = calc_ratios(
    wwig_total['res'], wwig_total['err'], cwwm_total['res'], cwwm_total['err'])
wwig_anlg_total_ratio, wwig_anlg_total_sigma = calc_ratios(
    wwig_total['res'], wwig_total['err'], anlg_total['res'], anlg_total['err'])

print(wwig_cwwm_total_ratio, wwig_cwwm_total_sigma)
print(wwig_anlg_total_ratio, wwig_anlg_total_sigma)

plt.show()
