
import matplotlib.pyplot as plt

# forwarder vs RMIN
rmin = [50, 75, 100, 125, 150, 175, 200, 225, 250]
frw = [602.5, 458.5, 431.3, 343, 333.5, 284, 256.2, 209.3, 146.9]

plt.plot(rmin, frw, 'r--')
plt.show()
