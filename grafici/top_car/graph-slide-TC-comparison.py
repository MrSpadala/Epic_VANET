
import numpy as np
import matplotlib.pyplot as plt


SAVE_IMG = True


plt.rcParams.update({'font.size': 18.3})
plt.rc('legend', fontsize=10)
plt.rc('xtick', labelsize=17)
plt.rc('ytick', labelsize=11.5)


p93_reached = np.array([97.91,99.77,97.61,98.42]) / 100
p93_frw = np.array([724.06,735.92,720.79,727.26]) / 790
p93_reached = np.array(list(reversed(p93_reached)))
p93_frw = np.array(list(reversed(p93_frw)))

p60_reached = np.array([92.56,88.23,85.11,82.78]) / 100
p60_frw = np.array([478.53,477.30,460.37,439.17]) / 790
p60_reached = np.array(list(reversed(p60_reached)))
p60_frw = np.array(list(reversed(p60_frw)))

w_pers_reached = np.array([97.54,96.32,95.40,99.91]) / 100
w_pers_frw = np.array([577.78,553.9,542.75,569.41]) / 790

epic_reached = np.array([97.37,98.81,96.79,97.34]) / 100
epic_frw = np.array([387.59,331.92,303.21,239.54]) / 790

ind = np.arange(4)  # 4 densities


p1 = plt.plot(ind, p93_reached, 'g^', markersize=11)
p2 = plt.plot(ind, p60_reached, 'bo', markersize=11)
p3 = plt.plot(ind, w_pers_reached, 'ro', markersize=11)
p4 = plt.plot(ind, epic_reached, 'r^', markersize=11)

#plt.plot(t, t, 'r--')
#plt.plot(t, t**2, 'bs', t, t**3, 'g^')
plt.grid()
plt.yticks(np.arange(0, 1.1, 0.1))
#plt.ylim((0.0,1.0))

plt.legend((p1[0], p2[0], p3[0], p4[0]), (r'$P = 0.93$', r'$P = 0.6$', 'w-p-Persistence', 'EPIC'), 
  	loc='upper center', bbox_to_anchor=(0.465, 1.15), fancybox=True, shadow=True, ncol=5)


plt.ylabel('Vehicles (%)')
plt.xlabel(r'avg. degree $\delta$')


plt.title('')
plt.xticks(ind, ('11.6', '24.8', '35.9', '43.8'))

plt.gcf().subplots_adjust(bottom=0.15, left=0.15)

if SAVE_IMG:
    plt.savefig('grafici/top_car/related-w-comparison-reached.png', dpi=300)
else:
    plt.show()


plt.clf()


p1 = plt.plot(ind, p93_frw, 'g^', markersize=11)
p2 = plt.plot(ind, p60_frw, 'bo', markersize=11)
p3 = plt.plot(ind, w_pers_frw, 'ro', markersize=11)
p4 = plt.plot(ind, epic_frw, 'r^', markersize=11)

#plt.plot(t, t, 'r--')
#plt.plot(t, t**2, 'bs', t, t**3, 'g^')
plt.grid()
plt.yticks(np.arange(0, 1.1, 0.1))
#plt.ylim((0.0,1.0))

plt.legend((p1[0], p2[0], p3[0], p4[0]), (r'$P = 0.93$', r'$P = 0.6$', 'w-p-Persistence', 'EPIC'), 
  	loc='upper center', bbox_to_anchor=(0.465, 1.15), fancybox=True, shadow=True, ncol=5)


plt.ylabel('Vehicles (%)')
plt.xlabel(r'avg. degree $\delta$')


plt.title('')
plt.xticks(ind, ('11.6', '24.8', '35.9', '43.8'))

plt.gcf().subplots_adjust(bottom=0.15, left=0.15)

if SAVE_IMG:
    plt.savefig('grafici/top_car/related-w-comparison-frw.png', dpi=300)
else:
    plt.show()
