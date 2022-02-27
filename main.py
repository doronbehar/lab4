import pint

ureg = pint.UnitRegistry()
ureg.setup_matplotlib(True)
import matplotlib.pyplot as plt
import numpy as np
y = np.linspace(0, 30) * ureg.miles
x = np.linspace(0, 5) * ureg.seconds
fig, ax = plt.subplots()
ax.plot(x, y, 'tab:blue')
plt.show()
#ax.axhline(26400 * ureg.feet, color='tab:red')
#ax.axvline(120 * ureg.seconds, color='tab:green');
