import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib(True)
from uncertainties import ufloat, umath

import pandas as pd

from scipy.signal import find_peaks

df = pd.read_csv("./high_res_16V_158-161C.csv", header=5, sep="\t")

metadata = np.genfromtxt("./high_res_16V_158-161C.csv", skip_header=2, max_rows=2,delimiter="=")
df.attrs['Vr(V)'] = metadata[0,1] * ureg.volt
df.attrs['Cathode Heater Current'] = metadata[1,1] * ureg.A

plt.plot(df['Va(V)_1'].values*ureg.volt, df['Ia(E-12 A)_1'].values*ureg.picoampere)

peaks, _ = find_peaks(df['Ia(E-12 A)_1'], height=150)

plt.plot(df['Va(V)_1'].iloc[peaks], df['Ia(E-12 A)_1'].iloc[peaks], "x")

plt.legend()
plt.show()
