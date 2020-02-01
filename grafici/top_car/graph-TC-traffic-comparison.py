
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

fig, (ax1, ax2) = plt.subplots(1,2, sharey=False)
ax1.yaxis.set_major_formatter(formatter)
ax2.yaxis.set_major_formatter(formatter)
ax1.xaxis.set_major_formatter(formatter_bytes)
ax2.xaxis.set_major_formatter(formatter_bytes)



#(249/790)*(7+22*6+x) > (608/790)*(7+x)

overhead_epic = 22*5+5+6
overhead_prb  = 5+6

x_lux = np.arange(0, 405, 1)
l1 = (249) * (overhead_epic+x_lux)
l2 = (608) * (overhead_prb+x_lux)
p1 = ax1.plot(l1, label='EPIC Luxemburg')
p2 = ax1.plot(l2, label='Probabilistic Luxembourg')

x_col = np.arange(0, 405, 1)
l1_col = 173 * (overhead_epic+x_col)
l2_col = 342 * (overhead_prb+x_col)
p3 = ax2.plot(l1_col, label='EPIC Cologne')
p4 = ax2.plot(l2_col, label='Probabilistic Cologne')

ax1.legend((p1[0], p2[0]), ('EPIC', 'Probabilistic'))

#ax1.set_xlabel('Message size (Bytes)')
fig.text(0.54, 0.032, 'Payload length (bytes)', ha='center', va='center')
fig.text(0.325, 0.91, 'Luxemburg', ha='center', va='center')
fig.text(0.765, 0.91, 'Cologne', ha='center', va='center')
ax1.set_ylabel('Total network traffic (Kbytes)')

ax1.set_ylim(21000, 61000)
ax1.set_xlim(40, 100)
ax2.set_ylim(21000, 61000)
ax2.set_xlim(50, 150)

plt.gcf().subplots_adjust(left=0.15, right=0.95)

plt.show()
#plt.savefig('grafici/top_car/traffic_comparison.png', dpi=300)




