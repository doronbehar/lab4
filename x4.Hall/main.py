import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib(True)
from uncertainties import ufloat, umath

# Testing two different curve fit methods
from scipy.optimize import curve_fit
# To calculate errors in fit parameters
from scipy.stats import distributions

plt.rcParams['text.usetex'] = True

# measurements
I_raw = np.linspace(-30,30,13)
U_raw = [
    # {{{ Data
    -1.264,
    -1.063,
    -0.8595,
    -0.653,
    -0.479,
    -0.2572,
    0,
    0.1748,
    0.3714,
    0.5913,
    0.7218,
    0.9548,
    1.1202,
    # }}}
]
# In this case every measurement has the same error
U = [ufloat(val, 0.05) for val in U_raw]*ureg.volt
I = [ufloat(val, 0.1) for val in I_raw]*ureg.mA

y = U
x = I
plt.errorbar(
    I_raw,
    U_raw,
    yerr=[val.magnitude.std_dev for val in U],
    xerr=[val.magnitude.std_dev for val in I],
    fmt='b.',
    label='measurements'
)

def func(I, R):
    return I*R

# calculate error of fit, based upon:
# https://kitchingroup.cheme.cmu.edu/blog/2013/02/12/Nonlinear-curve-fitting-with-parameter-confidence-intervals/
pars, pcov = curve_fit(func, I_raw, U_raw)
alpha = 0.05 # 95% confidence interval = 100*(1-alpha)
n = len(U_raw)    # number of data points
p = len(pars) # number of parameters
dof = max(0, n - p) # number of degrees of freedom
# student-t value for the dof and confidence level
tval = distributions.t.ppf(1.0-alpha/2., dof) 
# Only 1 value in this covariance matrix
R_0 = (ureg.volt/ureg.mA * ufloat(pars[0], umath.sqrt(pcov[0][0])*tval)).to('ohm')
# TODO: Calculate r-square and p-value of fit, use:
# https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit/37899817#37899817

label=r'fit: $R_0 = {:L}\Omega$'.format(
   R_0.magnitude
)
plt.plot(
    I_raw*ureg.mA,
    func(I_raw, *pars)*ureg.volt,
    'g--',
    label=label
)
# May be useful, but can't force it the fit of it to pass through (0,0)
#  from scipy.stats import linregress
#  res = linregress(I_raw, U_raw)
#  plt.plot(
    #  I_raw*ureg.mA,
    #  (res.intercept + res.slope*I_raw)*ureg.volt,
    #  'r--',
    #  label='linregeress: R = %5.3f' % res.slope
#  )
plt.legend()
plt.savefig('R_0.pgf')
# https://github.com/texworld/tikzplotlib produces ugly errorbars
#  import tikzplotlib
#  tikzplotlib.save("R_0.tex")

#  plt.show()
