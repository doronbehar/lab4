import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib(True)
from uncertainties import ufloat, umath
from uncertainties.unumpy import uarray
plt.rcParams['text.usetex'] = True

import pandas as pd
import os

df = pd.read_csv("{}/noise.tsv".format(os.path.dirname(os.path.realpath(__file__))), skiprows=10, index_col=False, sep="\t")

noise = np.mean(np.divide(
    uarray(df['Counts'].values, np.sqrt(df['Counts'].values)),
    df['Time'].values*ureg.sec
).to('hertz'))

print("Background noise is {}".format(noise))
