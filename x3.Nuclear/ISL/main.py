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
        return m/(r+a)**2 + noise.m.n
    popt, pcov = curve_fit(
        isl_fit, df['Number'].values, counts1,
        p0=df.attrs['p0'],
        # Use the standard deviation to determine a weight for each measurement
        sigma=counts1_err,
        # Weights are absolute, not relative
        absolute_sigma=True
    )
    distances_seq = np.linspace(df['Number'].min(), df['Number'].max(), 100)
    plt.plot(
        distances_seq,
        isl_fit(distances_seq, *popt),
        label=r'Fit $\sim \frac{1}{(r+a)^2} + n$'
    )
    # calculate error of fit, based upon:
    # https://kitchingroup.cheme.cmu.edu/blog/2013/02/12/Nonlinear-curve-fitting-with-parameter-confidence-intervals/
    alpha = 0.05 # 95% confidence interval = 100*(1-alpha)
    n = len(df) # number of data points
    p = len(popt) # number of parameters
    dof = max(0, n - p) # number of degrees of freedom
    # student-t value for the dof and confidence level
    tval = distributions.t.ppf(1.0-alpha/2., dof) 
    popt_err = np.sqrt(np.diag(pcov))*tval
    # Calculate r-square and p-value of fit, based upon:
    # https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit/37899817#37899817
    residuals = counts1 - isl_fit(df['Number'].values, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((counts1-np.mean(counts1))**2)
    r_squared = 1 - (ss_res / ss_tot)
    a = ufloat(popt[1], popt_err[1])

    plt.xlabel('Relative Distance [cm]')
    plt.ylabel('Counts [Hz]')
    plt.legend()
    plt.savefig("{}.pgf".format(df.attrs['matter']))
    plt.savefig("{}.png".format(df.attrs['matter']))
    plt.show()

    return {'R^2': r_squared, 'a': a}

df1 = pd.read_csv("./Ti-204_0.25uCi_3.78Yrs_Dec2019.tsv", skiprows=10, index_col=False, sep="\t")
df1.attrs = {
    'matter': "Thallium-204_March2020",
    # Got these from matlab originally ;/
    'p0': [161.1, -0.0585]
}
df1.attrs['fitResults'] = plotAndFit(df1)
df2 = pd.read_csv("./Sr-90_0.1uCi_28.8Yrs_Nov2014.tsv", skiprows=10, index_col=False, sep="\t")
df2.attrs = {
    'matter': "Strontium-90_Nov2014",
    # Got these from matlab originally ;/
    'p0': [315.7, -0.09377],
}
df2.attrs['fitResults'] = plotAndFit(df2)

a = np.array([df2.attrs['fitResults']['a'], df1.attrs['fitResults']['a']]).mean()

df3 = pd.read_csv("./Po-210_0.1uCi_8Nov2021_filtered.tsv", skiprows=10, index_col=False, sep="\t")
x_data = df3['Distance'].values + 1 # Plus 1 for the shelves offset
counts = np.divide(df3['Counts'].values, df3['Time'].values) - noise.m.n
y_data = np.divide(counts, np.power(x_data + a.n,-2))
y_data = y_data/max(y_data)
plt.plot(x_data, y_data, '.', label="counts normalized")
plt.hlines(0.5, x_data.min(), x_data.max(), linestyles="dashed", colors='red', label="Half Intensity")
# xl = 1.1882, yl = 0.6020, xr = 1.3902, yr=0.3102
x_data_f = np.delete(x_data, 1)
y_data_f = np.delete(y_data, 1)
yu = y_data_f[x_data_f.argmax()]
xu = x_data_f.max()
yl = y_data_f[x_data_f.argmin()]
xl = x_data_f.min()
plt.plot(
    [xl, xu],
    [yl, yu],
'g', label="Linear Interpolation")
m = (yl - yu)/(xl - xu)
# The position where the linear graph hits the y = 0.5 line
R_m = 1.32227
plt.vlines(R_m, 0, 1, linestyles='dashed', colors='black')
plt.plot([R_m], [0.5], 'o')
plt.xticks(ticks=[R_m], labels=['$R_m$'])
plt.yticks(ticks=[0,0.5,1])
plt.legend()
plt.savefig("Polonium-210-range.pgf")
plt.savefig("Polonium-210-range.png")
plt.show()
