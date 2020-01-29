
import numpy as np

from sim_config import config
from simulator import performSimulations


tmax_vals = np.linspace(0, 0.2, 9)
t_last_infctd_vals = np.zeros_like(tmax_vals)
ratios_infected_vals = np.zeros_like(tmax_vals)
sent_msgs_vals = np.zeros_like(tmax_vals)


for i, tmax in enumerate(np.linspace(0, 0.2, 9)):
    config.Tmax = tmax
    
    res = performSimulations(config.nsimulations)
    n_cars, sent_msgs, recv_msgs, t_last_infect, cars_infected_ratio, network_traffic = res

    t_last_infctd_vals[i] = t_last_infect
    ratios_infected_vals[i] = cars_infected_ratio
    sent_msgs_vals[i] = sent_msgs

print("RATIOS")
print(ratios_infected_vals)
print("SENT_MSGS")
print(sent_msgs_vals)


from matplotlib import pyplot as plt
plt.plot(tmax_vals, t_last_infctd_vals)
plt.show() 