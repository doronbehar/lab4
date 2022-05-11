import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib(True)
from uncertainties import ufloat, umath
plt.rcParams['text.usetex'] = True

import pandas as pd

dfd5 = pd.read_csv("./doron5.tsv", skiprows=10, index_col=False, sep="\t")
plt.plot(
    dfd5['Voltage'].values*ureg.volt,
    np.divide(
        dfd5['Counts'].values,
        dfd5['Time'].values*ureg.sec
    ).to('hertz'),
    '.',
    label="Strontium-90 - Nov 2014"
)
plt.legend()
plt.savefig("plateau1.pgf")
plt.savefig("plateau1.png")
plt.show()

dfs2 = pd.read_csv("./sarah2.tsv", skiprows=10, index_col=False, sep="\t")
plt.plot(
    dfs2['Voltage'].values*ureg.volt,
    np.divide(
        dfs2['Counts'].values,
        dfs2['Time'].values*ureg.sec
    ).to('hertz'),
    '.',
    label="Thallium-204 - March 2020"
)
plt.legend()
plt.savefig("plateau2.pgf")
plt.savefig("plateau2.png")
plt.show()
