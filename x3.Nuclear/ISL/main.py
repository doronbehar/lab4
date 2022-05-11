import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib(True)
from uncertainties import ufloat, umath
from uncertainties.unumpy import uarray
plt.rcParams['text.usetex'] = True
# To fit the modulation's sin
from scipy.optimize import curve_fit
# To calculate errors in fit parameters
from scipy.stats import distributions

import pandas as pd

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from background import noise

def plotAndFit(df):
    counts1 = np.divide(
        df['Counts'].values,
        df['Time'].values
    )
    counts1_err=np.divide(
        np.sqrt(df['Counts'].values),
        df['Time'].values
    )
    plt.errorbar(
        df['Number'].values,
        counts1,
        xerr=0.1*ureg.cm,
        yerr=counts1_err,
        fmt=".",
        label="measurements"
    )

    # Perform fit to I(t) to get I_0
    def isl_fit(r, m, a):
        return m/(r+a) + noise.m.n
    popt, pcov = curve_fit(
        isl_fit, df['Number'].values, counts1,
        p0=df.attrs['popt_matlab'],
        # Use the standard deviation to determine a weight for each measurement
        sigma=counts1_err,
        # Weights are absolute, not relative
        absolute_sigma=True
    )
    # TODO: Get Rsquare and all that jazz from pcov
    distances_seq = np.linspace(df['Number'].min(), df['Number'].max(), 100)
    plt.plot(
        distances_seq,
        isl_fit(distances_seq, *popt),
        label=r'Python Fit $\sim \frac{1}{r+a} + n$'
    )
    plt.plot(
        distances_seq,
        isl_fit(distances_seq, *df.attrs['popt_matlab']),
        label=r'Matlab Fit $\sim \frac{1}{r+a} + n$'
    )

    plt.xlabel('Relative Distance [cm]')
    plt.ylabel('Counts [Hz]')
    plt.legend()
    plt.savefig("{}.pgf".format(df.attrs['matter']))
    plt.savefig("{}.png".format(df.attrs['matter']))
    plt.show()


df1 = pd.read_csv("./Ti-204_0.25uCi_3.78Yrs_Dec2019.tsv", skiprows=10, index_col=False, sep="\t")
#  Coefficients (with 95% confidence bounds):
       #  a =     -0.0585  (-0.3468, 0.2298)
       #  m =       161.6  (119.9, 203.3)
#  Goodness of fit:
  #  SSE: 634
  #  R-square: 0.9733
  #  Adjusted R-square: 0.97
  #  RMSE: 8.902
df1.attrs = {
    'matter': "Thallium-204_March2020",
    'popt_matlab': [161.1, -0.0585]
}
plotAndFit(df1)
df2 = pd.read_csv("./Sr-90_0.1uCi_28.8Yrs_Nov2014.tsv", skiprows=10, index_col=False, sep="\t")
#  Coefficients (with 95% confidence bounds):
       #  a =    -0.09377  (-0.3116, 0.124)
       #  m =       315.7  (251.4, 380.1)
#  Goodness of fit:
  #  SSE: 1582
  #  R-square: 0.9834
  #  Adjusted R-square: 0.9813
  #  RMSE: 14.06
df2.attrs = {
    'matter': "Strontium-90_Nov2014",
    'popt_matlab': [315.7, -0.09377],
}
plotAndFit(df2)
