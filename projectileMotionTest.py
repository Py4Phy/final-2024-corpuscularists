import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm # Color maps
from projFuncs import *



t = np.linspace(0,10.2,num=200)
Z = np.zeros(t.shape)

r = integrate_EOM()
print(r[0])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(50*t,50*t-(0.5*9.8*t**2),Z, color='r')
ax.plot(r[1],r[2],r[3], color='b')
plt.show()