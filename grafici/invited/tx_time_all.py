
import numpy as np
from matplotlib import pyplot as plt

# MUST BE THE SAME used when generating the data below
THETA = 0.0025

# Time of last vehicle infection for all the topologies
newyork_7005 = (1/THETA) * np.array([0.007350000000000001, 0.019350000000000003, 0.03065, 0.043500000000000004, 0.05745, 0.06805, 0.0792, 0.09395, 0.11405, 0.1188, 0.13745000000000002, ])
newyork_3005 = (1/THETA) * np.array([0.0076500000000000005, 0.0198, 0.03355, 0.04505, 0.05885, 0.06935000000000001, 0.07965, 0.09620000000000001, 0.11025, 0.1105, 0.12645, ])
luxembourg_1000 = (1/THETA) * np.array([0.009550000000000001, 0.0239, 0.04125, 0.05885, 0.07295, 0.09095, 0.10745, 0.11415, 0.1306, 0.1484, 0.16315000000000002, ])
luxembourg_50 = (1/THETA) * np.array([0.0176, 0.056, 0.0917, 0.12090000000000001, 0.15625, 0.19125, 0.227, 0.26745, 0.3042, 0.3317, 0.38470000000000004, ])
cologne_1000 = (1/THETA) * np.array([0.0223, 0.04995, 0.0806, 0.12445, 0.15885000000000002, 0.19265000000000002, 0.24735000000000001, 0.25775000000000003, 0.28435, 0.33485000000000004, 0.34855, ])
cologne_50 = (1/THETA) * np.array([0.0181, 0.0482, 0.07995000000000001, 0.10990000000000001, 0.1427, 0.17395000000000002, 0.188, 0.2366, 0.2631, 0.30295, 0.29935, ])

# tmax values values
x = np.linspace(0, 20, 11)

def plot_config():
    plt.rcParams.update({'font.size': 18.3})
    plt.rc('legend', fontsize=13)
    plt.rc('xtick', labelsize=13.5)
    plt.rc('ytick', labelsize=11.5)
    plt.rc('grid', linestyle="--", color='black')
    plt.gcf().subplots_adjust(bottom=0.16, left=0.13)

    plt.ylabel(r'Transmission time $\left(\frac{D}{\theta}\right)$')
    plt.xlabel(r'$\frac{T_{max}}{\theta}$')
    plt.ylim((-14, 175))

    plt.grid(True)

# High density
plot_config()
plt.scatter(x, newyork_7005, label="New York", marker="o", color="blue")
plt.scatter(x, luxembourg_1000, label="Luxembourg", marker="s", color="red")
plt.scatter(x, cologne_1000, label="Cologne", marker="^", color="green")
plt.plot(x, newyork_7005, marker="o", color="blue", linewidth=0.8)
plt.plot(x, luxembourg_1000, marker="s", color="red", linewidth=0.8)
plt.plot(x, cologne_1000, marker="^", color="green", linewidth=0.8)
plt.title("High Density", fontsize=15)
plt.legend(loc="upper left")
#plt.show()
plt.savefig("grafici/invited/imgs/tx_time/all_high_dens.png", dpi=300)
plt.clf()

plot_config()
plt.scatter(x, newyork_3005, label="New York", marker="o", color="blue")
plt.scatter(x, luxembourg_50, label="Luxembourg", marker="s", color="red")
plt.scatter(x, cologne_50, label="Cologne", marker="^", color="green")
plt.plot(x, newyork_3005, marker="o", color="blue", linewidth=0.8)
plt.plot(x, luxembourg_50, marker="s", color="red", linewidth=0.8)
plt.plot(x, cologne_50, marker="^", color="green", linewidth=0.8)
plt.title("Low Density", fontsize=15)
plt.legend(loc="upper left")
#plt.show()
plt.savefig("grafici/invited/imgs/tx_time/all_low_dens.png", dpi=300)