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

ratios = np.array([5, 20, 50, 100])
wwig_res = np.array([6.82e-8, 6.8638E-08, 6.8536E-08, 6.9097E-08])  # placeholders
wwig_err = np.array([.01, 0.0140, 0.0178, 0.0204])  # placeholders
wwinp_res = np.array([6.8328E-08, 6.8328E-08, 6.8328E-08, 6.8328E-08])
wwinp_err = np.array([0.0076, 0.0076, 0.0076, 0.0076])
analog_res = np.array([6.47480E-08, 6.47480E-08, 6.47480E-08, 6.47480E-08])
analog_err = np.array([0.0475, 0.0475, 0.0475, 0.0475])

wwinp1_upper, wwinp1_lower = calc_sigmas(wwinp_res, wwinp_err, 1)
wwinp2_upper, wwinp2_lower = calc_sigmas(wwinp_res, wwinp_err, 2)


# Plots

wwinp_color = '#FF4242'
wwig_color = '#235FA4'
analog_color = '#6FDE6E'

# all colors: '#FF4242', '#E8F086', '#6FDE6E', '#0A284B', '#235FA4', '#A691AE'

cs = 5  # cap size
dpi = 300

# plot results
plt.figure()
plt.errorbar(ratios, wwig_res, yerr=(wwig_err*wwig_res),
    color=wwig_color, label='WWIG', ls='', marker='d', lw=.9, capsize=cs)
plt.errorbar([105], analog_res[0], yerr=(analog_err*analog_res)[0],
    color=analog_color, label='Analog', ls='', marker='d', lw=.9, capsize=cs)
plt.plot(ratios, wwinp_res, label='WWINP', ls='-', marker='', lw=.9, color=wwinp_color)
plt.plot(ratios, wwinp1_upper, label='WWINP +/- 1 sigma', ls='--', lw=.75, color=wwinp_color)
plt.plot(ratios, wwinp1_lower, label='', ls='--', lw=.75, color=wwinp_color)
plt.plot(ratios, wwinp2_upper, label='WWINP +/- 2 sigma', ls=':', lw=.75, color=wwinp_color)
plt.plot(ratios, wwinp2_lower, label='', ls=':', lw=.75, color=wwinp_color)
plt.xlabel('WWIG surface spacing ratio')
plt.ylabel('Tally')
plt.title('Point Detector Tally Results')
plt.legend(loc='best', ncol=2, fontsize='x-small')
plt.savefig('tally15_results.png', dpi=dpi)

# plot wwinp ratio
r1 = np.array([1, 1, 1, 1])

# ratios compared to wwinp results
wratio, werr = calc_ratios(wwig_res, wwig_err, wwinp_res, wwinp_err)
aratio, aerr = calc_ratios(analog_res, analog_err, wwinp_res, wwinp_err)

wr1_upper, wr1_lower = calc_sigmas(r1, werr, 1)
wr2_upper, wr2_lower = calc_sigmas(r1, werr, 2)
ar1_upper, ar1_lower = calc_sigmas(r1, aerr, 1)
ar2_upper, ar2_lower = calc_sigmas(r1, aerr, 2)

plt.figure()
plt.plot(ratios, r1, label='E/WWINP=1', ls='-', marker='', lw=.9, color=wwinp_color)

plt.plot(ratios, wr1_upper, label='WWIG/WWINP +/- 1 sigma', ls='--', lw=.75, color=wwig_color)
plt.plot(ratios, wr1_lower, label='', ls='--', lw=.75, color=wwig_color)
plt.plot(ratios, wr2_upper, label='WWIG/WWINP +/- 2 sigma', ls=':', lw=.75, color=wwig_color)
plt.plot(ratios, wr2_lower, label='', ls=':', lw=.75, color=wwig_color)
plt.plot(ratios, wratio, label='WWIG/WWINP', ls='', marker='d', lw=.9, color=wwig_color)

# figure out how I want to display the analog/wwinp ratio on this plot
#plt.plot(ratios, ar1_upper, label='Analog/WWINP +/- 1 sigma', ls='--', lw=.75, color=analog_color)
#plt.plot(ratios, ar1_lower, label='', ls='--', lw=.75, color=analog_color)
#plt.plot(ratios, ar2_upper, label='Analog/WWINP +/- 2 sigma', ls=':', lw=.75, color=analog_color)
#plt.plot(ratios, ar2_lower, label='', ls=':', lw=.75, color=analog_color)
#plt.plot(ratios, aratio, label='Analog/WWINP', ls='', marker='d', lw=.9, color=analog_color)
# make this plot a subplot right next to it?
plt.errorbar([105], [1], yerr=(aratio*aerr)[0], label='analog/WWINP +/- 1 sigma', ls='', marker='', lw=.9, capsize=cs, color=analog_color)
plt.plot([105], aratio[0], label='analog/WWINP', ls='', marker='d', lw=.9, color=analog_color)

plt.xlabel('WWIG surface spacing ratio')
plt.ylabel('Ratio (E/WWINP)')
plt.title('Point Detector Tally Results, compared to WWINP results')
plt.legend(loc='best', ncol=2, fontsize='x-small', title='Comparison Results E')
plt.savefig('tally15_ratios.png', dpi=dpi)


# plot relative errors
plt.figure()
plt.plot(ratios, wwinp_err, label='WWINP', ls='-', marker='', lw=.9, color=wwinp_color)
plt.plot(ratios, wwig_err, label='WWIG', ls='-', marker='d', lw=.9, color=wwig_color)
plt.plot(ratios, analog_err, label='analog', ls='-', marker='', lw=.9, color=analog_color)
plt.xlabel('WWIG surface spacing ratio')
plt.ylabel('Relative Error')
plt.title('Point Detector Tally Relative Error')
plt.legend(loc='best', fontsize='x-small')
plt.savefig('tally15_error.png', dpi=dpi)

plt.show()
