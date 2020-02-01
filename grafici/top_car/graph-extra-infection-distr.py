
from matplotlib import pyplot as plt
import pickle
from matplotlib.ticker import FuncFormatter
import numpy as np

tmax = 150
t_infected = pickle.load(open(f'grafici/runs/t_infected_normalized_TMAX-{tmax}.0.pickle', 'rb'))

N = 150

n_sum = 0
t1, t2 = 0.9*sum(t_infected[:2*N]), 0.99*sum(t_infected[:2*N])
print(t1,t2)
for i in range(len(t_infected[:2*N])):
    if n_sum<t1 and t_infected[i]+n_sum>=t1:
        print(f'{0.9} at {i}') 
    if n_sum<t2 and t_infected[i]+n_sum>=t2:
        print(f'{0.99} at {i}') 
    n_sum += t_infected[i]

#print(sum(t_infected))


def seconds(x, pos):
    '''The two args are the value and tick position'''
    return '%1.2fs' % (x*1e-2)

fig, ax = plt.subplots()

formatter = FuncFormatter(seconds)
ax.xaxis.set_major_formatter(formatter)

ax.plot(np.arange(N), t_infected[:N], 'firebrick', linewidth=2)

ax.set_ylim((0,0.07))
ax.set_xlim((-5,N))

plt.title('Infection distribution vs. time ')

#plt.show()
plt.savefig(f'grafici/top_car/infection-rate-TMAX-{tmax}.png', dpi=300)