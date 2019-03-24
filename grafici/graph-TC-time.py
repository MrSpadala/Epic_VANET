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

plt.rcParams.update({'font.size': 18.5})
plt.rc('legend', fontsize=13)
plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=11.5)

N = 3

means_high_dens = (2.7106, 5.70025, 1.12181)
means_low_dens = (6.1696, 5.1731, 1.46935)

ind = np.arange(N)    # the x locations for the groups
width = 0.28       # the width of the bars: can also be len(x) sequence

fig, ax = plt.subplots()

gap = 0.07

#ffc500
#cc6e00

p1 = plt.bar(ind, means_high_dens, width, color='#ffc500', edgecolor='k')
p2 = plt.bar(ind+width+gap, means_low_dens, width, color='#cc6e00', edgecolor='k')

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

plt.ylabel('Delay (s)')
plt.title('')
plt.xticks(ind+width/2+gap/2, ('Luxemburg', 'Cologne', 'New York'))
plt.yticks(np.arange(0, 6.1, 1.0))
plt.legend((p1[0], p2[0]), ('High density', 'Low density'), loc='upper right')

#plt.show()
plt.savefig('grafici/top_car/time.png', dpi=300)