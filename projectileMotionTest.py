import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm # Color maps
from projFuncs import *



t = np.linspace(0,0.9,num=200)
Z = np.zeros(t.shape)

r = integrate_EOM()
print(r[0])

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(t,-(1/(t-1)), color='r')
ax.plot(r[0],r[1], 'bo')

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.plot(r[0],np.abs((-(1/(r[0]-1)))-r[1]), color='g')
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(50*t,50*t-(0.5*9.8*t**2),Z, color='r')
# ax.plot(r[1],r[2],r[3], color='b')

plt.show()