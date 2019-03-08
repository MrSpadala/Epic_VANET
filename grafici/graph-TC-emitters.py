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


N = 6

'''
means_infected_low = (0.9128-(305.71/787), 0.9542-(143.53/220), 0.9405-(155.61/433))
means_frw_low = (355.48/790, 143.53/220, 155.61/433)
means_infected = (0.9917-(355.48/790), 0.9463-(222.75/436), 0.9547-(118.63/600))
means_frw = (305.71/787, 222.75/436, 118.63/600)
'''
cnum = 790  #cars number

x = np.asarray((100,10,5,3,2,1))
frw = np.asarray((330.136, 345.506, 356.647, 357.763, 362.719, 384.708)) / cnum
recv = np.asarray((0.9323, 0.934, 0.9467, 0.9365, 0.9432, 0.9494)) - frw
#x, frw, recv = np.flip(x), np.flip(frw), np.flip(recv)

ind = np.arange(N)    # the x locations for the groups
width = 0.3       # the width of the bars: can also be len(x) sequence

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

gap = 0.07

p1 = ax1.bar(ind, frw, width, color='b', edgecolor='k')
p2 = ax1.bar(ind, recv, width,
             bottom=frw, color='#ffa500', edgecolor='k')

p1 = ax2.bar(ind, frw, width, color='b', edgecolor='k')
p2 = ax2.bar(ind, recv, width,
             bottom=frw, color='#ffa500', edgecolor='k')


#p1 = ax.plot(x, frw)
#p1 = ax.plot(x, recv)

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

plt.ylabel('Nodes (%)')
plt.xlabel('Emitters Length Limit')
plt.title('')
plt.xticks(ind, ('1', '2', '3', '5', '10', 'Unlimited'))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.legend((p1[0], p2[0]), ('Relayers', 'Reached'), loc='lower center')

plt.show()
#plt.savefig('top_car/emitters.png', dpi=300)