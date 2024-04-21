import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm # Color maps
from projFuncs import *



t = np.linspace(0,0.9,num=200)
Z = np.zeros(t.shape)

r = integrate_EOM()
ucart = sph2cart(r[1],r[2],r[3],r[4],r[5],r[6])
print(r[1])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('equal', adjustable='box')
# ax.add_patch(plt.Circle((0, 0), 6, color='black')) # Circle in 2d
ax.plot(ucart[0],ucart[1],ucart[2], 'b')

# draw sphere
Radius = 6
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = Radius*np.cos(u)*np.sin(v)
y = Radius*np.sin(u)*np.sin(v)
z = Radius*np.cos(v)
ax.plot_wireframe(x, y, z, color="r")

#fig2 = plt.figure()
#ax2 = fig2.add_subplot(111)
#ax2.plot(r[0],np.abs((-(1/(r[0]-1)))-r[1]), color='g')
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(50*t,50*t-(0.5*9.8*t**2),Z, color='r')
# ax.plot(r[1],r[2],r[3], color='b')

plt.show()