"""import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple


n_groups = 3

means_alg = (20, 35, 30, 35, 27)
std_men = (2, 3, 4, 1, 2)

means_women = (25, 32, 34, 20, 25)
std_women = (3, 5, 2, 3, 3)



index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = ax.bar(index, means, bar_width,
                alpha=opacity, color='b',
                yerr=std_men, error_kw=error_config,
                label='Men')

rects2 = ax.bar(index + bar_width, means_women, bar_width,
                alpha=opacity, color='r',
                yerr=std_women, error_kw=error_config,
                label='Women')

ax.set_xlabel('Group')
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(('Luxemburg', 'Cologne', 'New York'))
#ax.legend()

fig.tight_layout()
plt.show()
"""


import numpy as np
import matplotlib.pyplot as plt


plt.rcParams.update({'font.size': 18.3})
plt.rc('legend', fontsize=10.3)
plt.rc('xtick', labelsize=13.5)
plt.rc('ytick', labelsize=11.5)


N = 3
#means_infected_low = (0.9128-(305.71/787), 0.9542-(143.53/220), 0.9405-(155.61/433))
#means_frw_low = (355.48/790, 143.53/220, 155.61/433)

'''
means_recv = (0.9917-(355.48/790), 0.9463-(222.75/436), 0.9547-(118.63/600))
means_frw = (305.71/787, 222.75/436, 118.63/600)

means_frw_low = (133.8/790, 72.78/436, 18.86/600)
means_low_prob = (0.3745-means_frw_low[0], 0.366- means_frw_low[1], 0.1552- means_frw_low[2])

means_frw_high = (702/790, 385.5/436, 540.6/600)
means_high_prob = (0.9362-means_frw_high[0], 0.9459- means_frw_high[1], 0.9398- means_frw_high[2])
'''

means_high_dens = (7.78, 15.925, 6.52)
means_low_dens = (13.18, 12.29, 7.02)

means_prob_high_dens = (7.5675, 15.24, 5.99)
means_prob_low_dens = (13.71, 11.5, 6.855)

ind = np.arange(N)    # the x locations for the groups
width = 0.12       # the width of the bars: can also be len(x) sequence

#fig, ax = plt.subplots()
fig = plt.figure()
ax = plt.subplot(111)

gap = 0.065

scale = 0.5
plt.figure(figsize=(15*scale, 10*scale))

p1 = plt.bar(ind, means_high_dens, width, color='#ffc500', edgecolor='k')
p2 = plt.bar(ind+width+gap, means_low_dens, width, color='#cc6e00', edgecolor='k')
#p3 = plt.bar(ind+width+gap, means_frw_low, width, color='b')
#p4 = plt.bar(ind+width+gap, means_infected_low, width,
#             bottom=means_frw_low, color='#cc6e00')

p3 = plt.bar(ind+2*width+2*gap, means_prob_high_dens, width, color='#00e000', edgecolor='k')
p4 = plt.bar(ind+3*width+3*gap, means_prob_low_dens, width, color='g', edgecolor='k')

'''
p5 = plt.bar(ind+2*width+2*gap, means_frw_low, width, color='b', edgecolor='k')
p6 = plt.bar(ind+2*width+2*gap, means_low_prob, width,
             bottom=means_frw_low, color='#00bb00', edgecolor='k')
'''

#plt.text(2.4, 0.9,'drop_rate = 0.03',{'size':11})

# Shrink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
#ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
  #        fancybox=True, shadow=True, ncol=5)



plt.ylabel('Hops')
plt.title('')
plt.xticks(ind+3*width/2+3*gap/2, ('Luxemburg', 'Cologne', 'New York'))
plt.yticks(np.arange(0, 19, 2))
plt.legend((p1[0], p2[0], p3[0], p4[0]), ('High density', 'Low density', 'Prob. high dens.', 'Prob. low dens.'), 
	loc='upper center', bbox_to_anchor=(0.47, -0.08),
    fancybox=True, shadow=True, ncol=5)


plt.gcf().subplots_adjust(bottom=0.15, left=0.15)
#plt.show()
plt.savefig('hops.png', dpi=300)