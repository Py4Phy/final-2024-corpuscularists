import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm # Color maps
from projFuncs import *
from processImg import *

### Using geometrized units; c=G=1.

t_max = 57
defaultTimeStep = 1e-3
MaxCount = 10000
R = 1 # schwarzchild radius
pixel_length = 1
z1 = -1000 # location of where we observe the final image
z2 = 1000 # location of the initial image. Keep it a positive number and the final image at a negative location for later parts of this program to work.

# set image position(s)
initialImage = imageTakeInner('Epic_Redpilled_Beckstein.png')
finalImage = np.zeros(initialImage.shape())
y_size, x_size, z_size = initialImage.shape()
y_positions = np.arange(0, y_size, 1)
x_positions = np.arange(0, x_size, 1)
y_positions = pixel_length*(y_positions - y_size/2)
x_positions = pixel_length*(x_positions - x_size/2)
y_center = pixel_length*y_size/2
x_center = pixel_length*x_size/2

for i in range(y_size):
    for j in range(x_size):
        x = x_positions[j]
        y = y_positions[i]
        z = z1
        vx = 0
        vy = 0
        vz = -1
        r, theta, phi, vr, vtheta, vphi = cart2sph(x,y,z,vx,vy,vz)
        u = integrate_EOM2(np.array([r,theta,phi]), np.array([vr,vtheta,vphi]), t_max, MaxCount, R, z2, defaultTimeStep)
        U1 = sph2cart(u[1:,-2]) # penultimate ray positions and velocities
        U2 = sph2cart(u[1:,-1]) # ultimate ray positions and velocities
        if ((U2[2] - z2) >= 0):
            k,l = findPixel(y_center, x_center, z2, pixel_length, U1[:3], U1[3:6])
            finalImage[i,j,:] = initialImage[k,l,:]