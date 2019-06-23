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
plt.rc('legend', fontsize=12.5)
plt.rc('xtick', labelsize=17)
plt.rc('ytick', labelsize=11.5)


N = 4
means_infected = (0.9725-0.575, 0.985-350/790, 0.978-300/790, 0.988-0.27)
means_frw = (0.575, 350/790, 300/790, 0.27)
ind = np.arange(N)    # the x locations for the groups
width = 0.28       # the width of the bars: can also be len(x) sequence

fig, ax = plt.subplots()

gap = 0.07

p1 = plt.bar(ind, means_frw, width, color='b', edgecolor='k')
p2 = plt.bar(ind, means_infected, width,
             bottom=means_frw, color='#ffa500', edgecolor='k')
#p3 = plt.bar(ind+width+gap, means_frw_low, width, color='b', edgecolor='k')
#p4 = plt.bar(ind+width+gap, means_infected_low, width,
#             bottom=means_frw_low, color='#cc6e00', edgecolor='k')

'''
# Shrink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
#ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
  #        fancybox=True, shadow=True, ncol=5)



plt.ylabel('Nodes (%)')
plt.title('')
plt.xticks(ind+width+gap, ('Luxemburg', 'Cologne', 'New York'))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.legend((p2[0], p4[0], p3[0]), ('Receivers high density', 'Receivers low density', 'Forwarders'), 
	loc='upper center', bbox_to_anchor=(0.5, -0.08),
    fancybox=True, shadow=True, ncol=5)
'''


# average degree
# x50 11.662007623888183
# x100 24.79695431472081
# x200 35.97969543147208
# x1000 43.8379746835443


plt.ylabel('Nodes (%)')
plt.xlabel(r'avg. degree $\delta$')
plt.title('')
plt.xticks(ind, ('11.6', '24.8', '35.9', '43.8'))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.ylim((0,1))
plt.legend((p1[0], p2[0]), ('Relay', 'EPIC'),
      loc='upper center', bbox_to_anchor=(0.44, 1.15),
          fancybox=True, shadow=True, ncol=5)

plt.gcf().subplots_adjust(left=0.15, right=0.95, bottom=0.15)



#plt.show()
plt.savefig('grafici/top_car/frw_recv_slides.png', dpi=300)