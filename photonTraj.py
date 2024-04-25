import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm # Color maps
from projFuncs import *
from tqdm import tqdm

# First plot. Impact parameter b=L/E. Photon sphere at 3R (dotted line)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.set_aspect('equal', adjustable='box')
ax1.set_xlabel(r'$X$ [M]')
ax1.set_ylabel(r'$Y$ [M]')
ax1.add_patch(plt.Circle((0, 0), Rs, color='red', label="Event Horizion")) # Circle in 2d
ax1.add_patch(plt.Circle((0, 0), 1.5*Rs, color='red', fill=False, linewidth=2.0, linestyle=':', label="Photon Sphere"))
ax1.add_patch(plt.Circle((0, 0), 2.598*Rs, color='red', fill=False, linewidth=2.0, linestyle='--', label="Shadow"))
ax1.legend(loc="upper left")
ax1.axes.set_xlim(left=-100, right=100) 
ax1.axes.set_ylim(bottom=-100, top=100) 

for i in range(-25,30,5):
    r1 = integrate_EOM(np.array([-100, i, 0]))
    ax1.plot(r1[1],r1[2], 'k')

for j in range(-100,-25,5):
    r2 = integrate_EOM(np.array([-100, j, 0]))
    ax1.plot(r2[1],r2[2], 'b')

for k in range(30,100,5):
    r3 = integrate_EOM(np.array([-100, k, 0]))
    ax1.plot(r3[1],r3[2], 'b')

plt.savefig('figures/ImpactParameter.png')
plt.close(fig1)


# Second plot. Orbit trajectories in plane
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.set_aspect('equal', adjustable='box')
ax2.set_xlabel(r'$X$ [M]')
ax2.set_ylabel(r'$Y$ [M]')
ax2.add_patch(plt.Circle((0, 0), Rs, color='red')) # Circle in 2d
Bound2 = 2*Rs+5
ax2.legend(loc="upper left")
ax2.axes.set_xlim(left=-Bound2, right=Bound2) 
ax2.axes.set_ylim(bottom=-Bound2, top=Bound2) 

rOrb1 = integrate_EOM(np.array([0, 2*Rs, 0]),np.array([1, 0, 0], dtype = np.float64),0,np.array([Bound2,Bound2,Bound2]))
ax2.plot(rOrb1[1],rOrb1[2], color='b', label='Escape')

rOrb2 = integrate_EOM(np.array([0, 1.5*Rs, 0]),np.array([1, 0, 0], dtype = np.float64),0,np.array([Bound2,Bound2,Bound2]))
ax2.plot(rOrb2[1],rOrb2[2], color='g', label='Unstable Orbit')

rOrb3 = integrate_EOM(np.array([0, 1.25*Rs, 0]),np.array([1, 0, 0], dtype = np.float64),0,np.array([Bound2,Bound2,Bound2]))
ax2.plot(rOrb3[1],rOrb3[2], color='m', label='Capture')

ax2.add_patch(plt.Circle((0, 0), 1.5*Rs, color='red', fill=False, linewidth=2.0, linestyle=':',zorder=10))
ax2.legend(loc="upper left")

plt.savefig('figures/OrbitTrajectories.png')
plt.close(fig2)

# Figure 3 Plane Solution
fig3 = plt.figure()
ax3 = fig3.add_subplot(111, projection='3d')
Bound3 = 101
ax3.set_aspect('equal', adjustable='box')
ax3.axes.set_xlim3d(left=-Bound3, right=Bound3) 
ax3.axes.set_ylim3d(bottom=-Bound3, top=Bound3) 
ax3.axes.set_zlim3d(bottom=-Bound3, top=Bound3) 
ax3.set_xlabel(r'$X$ [M]')
ax3.set_ylabel(r'$Y$ [M]')
ax3.set_zlabel(r'$Z$ [M]')

# Draw Sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = Rs*np.cos(u)*np.sin(v)
y = Rs*np.sin(u)*np.sin(v)
z = Rs*np.cos(v)
ax3.plot_surface(x, y, z, color="k", alpha = 0.5)

for i in range(-100,100,5):
    rpl = integrate_EOM(np.array([-100, i, i]),np.array([1, 0, 0], dtype = np.float64),0,np.array([Bound3,Bound3,Bound3]))
    ax3.plot(rpl[1],rpl[2],rpl[3], 'b')


plt.savefig('figures/PlanarTrajectories.png')
plt.close(fig3)

#ax = fig.add_subplot(111)
#ax1.axes.set_xlim3d(left=-Bound, right=Bound) 
#ax1.axes.set_ylim3d(bottom=-Bound, top=Bound) 
#ax1.axes.set_zlim3d(bottom=-Bound, top=Bound) 
#ax1.set_xlabel(r'$X$')
#ax1.set_ylabel(r'$Y$')
#ax.set_zlabel(r'$Z$')




        #R = integrate_EOM(np.array([-20, 5*(i-2.5), 5*(j-2.5)]),np.array([1, 0, 0], dtype = np.float64), 1)
        #ax.scatter(R[1],R[2],R[3], color='r', s=4)



'''
r = integrate_EOM(np.array([-10, 10, 10]))
ax.plot(r[1],r[2],r[3], 'b')
R = integrate_EOM(np.array([-10, 10, 10]),np.array([1, 0, 0], dtype = np.float64), 1)
ax.scatter(R[1],R[2],R[3], color='r', s=4)
'''

# draw sphere
#Radius = Rs
#u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
#x = Radius*np.cos(u)*np.sin(v)
#y = Radius*np.sin(u)*np.sin(v)
#z = Radius*np.cos(v)
#ax.plot_surface(x, y, z, color="k", alpha = 0.5)



#fig2 = plt.figure()
#ax2 = fig2.add_subplot(111)
#ax2.plot(r[0],np.abs((-(1/(r[0]-1)))-r[1]), color='g')
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(50*t,50*t-(0.5*9.8*t**2),Z, color='r')
# ax.plot(r[1],r[2],r[3], color='b')

#plt.show()