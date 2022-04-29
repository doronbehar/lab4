import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib(True)
from uncertainties import ufloat, umath
import pandas as pd
from scipy.signal import find_peaks
# To fit the modulation's sin
from scipy.optimize import curve_fit
# To calculate errors in fit parameters
from scipy.stats import distributions

plt.rcParams['text.usetex'] = True

R = (ufloat(0.33,0.05*0.33) + ufloat(0.47,0.1*0.47))*ureg.ohm

oscillator_feedback_knob = ufloat(30,1)

oscillator_feedback_knob_zero = 98.6 * ureg.MHz
oscillator_feedback_knob_13 = 98.3 * ureg.MHz

ni_RF = (oscillator_feedback_knob_13 - oscillator_feedback_knob_zero)/13 * \
        oscillator_feedback_knob + oscillator_feedback_knob_zero
# There's a bug in pint's library with gaussian units, haven't found the time
# to debug it, so I'm not using `ureg.bohr_magneton`. **This value is taken
# from the manual**.
g_DPPH_factor = ufloat(2.0036, 0.0002) 
g_times_bohr = g_DPPH_factor*9274.01008*ureg.yoctoerg/ureg.gauss
H0 = ((ureg.planck_constant*ni_RF).to('erg')/g_times_bohr).to('gauss')

dfdc = pd.read_csv("./dc-measurement.csv", header=None, usecols=[1,2,3], names=['t','1','2'])
dfdc.attrs = {
    'p0': [50, 0.2,0, -0.4],
    'bounds': ((45,0.1,0, -0.6), (55, 0.4, 2*np.pi, -0.3)),
    'xlim': [-0.075, 0.015],
    'inset_axes': [0.05, 0.4, 0.2, 0.2],
    'x1': -0.0335437, 'y1': -0.55201,
    'x2': -0.0333357, 'y2': -0.53408,
    'zoom_type': 'periodicity',
    'fname': 'dc-measurement'
}
dfeg = pd.read_csv("./energy-gap-measurement.csv", header=None, usecols=[1,2,3], names=['t','1','2'])
dfeg.attrs = {
    'p0': [50, 0.5,0, -0],
    # It should have a 0 offset, so the bounds are that small
    'bounds': ((45,0.4,0, -0.0001), (55, 0.6, 2*np.pi, 0.0001)),
    'zoom_type': 'maximas',
    'fname': 'energy-gap-measurement'
}

def plotAndFit(df, show=True):
    fig, ax = plt.subplots()
    I_modulation = (df['1'].values*ureg.volt/R).to('ampere')
    I_modulation_err = np.array([val.m.s for val in I_modulation])
    I_modulation_raw = np.array([val.m.n for val in I_modulation])
    ax.errorbar(
        df['t'].values*ureg.s,
        I_modulation_raw*ureg.ampere,
        # TODO: Explain in report that error is not shown, but it was considered
        # during curve_fit
        #yerr=I_modulation_err,
        color='blue',
        label='Modulation'
    )
    ax.tick_params(axis='y', color='blue', labelcolor='blue')
    # Perform fit to I(t) to get I_0
    def sin_fit(t, freq, a, phase, offset):
        return a*np.sin(2*np.pi*freq*t + phase) + offset
    popt, pcov = curve_fit(
        sin_fit, df['t'], I_modulation_raw,
        p0=df.attrs['p0'],
        bounds=df.attrs['bounds'],
        # Use the standard deviation to determine a weight for each measurement
        sigma=I_modulation_err,
        # Weights are absolute, not relative
        absolute_sigma=True
    )
    sin_fit_points = sin_fit(df['t'].values, *popt)

    # calculate error of fit, based upon:
    # https://kitchingroup.cheme.cmu.edu/blog/2013/02/12/Nonlinear-curve-fitting-with-parameter-confidence-intervals/
    alpha = 0.05 # 95% confidence interval = 100*(1-alpha)
    n = len(df)    # number of data points
    p = len(popt) # number of parameters
    dof = max(0, n - p) # number of degrees of freedom
    # student-t value for the dof and confidence level
    tval = distributions.t.ppf(1.0-alpha/2., dof) 
    popt_err = np.sqrt(np.diag(pcov))*tval
    I_0_fit = ufloat(popt[3], popt_err[3])*ureg.ampere
    I_amp = ufloat(popt[1],popt_err[1])*ureg.ampere
    # Calculate r-square and p-value of fit, based upon:
    # https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit/37899817#37899817
    residuals = I_modulation_raw - sin_fit(df['t'].values, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((I_modulation_raw-np.mean(I_modulation_raw))**2)
    r_squared = 1 - (ss_res / ss_tot)
    with open("{}.rsquare.tex".format(df.attrs['fname']), 'w') as ftex:
        ftex.write(r'$R^2 = {:.2f}$'.format(r_squared))

    ax.hlines(
        I_0_fit.m.n*ureg.ampere,
        df['t'].min()*ureg.s, df['t'].max()*ureg.s,
        colors='black',
        label="$I_0$",
        linestyles='dotted'
    )

    # Put the absorption in a different scale
    absorption = df['2']
    absorption_color = '#e1c126'
    axt = ax.twinx()
    axt.tick_params(axis='y', colors=absorption_color)
    axt.plot(
        df['t'].values*ureg.s,
        # Plotting without units, as they are irrelevant
        absorption.values*ureg.volt,
        color=absorption_color,
        label='Absorption'
    )
    peaks, _ = find_peaks(df['2'], height=1)
    axt.plot(
        df['t'].iloc[peaks].values*ureg.s,
        absorption.iloc[peaks].values,
        'x', color='green', label="Peaks"
    )
    # TODO: Figure out how to choose the limits of these lines
    axt.vlines(
        df['t'].iloc[peaks].values*ureg.s,
        absorption.min(),
        absorption.max(),
        colors='#ee10a7',
        linestyles='dashdot'
    )
    if df.attrs['zoom_type'] == 'periodicity':
        ax.set_xlim(*df.attrs['xlim'])
        axins = ax.inset_axes(df.attrs['inset_axes'])
        x1 = dfdc.attrs['x1']
        y1 = dfdc.attrs['y1']
        x2 = dfdc.attrs['x2']
        y2 = dfdc.attrs['y2']
        axins.set_xticks(
            [x1, x2],
            labels=[
                "{:.1f}".format(x1*1000),
                "{:.1f}".format(x2*1000)
            ]
        )
        axins.xaxis.tick_top()
        axins.set_xlabel("ms")
        axins.set_yticks([])
        axins.set_xlim(x1, x2)
        axins.set_ylim(y1, y2)
        # Plotting Modulation signal without errors, and without units, to not
        # clutter the plot
        axins.plot(
            df['t']*ureg.s,
            sin_fit_points,
            label="fit"
        )
        axins.hlines(
            I_0_fit.m.n,
            df['t'].min(), df['t'].max(),
            colors='black',
            linestyles='dotted'
        )
        axins.vlines(
            df['t'].iloc[peaks].values,
            sin_fit(dfdc['t'].iloc[peaks], *popt),
            absorption.iloc[peaks].values,
            colors='#ee10a7',
            linestyles='dashdot'
        )
        ax.indicate_inset_zoom(axins, edgecolor="black")

    if df.attrs['zoom_type'] == 'periodicity':
        axt.legend(loc='lower left')
        ax.legend(loc='upper left')
    elif df.attrs['zoom_type'] == 'maximas':
        axt.legend()
        ax.legend()
    #  fig.tight_layout()
    fig.savefig("{}.png".format(df.attrs['fname']))
    fig.savefig("{}.pgf".format(df.attrs['fname']))
    if show:
        plt.show()

    if df.attrs['zoom_type'] == 'periodicity':
        return I_0_fit
    elif df.attrs['zoom_type'] == 'maximas':
        return I_amp

I_DC_fit = plotAndFit(dfdc, False)
I_EG_fit = plotAndFit(dfeg, False)
# Hand made measurement
I_DC_manual_measure = ufloat(0.5148, 0.0001) * ureg.A

# k values are:
# - H0/I_DC_manual_measure 
# - H0/I_DC_fit
# - H0/I_EG_fit
#
# Use the propagated errors
