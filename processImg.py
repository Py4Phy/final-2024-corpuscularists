# takes in the initial image and prepares it for the lensing simulation.
# saves an array of the RGB values to a file

import numpy as np
import PIL
from PIL import Image as Im

# method to be used by other files in case we don't want to run this individually
def imageTakeInner(image_file):
    image = Im.open(image_file)
    image = np.array(image)
    return image

# method to find where the ray passes through an image
def findPixel(y_center, z_center, x_position, pixel_length, ri, v):
    xi, yi, zi = ri # initial positions, should input the final positions BEFORE the ray passes through the image
    vx, vy, vz = v # velocities from the same time as the initial position
    X = x_position - xi
    zf = zi + X*(vz/vx)
    yf = yi + X*(vy/vx)
    j = (zf + z_center)/pixel_length
    i = (yf + y_center)/pixel_length
    return i, j # y then x indices for the pixel

# choose the image to use and the file to save to HERE
image_file = 'stock-photo-young-attractive-dangerous-woman-aiming-at-gold-fish-55445056.jpg' # input file
array_file = 'usable.npy' # 0utput file with the format .npy

image = Im.open(image_file)
image = np.array(image)
np.save(array_file, image)