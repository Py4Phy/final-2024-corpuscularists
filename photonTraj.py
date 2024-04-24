import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm # Color maps
from projFuncs import *
from processImg import *
from inputVariables import *
import PIL
from PIL import Image as Im
from time import sleep
from tqdm import tqdm
# import asyncio

### Using Planck units; c=G=hbar=kB=1.

pixel_length = 5
x1 = -100 # location of where we observe the final image
x2 = 100 # location of the initial image. Keep it a positive number and the final image at a negative location for later parts of this program to work.

# Set image position(s)
imgName = "Epic_Redpilled_Beckstein"
initialImage = imageTakeInner(imgName+'.png')
finalImage = np.zeros(initialImage.shape, dtype = int)

y_size, z_size, x_size = initialImage.shape
y_positions = np.arange(0, y_size, 1)
z_positions = np.arange(0, z_size, 1)
y_positions = pixel_length*(y_positions - y_size/2)
z_positions = pixel_length*(z_positions - z_size/2)
y_center = pixel_length*y_size/2
z_center = pixel_length*z_size/2

# Set Resulting Image Size. width=y_size and height=z_size for whole image.
width = 100
height = 50

# Box of width by height samples centered at on the (possibly larger) image.
#finalImage = np.zeros([width,height,4], dtype = int).shape

# int(y_size/2)-int(width/2),int(y_size/2)+int(width/2),1
# int(z_size/2)-int(height/2),int(z_size/2)+int(height/2),1

print("Started.")
for i in tqdm(range(int(y_size/2)-int(height/2),int(y_size/2)+int(height/2),1)):
    for j in range(int(z_size/2)-int(width/2),int(z_size/2)+int(width/2),1):
        # print("Y: "+str(i)+"/"+str(y_size)+" Z: "+str(j)+"/"+str(z_size))
        z = z_positions[j]
        y = y_positions[i]
        x = x1
        vx = 1
        vy = 0
        vz = 0
        u = integrate_EOM(np.array([x,y,z]), np.array([vx,vy,vz]),1,np.array([x2,y_size + 1,z_size + 1]))
        Uu = u[1:,-1,0] # ultimate
        if ((Uu[0] - x2) >= 0):
            k,l = findPixel(y_center, z_center, x2, pixel_length, Uu[:3], Uu[3:])
            if ((k > -1) and (k < y_size) and (l > -1) and (l < z_size)):
                finalImage[i,j,:] = initialImage[k,l,:]
print("Finished.")


#plt.style.use('dark_background')
fig,ax = plt.subplots(1)
ax = plt.gca()
ax.set_ylim([int(y_size/2)-int(height/2), int(y_size/2)+int(height/2)])
ax.set_xlim([int(z_size/2)-int(width/2), int(z_size/2)+int(width/2)])
ax.set_aspect('equal')
ax.imshow(finalImage)

print(y_size)
print(z_size)
ax.add_patch(plt.Circle((z_size/2,y_size/2), Rs, color='black'))
ax.add_patch(plt.Circle((z_size/2,y_size/2), 1.5*Rs, color='black', fill=False, linewidth=2.0, linestyle=':'))
ax.add_patch(plt.Circle((z_size/2,y_size/2), 2.598*Rs, color='black', fill=False, linewidth=2.0, linestyle='--'))
plt.savefig("Lensed_"+imgName+".png")