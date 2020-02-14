
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import sys
sys.path.append("src")
from sim_config import config
from simulator import performSimulations, computeMetrics


if config.city_name == "Luxembourg":
    if config.scenario.endswith("1000.txt"):
        rmin_vals = np.linspace(120, 220, 9)   #luxemburg high density
    elif config.scenario.endswith("50.txt"):
        rmin_vals = np.linspace(40, 140, 9)   #luxemburg low density
    else:
        raise Exception("scenario density not implemented")
elif config.city_name == "Cologne":
    rmin_vals = np.linspace(70, 170, 9)   #cologne
elif config.city_name == "NewYork":
    rmin_vals = np.linspace(530, 730, 9)   #ny
else:
    raise Exception("not implemented")

if config.use_CBF:
    # If we use CBF we don't care about Rmin, we just use one value
    rmin_vals = rmin_vals[:1]

t_last_infctd_vals = np.zeros_like(rmin_vals)
ratios_infected_vals = np.zeros_like(rmin_vals)
sent_msgs_vals = np.zeros_like(rmin_vals)


for i, rmin in enumerate(rmin_vals):
    config.Rmin = rmin
    
    sims = performSimulations(config.nsimulations)
    res = computeMetrics(sims)
    n_cars, sent_msgs, recv_msgs, t_last_infect, cars_infected_ratio, network_traffic = res

    t_last_infctd_vals[i] = t_last_infect
    ratios_infected_vals[i] = cars_infected_ratio
    sent_msgs_vals[i] = sent_msgs

def mypprint(arr):
    print("[", end="")
    for v in arr:
        print(f"{v}, ", end="")
    print("]")

print("RATIOS")
mypprint(ratios_infected_vals)
print("SENT_MSGS")
mypprint(sent_msgs_vals)
print("RMIN VALS")
mypprint(rmin_vals)




def make_plot(n_cars, means_recv_ratio, means_frwd, labels=None):

    assert(len(means_recv_ratio) == len(means_frwd))
    N = len(means_recv_ratio)

    # pyplot config
    plt.rcParams.update({'font.size': 18.3})
    plt.rc('legend', fontsize=13)
    plt.rc('xtick', labelsize=13.5)
    plt.rc('ytick', labelsize=11.5)

    means_frwd_ratio = np.asarray(means_frwd) / n_cars
    means_recv_ratio = np.asarray(means_recv_ratio) - means_frwd_ratio


    ind = np.arange(N)    # the x locations for the groups
    width = 0.3       # the width of the bars: can also be len(x) sequence

    #plt.bar(ind, means)

    #fig, ax = plt.subplots()
    fig = plt.figure()
    ax = plt.subplot(111)

    gap = 0.075

    scale = 0.5
    plt.figure(figsize=(15*scale, 10*scale))

    p1 = plt.bar(ind, means_frwd_ratio, width, color='b', edgecolor='k')
    p2 = plt.bar(ind, means_recv_ratio, width,
                bottom=means_frwd_ratio, color='#ffa500', edgecolor='k')


    """
    p3 = plt.bar(ind+width+gap, means_frw_low_dens, width, color='b', edgecolor='k')
    p4 = plt.bar(ind+width+gap, means_recv_ratio_low_dens, width,
                bottom=means_frw_low_dens, color='#cc6e00', edgecolor='k')
    """


    #plt.text(2.4, 0.9,'drop_rate = 0.03',{'size':11})

    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                    box.width, box.height * 0.9])

    if config.city_name == "Luxembourg":
        plt.hlines(279/790,-0.3,8.3, colors="g", linestyles="--")  #LUXEMBOURG CSC
    elif config.city_name == "Cologne":
        plt.hlines(214/436,-0.3,8.3, colors="g", linestyles="--")  #COLOGNE CSC
    elif config.city_name == "NewYork":
        pass   # NO COMPARISON WITH NY AVAILABLE YET
    else:
        raise Exception("not implemented")

    plt.ylabel('Nodes (%)')
    plt.xlabel(r'$R_{min}$ (m)')
    plt.title('')
    if not labels is None:
        plt.xticks(ind, map(str, labels)) 
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.ylim((0.0, 1.0))


    #plt.legend((p1[0], p2[0], p4[0]), ('Relay', r'EPIC avg $\delta =43.8$', r'EPIC avg $\delta =11.6$'), 
    #    loc='upper center', bbox_to_anchor=(0.465, 1.15), fancybox=True, shadow=True, ncol=5)

    plt.legend((p1[0], p2[0]), ('Relay', 'Receivers'), 
        loc='upper center', bbox_to_anchor=(0.465, 1.15), fancybox=True, shadow=True, ncol=5)

    plt.gcf().subplots_adjust(bottom=0.15, left=0.15)
    plt.show()
    #plt.savefig('grafici/top_car/rmin_comparison.png', dpi=300)


labels = map(lambda x: f"{x:.0f}", rmin_vals)
make_plot(
    n_cars,
    ratios_infected_vals,
    sent_msgs_vals,
    labels=labels
)
