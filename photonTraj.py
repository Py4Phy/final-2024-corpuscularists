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
initialImage = imageTakeInner('small_test_image.png')
finalImage = np.zeros(initialImage.shape)
print(finalImage.shape)
y_size, z_size, x_size = initialImage.shape
y_positions = np.arange(0, y_size, 1)
z_positions = np.arange(0, z_size, 1)
y_positions = pixel_length*(y_positions - y_size/2)
z_positions = pixel_length*(z_positions - z_size/2)
y_center = pixel_length*y_size/2
z_center = pixel_length*z_size/2

for i in range(y_size):
    for j in range(z_size):
        z = z_positions[j]
        y = y_positions[i]
        x = x1
        vx = 1
        vy = 0
        vz = 0
        u = integrate_EOM(np.array([x,y,z]), np.array([vx,vy,vz]))
        Upu = u[1:][-2] # penultimate
        Uu = u[1:][-1] # ultimate
        if ((Uu[0][0] - x2) >= 0):
            k,l = findPixel(y_center, z_center, x2, pixel_length, Upu[:3][0], Upu[3:][0])
            finalImage[i][j][:] = initialImage[k][l][:]

outputImage = Im.fromarray(finalImage[0][0][:3])
Im.show()
# Im.save('Lensed_Epic_Redpilled_Beckstein.png')