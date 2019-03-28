import numpy as np
import matplotlib
import matplotlib.pyplot as plt


plt.rcParams.update({'font.size': 18.3})
plt.rc('legend', fontsize=13)
plt.rc('xtick', labelsize=13.5)
plt.rc('ytick', labelsize=11.5)

# HERE I am considering forw recv depending on rmin in luxemurg, 1000 and 50

N = 6


means_frw_low_dens = np.array([73.05174563591022, 55.531483790523666, 40.39900249376558, 27.771197007481287, 16.683291770573568, 10.11533665835411]) /100
means_recv_low_dens = np.array([96.52431421446393, 98.25748129675812, 91.67082294264337, 80.20573566084788, 64.50124688279301, 45.84632169576061])*0.98/100 - means_frw_low_dens 

means_frw_high_dens = np.array([95.57512468827926, 86.88591022443896, 75.12312967581047, 54.59943890274313, 40.985037406483784, 33.07824189526184, ]) /100
means_recv_high_dens = np.array([98.38528678304236, 95.80268079800486, 95.75592269326678, 95.80268079800499, 93.55049875311721, 87.05423940149629, ])/100 - means_frw_high_dens



ind = np.arange(N)    # the x locations for the groups
width = 0.21       # the width of the bars: can also be len(x) sequence

#fig, ax = plt.subplots()
fig = plt.figure()
ax = plt.subplot(111)

gap = 0.075

scale = 0.5
plt.figure(figsize=(15*scale, 10*scale))

p1 = plt.bar(ind, means_frw_high_dens, width, color='b', edgecolor='k')
p2 = plt.bar(ind, means_recv_high_dens, width,
             bottom=means_frw_high_dens, color='#ffa500', edgecolor='k')


p3 = plt.bar(ind+width+gap, means_frw_low_dens, width, color='b', edgecolor='k')
p4 = plt.bar(ind+width+gap, means_recv_low_dens, width,
             bottom=means_frw_low_dens, color='#cc6e00', edgecolor='k')



#plt.text(2.4, 0.9,'drop_rate = 0.03',{'size':11})

# Shrink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
#ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
  #        fancybox=True, shadow=True, ncol=5)



plt.ylabel('Nodes (%)')
plt.xlabel(r'$R_{min}$ (m)')
plt.title('')
plt.xticks(ind+width/2+gap/2, ('50', '100', '150', '200', '250', '300')) 
plt.yticks(np.arange(0, 1.1, 0.1))
#plt.legend((p3[0], p2[0], p6[0], p4[0]), ('Relayers', 'Reached', r'Probabilistic $P=\widehat{P}$', r'Probabilistic $P=0.96$'), 
#	loc='upper center', bbox_to_anchor=(0.5, -0.08),
#    fancybox=True, shadow=True, ncol=5)
plt.legend((p1[0], p2[0], p4[0]), ('Relay', 'EPIC high density', 'EPIC low density'), loc='lower center', fancybox=True)


plt.gcf().subplots_adjust(bottom=0.15, left=0.15)
#plt.show()
plt.savefig('grafici/top_car/rmin_comparison.png', dpi=300)