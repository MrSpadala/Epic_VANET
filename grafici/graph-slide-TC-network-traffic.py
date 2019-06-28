
from matplotlib import pyplot as plt 
from matplotlib.ticker import FuncFormatter
import numpy as np


plt.rcParams.update({'font.size': 13})
plt.rc('legend', fontsize=12.5)
plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=11.5)
plt.rc('axes', titlesize=11)
plt.rc('axes', labelsize=13)



def kilobytes(x, pos):
    '''The two args are the value and tick position'''
    return '%1.0fKB' % (x*1e-3)
def bytes(x, pos):
	return '%1.0f' % x

formatter = FuncFormatter(kilobytes)
formatter_bytes = FuncFormatter(bytes)

fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(formatter)
ax.xaxis.set_major_formatter(formatter_bytes)



#(249/790)*(7+22*6+x) > (608/790)*(7+x)

overhead_msg  = 5+6
overhead_epic = 22*3+overhead_msg

f_epic, f_prb60, f_prb93, f_wp = 243, 478, 724, 569

X_MAX = 175

x_lux = np.arange(0, X_MAX+1, 5 )
l1 = f_epic  * (overhead_epic+x_lux)
l2 = f_prb93 * (overhead_msg+x_lux)
l3 = f_prb60 * (overhead_msg+x_lux)
l4 = f_wp    * (overhead_msg+x_lux)
p1 = ax.plot(x_lux, l1, 'firebrick', linewidth=2)
p2 = ax.plot(x_lux, l2, 'k', linewidth=2)
p3 = ax.plot(x_lux, l3, 'b', linewidth=2)
p4 = ax.plot(x_lux, l4, 'darkgreen', linewidth=2)

ax.legend((p1[0], p2[0], p3[0], p4[0]), ('EPIC', r'$P = 0.93$', r'$P = 0.6$', 'w-p-Persistence'))

#ax.set_xlabel('Message size (Bytes)')
fig.text(0.54, 0.032, 'Payload length (bytes)', ha='center', va='center')
#fig.text(0.325, 0.91, 'Luxemburg', ha='center', va='center')
ax.set_ylabel('Total network traffic (Kbytes)')


ax.set_ylim(0, 100000)
ax.set_xlim(5, X_MAX)


plt.gcf().subplots_adjust(left=0.15, right=0.95)

#plt.show()
plt.savefig('grafici/top_car/traffic_comparison.png', dpi=300)




