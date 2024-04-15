import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm # Color maps
from projFuncs import *
from processImg import *

### Using geometrized units; c=G=1.

pixel_length = 1
z_position1 = 1000 # location of where we observe the final image
z_position2 = -1000 # location of the initial image

# set image position(s)
initialImage = imageTakeInner('Epic_Redpilled_Beckstein.png')
y_size, x_size, z_size = initialImage.shape()
y_positions, x_positions = np.meshgrid(y_size, x_size)
y_positions = pixel_length*(y_positions - y_size/2)
x_positions = pixel_length*(x_positions - x_size/2)
y_center = pixel_length*y_size/2
x_center = pixel_length*x_size/2