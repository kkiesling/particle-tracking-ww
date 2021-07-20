import numpy as np
import matplotlib.pyplot as plt
import math as m




def calc_sigmas(means, errors, num):
    sigma_upper = means + (means * errors)*num
    sigma_lower = means - (means * errors)*num

    return sigma_upper, sigma_lower


def calc_ratios(m1, e1, m2, e2):
    # m1 = experiment
    # m2 = accepted

    ratios = m1/m2
    s1 = m1*e1
    s2 = m2*e2
    sigma_ratio = np.sqrt((s1/m2)**2 + (m1*s2/(m2*m2))**2)

    return ratios, sigma_ratio



## Data

# upper bound ratios
c_u = [20, 50, 100]

wwig20 = np.array([6.92970E-08, 6.92190E-08, 6.90550E-08])
wwig20_err = np.array([0.0197, 0.024, 0.0286])

wwig50 = np.array([6.74430E-08, 7.00660E-08, 7.01590E-08])
wwig50_err = np.array([0.0244, 0.0352, 0.0362])

wwig100 = np.array([6.77020E-08, 6.96540E-08, 6.94170E-08])
wwig100_err = np.array([0.0264, 0.0297, 0.0301])

wwinp = np.array([6.88180E-08, 7.07220E-08, 6.87680E-08])
wwinp_err = np.array([0.0128, 0.0198, 0.022])

analog = np.array([6.47480E-08, 6.47480E-08, 6.47480E-08])
analog_err = np.array([0.0475, 0.0475, 0.0475])


wwinp1_upper, wwinp1_lower = calc_sigmas(wwinp, wwinp_err, 1)
wwinp2_upper, wwinp2_lower = calc_sigmas(wwinp, wwinp_err, 2)


# Plots

wwinp_color = '#6FDE6E'
wwig_color = ['#0A284B', '#235FA4', '#A691AE']
analog_color = '#E8F086'

extra_color = '#FF4242'

# raw results compared to 1, 2, sigma of wwinp value
plt.figure()
plt.plot(c_u, wwinp, label='WWINP', ls='', marker='o', lw=.75, color=wwinp_color)
plt.plot(c_u, wwinp1_upper, label='WWINP +/- 1 sigma', ls='--', lw=.75, color=wwinp_color)
plt.plot(c_u, wwinp1_lower, label='', ls='--', lw=.75, color=wwinp_color)
plt.plot(c_u, wwinp2_upper, label='WWINP +/- 2 sigma', ls=':', lw=.75, color=wwinp_color)
plt.plot(c_u, wwinp2_lower, label='', ls=':', lw=.75, color=wwinp_color)
plt.errorbar(c_u, analog, yerr=(analog_err*analog), color=analog_color, label='Analog', ls='', marker='D', lw=.9, capsize=4)
plt.errorbar(c_u, wwig20, yerr=(wwig20_err*wwig20), color=wwig_color[0], label='WWIG r=20', ls='', marker='d', lw=.9, capsize=4)
plt.errorbar(c_u, wwig50, yerr=(wwig50_err*wwig50), color=wwig_color[1], label='WWIG r=50', ls='', marker='d', lw=.9, capsize=4)
plt.errorbar(c_u, wwig100, yerr=(wwig100_err*wwig100), color=wwig_color[2], label='WWIG r=100', ls='', marker='d', lw=.9, capsize=4)
plt.xlabel('WW Upper Bound Constant c_u')
plt.ylabel('Tally')
plt.title('Point Detector Tally Results')
plt.legend(loc='best', ncol=2, fontsize='xx-small')
plt.savefig('tally15_results.png')


# plot ratios compared to wwinp
m20, e20 = calc_ratios(wwig20, wwig20_err, wwinp, wwinp_err)
m50, e50 = calc_ratios(wwig50, wwig50_err, wwinp, wwinp_err)
m100, e100 = calc_ratios(wwig100, wwig100_err, wwinp, wwinp_err)
mana, eana = calc_ratios(analog, analog_err, wwinp, wwinp_err)

plt.figure()
plt.plot(c_u, [1, 1, 1], ls='-', color=wwinp_color, lw=.9)
plt.errorbar(c_u, m20, yerr=e20, label='WWIG r=20', ls='', marker='d', lw=.9, capsize=4, color=wwig_color[0])
plt.errorbar(c_u, m50, yerr=e50, label='WWIG r=50', ls='', marker='d', lw=.9, capsize=4, color=wwig_color[1])
plt.errorbar(c_u, m100, yerr=e100, label='WWIG r=100', ls='', marker='d', lw=.9, capsize=4, color=wwig_color[2])
plt.errorbar(c_u, mana, yerr=eana, label='WWIG analog', ls='', marker='D', lw=.9, capsize=4, color=analog_color)
plt.xlabel('WW Upper Bound Constant c_u')
plt.ylabel('Ratio (E/WWINP)')
plt.title('Point Detector Tally Results, compared to WWINP results')
plt.legend(loc='best', ncol=4, fontsize='xx-small', title='Comparison Results E')
plt.savefig('tally15_ratios.png')

# plot relative errors
plt.figure()
plt.plot(c_u, analog_err, label='analog', ls='-', marker='D', lw=.9, color=analog_color)
plt.plot(c_u, wwinp_err, label='WWINP', ls='-', marker='o', lw=.9, color=wwinp_color)
plt.plot(c_u, wwig20_err, label='WWIG r=20', ls='-', marker='d', lw=.9, color=wwig_color[0])
plt.plot(c_u, wwig50_err, label='WWIG r=50', ls='-', marker='d', lw=.9, color=wwig_color[1])
plt.plot(c_u, wwig100_err, label='WWIG r=100', ls='-', marker='d', lw=.9, color=wwig_color[2])
plt.xlabel('WW Upper Bound Constant c_u')
plt.ylabel('Relative Error')
plt.title('Point Detector Tally Relative Error')
plt.legend(loc='best', ncol=3, fontsize='xx-small')
plt.savefig('tally15_error.png')

plt.show()
