"""
Comparison of different msg threshold number of CBF
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import sys
sys.path.append("src")
import sim_config
from simulator import performSimulations, computeMetrics
from graph_utils.other_stats import get_avg_degree



def plt_config():
    plt.rcParams.update({'font.size': 18.3})
    plt.rc('legend', fontsize=13)
    plt.rc('xtick', labelsize=13.5)
    plt.rc('ytick', labelsize=11.5)


city_scenario = {
    "Luxembourg": [
        "time27100Tper1000.txt",
        "time27100Tper50.txt"
    ],
    "Cologne": [
        "time23000Tper1000.txt",
        "time23000Tper50.txt"
    ],
    "NewYork": [
        "Newyork7005.mat",
        "Newyork3005.mat"
    ]
}


N = 6   #plot for k=1 to k=N

sim_config.config.use_CBF = True

for city, scenarios in city_scenario.items():
    rcv_high_dens = np.zeros(N)
    rcv_low_dens  = np.zeros(N)
    frw_high_dens = np.zeros(N)
    frw_low_dens  = np.zeros(N)
    rcv = [rcv_high_dens, rcv_low_dens]
    frw = [frw_high_dens, frw_low_dens]
    avg_degree = [0, 0]

    for i, scenario in enumerate(scenarios):  #two scenarios per city, they must be in order high density then low density
        sim_config.config.city_name = city
        sim_config.config.scenario = scenario
        sim_config.load_opt_parameters()
        avg_degree[i] = get_avg_degree()

        for k in range(1, N+1):
            sim_config.config.CBF_msg_thresh = k
            sims = performSimulations(sim_config.config.nsimulations)
            res = computeMetrics(sims)
            n_cars, sent_msgs, recv_msgs, t_last_infect, cars_infected_ratio, network_traffic = res

            frw[i][k-1] = sent_msgs / n_cars  #normalize in [0,1]
            rcv[i][k-1] = cars_infected_ratio - frw[i][k-1]   #ratio of vehicles received that didn't forward
                
    fig = plt.figure()
    plt_config()
    ax = plt.subplot(111)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.21       # the width of the bars: can also be len(x) sequence
    gap = 0.075
    scale = 0.5

    plt.figure(figsize=(15*scale, 10*scale))

    p1 = plt.bar(ind, frw[0], width, color='b', edgecolor='k')
    p2 = plt.bar(ind, rcv[0], width, bottom=frw[0], color='#ffa500', edgecolor='k')

    p3 = plt.bar(ind+width+gap, frw[1], width, color='b', edgecolor='k')
    p4 = plt.bar(ind+width+gap, rcv[1], width, bottom=frw[1], color='#cc6e00', edgecolor='k')

    #plt.text(2.4, 0.9,'drop_rate = 0.03',{'size':11})

    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                    box.width, box.height * 0.9])

    plt.ylabel('Nodes (%)')
    plt.xlabel(r'$K$', fontsize=14.5)
    plt.title('')
    plt.xticks(ind+width/2+gap/2, ind+1) 
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.ylim((0.0, 1.0))

    #plt.legend((p3[0], p2[0], p6[0], p4[0]), ('Relayers', 'Reached', r'Probabilistic $P=\widehat{P}$', r'Probabilistic $P=0.96$'), 
    #	loc='upper center', bbox_to_anchor=(0.5, -0.08),
    #    fancybox=True, shadow=True, ncol=5)
    plt.legend((p1[0], p2[0], p4[0]), ('RR', r'PDR, avg $\delta ='+f'{avg_degree[0]:.1f}$', r'PDR, avg $\delta ='+f'{avg_degree[1]:.1f}$'), 
        loc='upper center', bbox_to_anchor=(0.465, 1.15), fancybox=True, shadow=True, ncol=5)

    plt.gcf().subplots_adjust(bottom=0.11, left=0.11)
    #plt.show()

    city, scenario = sim_config.config.city_name, sim_config.config.scenario
    plt.savefig(f'grafici/invited/imgs/CBF_k/{city}-{scenario}.png', dpi=300); plt.clf()