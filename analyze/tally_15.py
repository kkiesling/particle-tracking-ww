import numpy as np
import matplotlib.pyplot as plt


## Data

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


plt.figure()
plt.errorbar(c_u, wwinp, yerr=(wwinp_err*wwinp), label='WWINP', ls='', marker='D', lw=.75)
plt.errorbar(c_u, wwig20, yerr=(wwig20_err*wwig20), label='WWIG r=20', ls='', marker='D', lw=.75)
plt.errorbar(c_u, wwig50, yerr=(wwig50_err*wwig50), label='WWIG r=50', ls='', marker='D', lw=.75)
plt.errorbar(c_u, wwig100,yerr=(wwig100_err*wwig100), label='WWIG r=100', ls='', marker='D', lw=.75)
plt.xlabel('WW Upper Bound Constant c_u')
plt.ylabel('Detector Tally Results')
plt.legend()

plt.savefig('temp_results.png')

plt.figure()
plt.errorbar(c_u, wwig20/wwinp, yerr=(wwig20_err*wwig20), label='WWIG r=20', ls='', marker='D', lw=.75)
plt.errorbar(c_u, wwig50/wwinp, yerr=(wwig50_err*wwig50), label='WWIG r=50', ls='', marker='D', lw=.75)
plt.errorbar(c_u, wwig100/wwinp,yerr=(wwig100_err*wwig100), label='WWIG r=100', ls='', marker='D', lw=.75)
plt.errorbar(c_u, analog/wwinp,yerr=(analog_err*analog), label='analog', ls='', marker='D', lw=.75)
plt.legend()

plt.figure()
plt.plot(c_u, analog_err, label='analog', ls='-', marker='', lw=.75)
plt.plot(c_u, wwinp_err, label='WWINP', ls='-', marker='D', lw=.75)
plt.plot(c_u, wwig20_err, label='WWIG r=20', ls='-', marker='D', lw=.75)
plt.plot(c_u, wwig50_err, label='WWIG r=50', ls='-', marker='D', lw=.75)
plt.plot(c_u, wwig100_err, label='WWIG r=100', ls='-', marker='D', lw=.75)
plt.legend()


plt.show()
