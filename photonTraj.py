import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm # Color maps
from projFuncs import *
from processImg import *
import PIL
from PIL import Image as Im

### Using geometrized units; c=G=1.

pixel_length = 1
x1 = -1000 # location of where we observe the final image
x2 = 1000 # location of the initial image. Keep it a positive number and the final image at a negative location for later parts of this program to work.

# set image position(s)
initialImage = imageTakeInner('Epic_Redpilled_Beckstein.png')
finalImage = np.zeros(initialImage.shape())
y_size, z_size, x_size = initialImage.shape()
y_positions = np.arange(0, y_size, 1)
z_positions = np.arange(0, z_size, 1)
y_positions = pixel_length*(y_positions - y_size/2)
z_positions = pixel_length*(z_positions - z_size/2)
y_center = pixel_length*y_size/2
z_center = pixel_length*z_size/2

for i in range(y_size):
    for j in range(x_size):
        z = z_positions[j]
        y = y_positions[i]
        d = np.sqrt(y**2 + z**2)
        COSPSI = y/d
        SINPSI = z/d
        x = x1
        vx = 1
        vy = 0
        vz = 0
        u = integrate_EOM(np.array([x,d,0]), np.array([vx,vy,vz])) # the arguments are rotated to be in the xy plane
        U = sph2cart(u[1:])
        temporary = COSPSI*U[1] - SINPSI*U[2]
        U[2] = SINPSI*U[1] + COSPSI*U[2]
        U[1] = temporary
        Upu = U[:,-2] # penultimate
        Uu = U[:,-1] # ultimate
        if ((Uu[0] - x2) >= 0):
            k,l = findPixel(y_center, z_center, x2, pixel_length, Upu[:3], Upu[3:])
            finalImage[i,j,:] = initialImage[k,l,:]

outputImage = Im.fromarray(finalImage)
Im.show()
Im.save('Lensed_Epic_Redpilled_Beckstein.png')