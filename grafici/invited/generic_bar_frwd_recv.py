import numpy as np
import matplotlib
import matplotlib.pyplot as plt


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

if __name__ == "__main__":
    inf_ratio = [0.99734177, 0.98512658, 0.88582278, 0.98126582, 0.98392405, 0.9835443, 0.98373418, 0.98468354, 0.98436709]
    sent = [732.5 , 297.55, 245.15, 261.6 , 243.15, 242.15, 246.05, 245.65, 253.85]
    n_cars = 790

    make_plot(n_cars, inf_ratio, sent)
