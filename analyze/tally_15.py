import numpy as np
import matplotlib.pyplot as plt
import math as m
import twosample_ttest as tt
from scipy import stats


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
plt.plot(np.append(ratios, ext_x), np.append(r1, 1), label='$E/F=1$', ls='-', marker='', lw=.9,
         color=ref_color)
plt.plot(np.append(ratios, ext_x), ref_err + 1, label='$E/F \pm 1\sigma$', ls='--', marker='', lw=.9,
         color=ref_color)
plt.plot(np.append(ratios, ext_x), -ref_err + 1, ls='--', marker='', lw=.9,
         color=ref_color)
plt.plot(np.append(ratios, ext_x), 2.*ref_err + 1, label='$E/F \pm 2\sigma$', ls=':', marker='', lw=.9,
         color=ref_color)
plt.plot(np.append(ratios, ext_x), -2.*ref_err + 1, ls=':', marker='', lw=.9,
         color=ref_color)
# wwig/reference
plt.errorbar(ratios, wgratio, yerr=(wgerr * wgratio), label='$WWIG/F$', ls='', marker='d', lw=.9,
             color=wwig_color, capsize=cs)
# wwinp/reference
plt.errorbar(ext_x, wpratio, yerr=(wpratio * wperr),
             label='$CWWM/F \pm 1\sigma$', ls='', marker='x', lw=.9,
             capsize=cs, color=wwinp_color)
# analog/reference
plt.errorbar(ext_x, aratio, yerr=(aratio * aerr),
             label='$Analog/F \pm 1\sigma$', ls='', marker='o', lw=.9,
             capsize=cs, color=analog_color)
plt.xlabel('WWIG surface spacing ratio')
plt.ylabel('Ratio (E/Reference)')
plt.title('Point Detector Tally Results,\n compared to reference results')
plt.legend(bbox_to_anchor=(0.5, -.3), loc='lower center', ncol=6,
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
alpha = 0.01
print("ALPHA {}".format(alpha))
print("t_val, df, p_val, t_crit, reject, [rse1, rse2]")
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

ana_ref_tt = tt.t_test(ref_sample, analog_sample, alpha)
wwinp_ref_tt = tt.t_test(ref_sample, wwinp_sample, alpha)

wwig_ref_tt = {}
for ratio, sample in wwig_samples.items():
    tt_res = tt.t_test(ref_sample, sample, alpha)
    wwig_ref_tt[ratio] = tt_res

print('Analog')
print(ana_ref_tt)

print('CWWM')
print(wwinp_ref_tt)

print('WWIG')
for ratio, tt_res in wwig_ref_tt.items():
    print(ratio)
    print(tt_res)
    #tt.print_rej_summary(tt_res, .05, 0, verbose=2)

#plt.show()


#########################3

# Test of equivalence (TOST)

def calc_allowable_discrepancy(m1, m2, delta):
    """for a given allowable discrepancy (eg 20%, delta=0.2), calculate
    the upper and lower bounds of the difference.

    Inputs:
    -------
        m1, m2: floats, the means of the two samples
        delta: float, allowable relative differnce

    Returns
    -------
        bound: float, absolute difference bound
    """
    bound = delta * (m1 + m2) / 2.0
    return bound


def calc_sigma_pooled(m1, e1, n1, m2, e2, n2):
    s1 = m1 * e1
    s2 = m2 * e2
    sigma_p = m.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2.))
    return sigma_p


def calc_t_bounds(m1, e1, n1, m2, e2, n2, cohens):
    """calculate the upper and lower t-values given the means, standard
    deviations, sample sizes, and acceptable discrepancies.

    Input:
    ------
        m1, m2: floats, means
        s1, s2: floats, standard deviations
        n1, n2: ints (or floats), sample sizes
        bound: float, absolute value of the acceptable absolute discrepancy

    Returns:
    --------
        t_L, t_U: floats, lower and upper t-values
    """
    sigma_p = calc_sigma_pooled(m1, e1, n1, m2, e2, n2)
    bound = sigma_p * cohens
    bound_up = abs(bound)
    bound_low = -abs(bound)
    t_L = (m1 - m2 - bound_low) / \
        (sigma_p * m.sqrt(1. / float(n1) + 1. / float(n2)))
    t_U = (m1 - m2 - bound_up) / \
        (sigma_p * m.sqrt(1. / float(n1) + 1. / float(n2)))
    return t_L, t_U, bound


def calc_df(m1, e1, n1, m2, e2, n2):
    """calculate the degrees of freedom"""
    s1 = m1 * e1
    s2 = m2 * e2
    n1 = float(n1)
    n2 = float(n2)
    df = (s1**2 / n1 + s2**2 / n2)**2 / \
        ((s1**2 / n1)**2 / (n1 - 1) + (s2**2 / n2)**2 / (n2 - 1))
    return int(df)


def calc_confidence_interval(m1, e1, n1, m2, e2, n2):
    pass


def analyze_tost(res, err):
    # calculate this stuff
    # delta = 0.2

    cohens = abs(res - ref_res[0]) / m.sqrt(((res*err)**3 + (ref_res[0]*ref_err[0])**3) / 2)
    # get t-values
    t_L, t_U, bound = calc_t_bounds(res, err, num_hist, ref_res[0], ref_err[0], ref_hist, cohens)

    df = calc_df(res, err, num_hist, ref_res[0], ref_err[0], ref_hist)
    t_crit = round(stats.t.ppf(1.0 - alpha, df), 3)

    dL = -bound
    dU = bound
    diff = ref_res[0] - res
    within_descrepancy = False
    if dL <= diff <= dU:
        within_descrepancy = True

    # decide if the t values should be rejected
    reject_upper = False
    reject_lower = False
    if t_U <= -t_crit:
        reject_upper = True
    if t_L >= t_crit:
        reject_lower = True

    stat_equiv = False
    if reject_lower and reject_upper:
        stat_equiv = True

    # calc confidence level


    # print results
    print('allowable diff: {}'.format(bound))
    print('actual diff: {}'.format(diff))
    print('within bounds: {}'.format(within_descrepancy))
    print('df: {}'.format(df))
    print('t_crit: {}'.format(t_crit))
    print('t_L: {}'.format(t_L))
    print('t_U: {}'.format(t_U))
    #print('reject upper: {}'.format(reject_upper))
    #print('reject lower: {}'.format(reject_lower))
    print('Statistically Equivalent? {}'.format(stat_equiv))


print('****TOST****')
print("\n*ANALOG*")
analyze_tost(analog_res[0], analog_err[0])
print("\n*CWWM*")
analyze_tost(wwinp_res[0], wwinp_err[0])

for i, r in enumerate(ratios):
    print("\n*WWIG* r = {}".format(r))
    analyze_tost(wwig_res[i], wwig_err[i])

plt.show()
