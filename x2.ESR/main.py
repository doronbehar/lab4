import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib(True)
from uncertainties import ufloat, umath
import pandas as pd
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

R = (ufloat(0.33,0.05*0.33) + ufloat(0.47,0.1*0.47))*ureg.ohm

oscillator_feedback_knob = ufloat(30,1)

oscillator_feedback_knob_zero = 98.6 * ureg.MHz
oscillator_feedback_knob_13 = 98.3 * ureg.MHz

ni_RF = (oscillator_feedback_knob_13 - oscillator_feedback_knob_zero)/13 * \
        oscillator_feedback_knob + oscillator_feedback_knob_zero
# There's a bug in pint's library with gaussian units, haven't found the time
# to debug it, so I'm not using `ureg.bohr_magneton`.
g_DPPH_factor = ufloat(2.0036, 0.0002)
g_times_bohr = g_DPPH_factor*9274.01008*ureg.yoctoerg/ureg.gauss
H0 = ((ureg.planck_constant*ni_RF).to('erg')/g_times_bohr).to('gauss')

# Not a good measurement - doesn't include enough data points.
dfdc = pd.read_csv("./dc-measurement.csv", header=None, usecols=[1,2,3], names=['t','1','2'])

fig, ax = plt.subplots()
I_modulation = (dfdc['1'].values*ureg.volt/R).to('ampere')
I_modulation_err = np.array([val.magnitude.std_dev for val in I_modulation])
I_modulation_raw = np.array([val.magnitude.nominal_value for val in I_modulation])
plt.errorbar(
    dfdc['t'].values*ureg.s,
    I_modulation_raw,
    # TODO: Explain in report that error is not shown, but it was considered
    # during curve_fit
    #yerr=I_modulation_err,
    label='Modulation'
)
# Perform fit to I(t) to get I_0
def sin_fit(t, freq, a, phase, offset):
    return a*np.sin(2*np.pi*freq*t + phase) + offset
popt, pcov = curve_fit(
    sin_fit, dfdc['t'], I_modulation_raw,
    p0=[50, 0.2,0, -0.4],
    # Use the standard deviation to determine a weight for each measurement
    sigma=I_modulation_err,
    # Weights are absolute, not relative
    absolute_sigma=True,
    bounds=((45,0.1,0, -0.6), (55, 0.4, 2*np.pi, -0.3))
)
I_0_fit = popt[3]
ax.hlines(
    I_0_fit*ureg.volt,
    dfdc['t'].min(), dfdc['t'].max(),
    colors='black',
    linestyles='dotted'
)
I_m_fit = popt[1]

# Put the absorption near the modulation signal, normalized, with amplitude
# slightly larger then I_m_fit
absorption = (I_m_fit + 0.1)*dfdc['2']/dfdc['2'].max() + I_0_fit
plt.plot(
    dfdc['t'].values*ureg.s,
    # Plotting without units, as they are irrelevant
    absorption,
    color='#e1c126',
    label='Absorption'
)
peaks, _ = find_peaks(dfdc['2'], height=1)
ax.plot(
    dfdc['t'].iloc[peaks].values*ureg.s,
    absorption.iloc[peaks].values,
    'x', label="Peaks"
)
ax.vlines(
    dfdc['t'].iloc[peaks].values*ureg.s,
    sin_fit(dfdc['t'].iloc[peaks], *popt),
    absorption.iloc[peaks].values,
    colors='#ee10a7',
    linestyles='dashdot'
)

ax.set_xlim(-0.075, 0.015)
axins = ax.inset_axes([0.05, 0.4, 0.2, 0.2])
x1, y1 = -0.0335184, -0.55463
x2, y2 = -0.0333473, -0.54059
zoom = 100/0.3
axins.set_xticks([x1, x2], labels=["{:.1f}".format(x1*1000), "{:.1f}".format(x2*1000)])
axins.xaxis.tick_top()
axins.set_xlabel("ms")
axins.set_yticks([])
#  axins.title("zoom")
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
# Plotting Modulation signal without errors, to not clutter the plot
axins.plot(
    dfdc['t']*ureg.s,
    I_modulation_raw,
    color='#e1c126',
    label="fit"
)
axins.hlines(
    I_0_fit,
    dfdc['t'].min(), dfdc['t'].max(),
    colors='black',
    linestyles='dotted'
)
axins.vlines(
    dfdc['t'].iloc[peaks].values,
    sin_fit(dfdc['t'].iloc[peaks], *popt),
    absorption.iloc[peaks].values,
    colors='#ee10a7',
    linestyles='dashdot'
)
ax.indicate_inset_zoom(axins, edgecolor="black")
plt.legend()
plt.show()

# TODO: Compare I_0_fit with error from pcov to this hand made measurement
I_DC = ufloat(0.5148, 0.0001) * ureg.A

# TODO: Compare the Vpp of ./part1Mes 0.csv

# TODO: Compute k of bio savare via selonoid's geometry and compare that with
# H0/I_0 and H0/I_DC , Use the propagated errors
