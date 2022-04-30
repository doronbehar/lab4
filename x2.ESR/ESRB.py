import numpy as np
import matplotlib.pyplot as plt
import pint
# Use the same registry
from main import ureg
ureg.setup_matplotlib(True)
from uncertainties import ufloat, umath, unumpy
import pandas as pd
from scipy.signal import find_peaks
from scipy.integrate import simpson
from scipy.optimize import curve_fit
plt.rcParams['text.usetex'] = True

amp = 700*ureg.mV
R=ufloat(0.82, 0.82*0.1)*ureg.ohm

df = pd.read_csv("./ESRB.csv")
# The I0_modulation signal is horrible, the system was too noisy, so instead:
#
#  I0_modulation = (unumpy.uarray(
    #  df['V_modulation_raw'].values,
    #  df['V_modulation_err'].values
#  )*ureg.mV/R).to('ampere')
#
# we regnerate it, assuming it should be linear, just as V_DC is.
I0_modulation = (unumpy.uarray(np.linspace(
    df['V_modulation_raw'].min(),
    df['V_modulation_raw'].max(),
    len(df)
), df['V_modulation_err'].mean())*ureg.mV/R).to('ampere')

ptp_Y = unumpy.uarray(
    df['ptp_Y_raw'].values*df['phase_sign'].values,
    df['ptp_Y_err'].values
)*ureg.mV
ptp_X_modulation = ufloat(3.09, 0.01)*ureg.mV

fig, ax = plt.subplots()
I0_modulation_err = np.array([val.m.s for val in I0_modulation])
I0_modulation_raw = np.array([val.m.n for val in I0_modulation])
ptp_ratio = ptp_Y/ptp_X_modulation
absorption_deriviative = ptp_ratio/max(ptp_ratio)
absorption_deriviative_raw = np.array([val.m.n for val in absorption_deriviative])
absorption_deriviative_err = np.array([val.m.s for val in absorption_deriviative])
ax.errorbar(
    I0_modulation_raw*ureg.ampere,
    absorption_deriviative_raw, # Dimensionless
    fmt='.',
    yerr=absorption_deriviative_err,
    # TODO: Mention in report that error is too big to be drafted
    #xerr=I_modulation_err,
    # TODO: Is this the correct label?
    label='Absorption Deriviative'
)

def lorentzian_dif_fit(I, I0, gamma, amplitude):
    return amplitude*(-2*(gamma**2)*(I - I0))/ \
            (gamma**2 + (I - I0)**2)**2
def lorentzian_fit(I, I0, gamma, amplitude):
    return amplitude*gamma**2/\
            (gamma**2 + (I - I0)**2)**2
##### By MATLAB:
#  Goodness of fit:
#  SSE: 0.197
#  R-square: 0.9845
#  Adjusted R-square: 0.9838
#  RMSE: 0.06769
#               I0      gamma    amplitude
matlab_p0    = [0.5479, 0.03847, 0.05554]
matlab_bounds=((0.547,  0.03672,  0.05304),
               (0.5488, 0.04021,   0.05805))
I_rf = ufloat(matlab_p0[0], abs(matlab_bounds[0][0] - matlab_p0[0]))*ureg.ampere
I_hwhm = ufloat(matlab_p0[1], abs(matlab_bounds[0][1] - matlab_p0[1]))*ureg.ampere

from main import g_times_bohr
# TODO: Take this value from Itamar & Tomer
H_RF = ufloat(34.914, 0.009)*ureg.gauss
k = H_RF/I_rf
# Converts current I To frequency f using all of the constants
def I2f(I):
    return (I*k*g_times_bohr/ureg.planck_constant).to('megahertz')

f0_modulation = I2f(I0_modulation)
f_rf = I2f(I_rf)
f_hwhm = I2f(I_hwhm)
T2 = (1/f_hwhm).to('nanosecond')

##### A failing Python fit attempt - I consider it as a failure because it hits
##### the bounds :/
#  popt, pcov = curve_fit(
    #  lorentzian_dif_fit, absorption_deriviative_raw, I0_modulation_raw,
    #  p0=matlab_p0, bounds=matlab_bounds
#  )
#  lorentzian_dif_fit_points = lorentzian_dif_fit(I0_modulation_raw, *popt)
#  ax.plot(
    #  I0_modulation_raw*ureg.ampere,
    #  lorentzian_dif_fit_points,
    #  label="Python fit"
#  )

I0_modulation_seq = np.linspace(
    I0_modulation.min().m.n,
    I0_modulation.max().m.n,
    len(I0_modulation)*100
)
ax.plot(
    I0_modulation_seq*ureg.ampere,
    lorentzian_dif_fit(I0_modulation_seq, I_rf.m.n, I_hwhm.m.n, matlab_p0[2]),
    label="Matlab fit"
)
ax.set_yticks([])
axt = ax.twiny()
axt.grid(linestyle='--')
axt.set_yticks([])
f0_modulation_seq = np.linspace(
    f0_modulation.min().m.n,
    f0_modulation.max().m.n,
    len(f0_modulation)*100
)
def lorentzian_wrapper(f0):
    # From some reason this need to be amplified by a factor of 800 so it will
    # look good.
    return lorentzian_fit(f0, f_rf.m.n, f_hwhm.m.n, matlab_p0[2]*800)
axt.plot(
    f0_modulation_seq*ureg.megahertz,
    lorentzian_wrapper(f0_modulation_seq),
    label = "Lorenzian fit", color='green'
)
axt.set_xticks(
    [(f_rf - f_hwhm).m.n, f_rf.m.n, (f_rf + f_hwhm).m.n],
    ['', '$f_{rf}$', '']
)
axt.set_xlabel('')
axt.arrow(
    length_includes_head = True,
    x = (f_rf - f_hwhm).m.n*ureg.megahertz,
    y = lorentzian_wrapper((f_rf - f_hwhm).m.n),
    dx = 2*f_hwhm.m.n*ureg.megahertz,
    dy = 0,
    head_length = f_hwhm.m.n/10,
    head_width = matlab_p0[2],
    label="Full Width Half Max",
)
axt.arrow(
    length_includes_head = True,
    x = (f_rf + f_hwhm).m.n*ureg.megahertz,
    y = lorentzian_wrapper((f_rf + f_hwhm).m.n),
    dx = -2*f_hwhm.m.n*ureg.megahertz,
    head_length = f_hwhm.m.n/10,
    head_width = matlab_p0[2],
    dy = 0,
)
axt.text(
    0.5, 0.63,
    #  (f_hwhm.m.n/10),
    #  lorentzian_wrapper((f0 - f_hwhm).m.n)*2,
    "FWHM",
    transform=ax.transAxes,
    #  fontsize=00
)
ax.legend(loc='upper right')
#  axt.legend(loc='upper left')
plt.show()
fig.savefig("ESRB.pgf")
fig.savefig("ESRB.png")

# TODO: Integrate numerically / or fit to a laurenzian's differentiation

# TODO: Scale the x axis to frequency and find the width of the laurenzian in
# frequency scale
