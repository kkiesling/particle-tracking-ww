import numpy as np
import matplotlib.pyplot as plt
import math as m
import twosample_ttest as tt


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


# Data - 1e6 particles
ratios = np.array([5, 10, 15, 20])
wwinp_res = np.full(len(ratios), 5.5896E-08)
wwinp_err = np.full(len(ratios), 0.0100)
wwig_res = np.array([5.6022E-08, 5.5119E-08, 5.5265E-08, 5.5659E-08])
wwig_err = np.array([0.0093, 0.0107, 0.0121, 0.0126])
analog_res = np.full(len(ratios), 5.5739E-08)
analog_err = np.full(len(ratios), 0.0240)

# reference solutions
ref_res = np.full(len(ratios) + 1, 5.5894E-08)
ref_err = np.full(len(ratios) + 1, 0.0076)

ref1_upper, ref1_lower = calc_sigmas(ref_res, ref_err, 1)
ref2_upper, ref2_lower = calc_sigmas(ref_res, ref_err, 2)

# Plots
# stuff for plots
ext_x = max(ratios) + 1
ref_xs = np.append(ratios, ext_x)

# all colors: '#FF4242', '#235FA4', '#6FDE6E', '#E8F086', '#0A284B', '#A691AE'
wwinp_color = '#A691AE'
wwig_color = '#235FA4'
analog_color = '#FF4242'
ref_color = '#6FDE6E'

cs = 5  # cap size
dpi = 300

# plot results
plt.figure()
plt.errorbar(ratios, wwig_res, yerr=(wwig_err * wwig_res), color=wwig_color,
             label='WWIG', ls='', marker='d', lw=.9, capsize=cs)
plt.errorbar([ext_x], wwinp_res[0], yerr=(wwinp_err * wwinp_res)[0],
             color=wwinp_color, label='CWWM', ls='', marker='x', lw=.9,
             capsize=cs)
plt.errorbar([ext_x], analog_res[0], yerr=(analog_err * analog_res)[0],
             color=analog_color, label='Analog', ls='', marker='o', lw=.9,
             capsize=cs)
plt.plot(ref_xs, ref_res, label='Reference', ls='-', marker='', lw=.9,
         color=ref_color)
plt.plot(ref_xs, ref1_upper, label='Reference $\pm 1\sigma$', ls='--', lw=.75,
         color=ref_color)
plt.plot(ref_xs, ref1_lower, label='', ls='--', lw=.75, color=ref_color)
plt.plot(ref_xs, ref2_upper, label='Reference $\pm 2\sigma$',
         ls=':', lw=.75, color=ref_color)
plt.plot(ref_xs, ref2_lower, label='', ls=':', lw=.75, color=ref_color)
plt.xlabel('WWIG surface spacing ratio $r$')
plt.ylabel('Neutron Flux $[1/cm^2]$')
plt.title('Point Detector Tally Results')
plt.legend(bbox_to_anchor=(0.5, -.21), loc='lower center', ncol=6, fontsize='x-small')
plt.tight_layout()
plt.savefig('tally15_results.png', dpi=dpi)

# plot wwinp ratio
r1 = np.full(len(ratios), 1)

# results compared to reference results (ratios)
wgratio, wgerr = calc_ratios(
    wwig_res, wwig_err, ref_res[:len(ratios)], ref_err[:len(ratios)])
wpratio, wperr = calc_ratios(
    wwinp_res[0], wwinp_err[0], ref_res[0], ref_err[0])
aratio, aerr = calc_ratios(
    analog_res[0], analog_err[0], ref_res[0], ref_err[0])

# wwig/ref sigmas
wgr1_upper, wgr1_lower = calc_sigmas(r1, wgerr, 1)
wgr2_upper, wgr2_lower = calc_sigmas(r1, wgerr, 2)

# wwinp/ref sigmas
wpr1_upper, wpr1_lower = calc_sigmas(r1, wperr, 1)
wpr2_upper, wpr2_lower = calc_sigmas(r1, wperr, 2)

# analog/ref sigmas
ar1_upper, ar1_lower = calc_sigmas(r1, aerr, 1)
ar2_upper, ar2_lower = calc_sigmas(r1, aerr, 2)

plt.figure()

# reference
plt.plot(np.append(ratios, ext_x), np.append(r1, 1), label='E/Ref=1', ls='-', marker='', lw=.9,
         color=ref_color)
# wwig/reference
plt.plot(ratios, wgratio, label='WWIG/Ref', ls='', marker='d', lw=.9,
         color=wwig_color)
plt.plot(ratios, wgr1_upper, label='WWIG/Ref $\pm 1\sigma$',
         ls='--', lw=.75, color=wwig_color)
plt.plot(ratios, wgr1_lower, label='', ls='--', lw=.75, color=wwig_color)
plt.plot(ratios, wgr2_upper, label='WWIG/Ref $\pm 2\sigma$',
         ls=':', lw=.75, color=wwig_color)
plt.plot(ratios, wgr2_lower, label='', ls=':', lw=.75, color=wwig_color)
# wwinp/reference
plt.errorbar(ext_x, [1], yerr=(wpratio * wperr),
             label='CWWM/Ref $\pm 1\sigma$', ls='', marker='', lw=.9,
             capsize=cs, color=wwinp_color)
plt.plot(ext_x, wpratio, label='CWWM/Ref', ls='',
         marker='x', lw=.9, color=wwinp_color)
# analog/reference
plt.errorbar(ext_x, [1], yerr=(aratio * aerr),
             label='Analog/Ref $\pm 1\sigma$', ls='', marker='', lw=.9,
             capsize=cs, color=analog_color)
plt.plot(ext_x, aratio, label='Analog/Ref', ls='', marker='o', lw=.9,
         color=analog_color)

plt.xlabel('WWIG surface spacing ratio')
plt.ylabel('Ratio (E/Reference)')
plt.title('Point Detector Tally Results,\n compared to reference results')
plt.legend(bbox_to_anchor=(0.5, -.3), loc='lower center', ncol=4,
           fontsize='x-small')
plt.tight_layout()

plt.savefig('tally15_ratios.png', dpi=dpi)

# plot relative errors
plt.figure()
plt.plot(ref_xs[:len(ratios)], ref_err[:len(ratios)], label='Reference',
         ls='-', marker='', lw=.9, color=ref_color)
plt.plot(ratios, wwig_err, label='WWIG', ls='-', marker='d', lw=.9,
         color=wwig_color)
plt.plot(ratios, wwinp_err, label='CWWM', ls='--', marker='', lw=.9,
         color=wwinp_color)
plt.plot(ratios, analog_err, label='Analog', ls='-.', marker='', lw=.9,
         color=analog_color)
plt.xlabel('WWIG surface spacing ratio')
plt.ylabel('Relative Error')
plt.title('Point Detector Tally Relative Error')
plt.legend(bbox_to_anchor=(0.5, -.21), loc='lower center', ncol=4, fontsize='x-small')
plt.tight_layout()
plt.savefig('tally15_error.png', dpi=dpi)



## calculate p-value
# [mean, error, sample size]
num_hist = 1e6
ref_hist = 1e7
ref_sample = {'Tally': [ref_res[0], ref_err[0]*ref_res[0], ref_hist]}
analog_sample = {'Tally': [analog_res[0], analog_err[0]*analog_res[0], num_hist]}
wwinp_sample = {'Tally': [wwinp_res[0], wwinp_err[0]*wwinp_res[0], num_hist]}
wwig_samples = {}

for i, ratio in enumerate(ratios):
    key = 'r={}'.format(ratio)
    wwig_dict = {'Tally': [wwig_res[i], wwig_err[i]*wwig_res[i], num_hist]}
    wwig_samples[key] = wwig_dict

ana_ref_tt = tt.t_test(ref_sample, analog_sample)
wwinp_ref_tt = tt.t_test(ref_sample, wwinp_sample)

wwig_ref_tt = {}
for ratio, sample in wwig_samples.items():
    tt_res = tt.t_test(ref_sample, sample)
    wwig_ref_tt[ratio] = tt_res

print('Analog')
print(ana_ref_tt)

print('CWWM')
print(wwinp_ref_tt)

print('WWIG')
for ratio, tt_res in wwig_ref_tt.items():
    print(ratio)
    print(tt_res)
    tt.print_rej_summary(tt_res, .05, 0, verbose=2)

plt.show()

