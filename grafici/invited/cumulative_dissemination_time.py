
from matplotlib import pyplot as plt
import numpy as np

import sys
sys.path.append("src")
from sim_config import config
from simulator import performSimulations

MAX_T = 10**4  #max simulation tick

def computeInfectionTime():
    sims = performSimulations(config.nsimulations)
    """
    # Retrieve highest simulation tick
    max_t = 0
    for sim in sims:
        if len(sim.t_infected) == 0:
            continue
        max_t = max(max_t, max(sim.t_infected.keys()))
    """

    # Array counting infected nodes at each time t
    infected = np.zeros(MAX_T+1, dtype=float)

    # Populate
    for sim in sims:
        for t, n in sim.t_infected.items():
            infected[t] += n

    # "Integrate"
    prev = 0
    for t, n in enumerate(infected):
        infected[t] += prev
        prev = infected[t]

    # Take the average
    infected /= len(sims)

    # Normalize by the number of cars
    infected /= len(sims[0].cars)

    return infected


# pyplot config
plt.rcParams.update({'font.size': 18.3})
plt.rc('legend', fontsize=13)
plt.rc('xtick', labelsize=13.5)
plt.rc('ytick', labelsize=11.5)
plt.rc('grid', linestyle="--", color='black')



topologies = [
    ("NewYork", "Newyork5005.mat"),
    ("Luxembourg", "time27100Tper1000.txt"),
    ("Cologne", "time23000Tper1000.txt")
]

rmins = [600, 170, 120]
labels = ["New York", "Luxembourg", "Cologne"]
colors = ["blue", "red", "green"]
x = np.arange(MAX_T+1) * config.time_resolution * 1000   #ms

for i, (city, scenario) in enumerate(topologies):
    config.city_name = city
    config.scenario = scenario
    config.Rmin = rmins[i]
    inf = computeInfectionTime()

    # Extend values up to the greater simulation tick
    for t in range(1, len(inf)):
        if inf[t] == 0.0:
            inf[t] = inf[t-1]

    plt.plot(x, inf, label=labels[i], color=colors[i])

plt.gcf().subplots_adjust(bottom=0.15)
plt.ylabel('Nodes (%)')
plt.xlabel('Time (ms)')
plt.legend()
plt.grid(True)

plt.show()

