
import numpy as np
from matplotlib import pyplot as plt

# Time of last vehicle infection for all the topologies
newyork_7005 = [0.00755, 0.0437, 0.0801, 0.1158, 0.16335, 0.19315000000000002, 0.23915, 0.27245, 0.3128, 0.34935, 0.38005, ]
newyork_3005 = [0.0076500000000000005, 0.0443, 0.07980000000000001, 0.12725, 0.1492, 0.18675, 0.217, 0.2606, 0.2869, 0.32545, 0.38235, ]
luxembourg_1000 = [0.00935, 0.05185, 0.10325000000000001, 0.15445, 0.20850000000000002, 0.25075000000000003, 0.29975, 0.32305, 0.37255, 0.42925, 0.46795000000000003, ]
luxembourg_50 = [0.01705, 0.12575, 0.2265, 0.3211, 0.44265000000000004, 0.5555, 0.6438, 0.7100500000000001, 0.8856, 0.9618000000000001, 1.0461, ]
cologne_1000 = [0.01955, 0.12145, 0.22690000000000002, 0.33585000000000004, 0.44225000000000003, 0.51715, 0.6585000000000001, 0.74145, 0.8527, 0.95435, 1.0915000000000001, ]
cologne_50 = [0.01755, 0.11495000000000001, 0.19790000000000002, 0.30625, 0.3947, 0.4923, 0.55805, 0.641, 0.72355, 0.8239000000000001, 0.9342, ]

# tmax values values
x = np.linspace(0, 100, 11)

def plot_config():
    plt.rcParams.update({'font.size': 18.3})
    plt.rc('legend', fontsize=13)
    plt.rc('xtick', labelsize=13.5)
    plt.rc('ytick', labelsize=11.5)
    plt.rc('grid', linestyle="--", color='black')
    plt.gcf().subplots_adjust(bottom=0.16)

    plt.ylabel('Transmission time (s)')
    plt.xlabel(r'$\frac{T_{max}}{\theta}$')
    plt.ylim((-0.05, 1.15))

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
plt.legend()
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
plt.legend()
#plt.show()
plt.savefig("grafici/invited/imgs/tx_time/all_low_dens.png", dpi=300)