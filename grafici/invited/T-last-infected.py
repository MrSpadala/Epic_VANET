
import numpy as np
from matplotlib import pyplot as plt

# Time of last vehicle infection for all the topologies
newyork = [0.0076, 0.0152, 0.0216, 0.029050000000000003, 0.04105, 0.045950000000000005, 0.055600000000000004, 0.06555, 0.0733, 0.08360000000000001, 0.08775000000000001, ]
luxembourg = [0.00945, 0.03735, 0.0694, 0.1077, 0.12865000000000001, 0.15405000000000002, 0.20035, 0.22965000000000002, 0.24265, 0.27640000000000003, 0.30145, ]
cologne = [0.0207, 0.08415, 0.15315, 0.2353, 0.3256, 0.35455000000000003, 0.45795, 0.4975, 0.5698, 0.5618500000000001, 0.7252500000000001, ]

# tmax values values
x = np.linspace(0, 0.1, 11) * 1000


# pyplot config
plt.rcParams.update({'font.size': 18.3})
plt.rc('legend', fontsize=13)
plt.rc('xtick', labelsize=13.5)
plt.rc('ytick', labelsize=11.5)
plt.rc('grid', linestyle="--", color='black')
plt.gcf().subplots_adjust(bottom=0.15)

plt.ylabel('Transmission time (s)')
plt.xlabel(r'$T_{max}$ (ms)')

plt.scatter(x, newyork, label="New York", marker="o", color="blue")
plt.scatter(x, luxembourg, label="Luxembourg", marker="s", color="red")
plt.scatter(x, cologne, label="Cologne", marker="^", color="green")

plt.legend()

# Grid
plt.grid(True)

plt.show()