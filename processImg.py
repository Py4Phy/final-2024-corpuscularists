# takes in the initial image and prepares it for the lensing simulation.
# saves an array of the RGB values to a file

import numpy as np
import PIL
from PIL import Image as Im

# choose the image to use and the file to save to HERE
image_file = 'stock-photo-young-attractive-dangerous-woman-aiming-at-gold-fish-55445056.jpg' # input file
array_file = 'usable.npy' # 0utput file with the format .npy

image = Im.open(image_file)
image = np.array(image)
np.save(array_file, image)

def imageTakeInner():
    image_file
    image = Im.open(image_file)
    image = np.array(image)
    return image