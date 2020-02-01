
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import sys
sys.path.append("src")
from sim_config import config
from simulator import performSimulations


tmax_vals = np.linspace(0, 0.2, 9)
t_last_infctd_vals = np.zeros_like(tmax_vals)
ratios_infected_vals = np.zeros_like(tmax_vals)
sent_msgs_vals = np.zeros_like(tmax_vals)


for i, tmax in enumerate(tmax_vals):
    config.Tmax = tmax
    
    res = performSimulations(config.nsimulations)
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
print("TMAX VALS")
mypprint(tmax_vals)
print("T LAST INFCTD")
mypprint(t_last_infctd_vals)


def make_plot_frwd_recv(n_cars, means_recv_ratio, means_frwd, labels=None):
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



    plt.ylabel('Nodes (%)')
    plt.xlabel(r'$T_{max}$ (ms)')
    plt.title('')
    if not labels is None:
        plt.xticks(ind, labels) 
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.ylim((0.0, 1.0))


    #plt.legend((p1[0], p2[0], p4[0]), ('Relay', r'EPIC avg $\delta =43.8$', r'EPIC avg $\delta =11.6$'), 
    #    loc='upper center', bbox_to_anchor=(0.465, 1.15), fancybox=True, shadow=True, ncol=5)

    plt.legend((p1[0], p2[0]), ('Relay', 'Receivers'), 
        loc='upper center', bbox_to_anchor=(0.465, 1.15), fancybox=True, shadow=True, ncol=5)

    plt.gcf().subplots_adjust(bottom=0.15, left=0.15)
    plt.show()
    #plt.savefig('grafici/top_car/rmin_comparison.png', dpi=300)


def make_plot_time(tmax_vals, t_last_infctd_vals):
    plt.plot(tmax_vals*1000, t_last_infctd_vals)
    plt.ylabel('Transmission time (s)')
    plt.xlabel(r'$T_{max}$ (ms)')
    plt.show()


labels = map(lambda x: f"{1000*x:.0f}", tmax_vals)
make_plot_frwd_recv(
    n_cars,
    ratios_infected_vals,
    sent_msgs_vals,
    labels=labels
)

make_plot_time(
    tmax_vals,
    t_last_infctd_vals
)


"""
RUNS:


{
    "ncpus": 4,
    "nsimulations": 20,
    "time_resolution": 0.0001,
    "Tmax": 0.3,
    "Tmin": 0,
    "Rmin": 170,
    "Rmax": 500,
    "drop": 0.01,
    "alpha": 0.05,
    "city_name": "Luxembourg",
    "scenario": "time27100Tper1000.txt"
}

RATIOS
[0.9968354430379747, 0.984493670886076, 0.9838607594936709, 0.9822784810126582, 0.9835443037974684, 0.9835443037974684, 0.9857594936708861, ]
SENT_MSGS
[726.0, 290.0, 284.75, 241.0, 239.75, 238.5, 264.5, ]
TMAX VALS
[0.0, 0.03333333333333333, 0.06666666666666667, 0.1, 0.13333333333333333, 0.16666666666666666, 0.2, ]

"""