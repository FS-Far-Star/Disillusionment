from bisect import bisect_right
import math 
import matplotlib 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from PIL import Image
from numpy import *
from shapely.geometry import Polygon
from functions import *
import pandas as pd 

import warnings
warnings.filterwarnings('ignore')  

height = 0.1    #meter, acrylic block height
width = 0.1    #meter, acrylic block width
A_t = height*width 

phi = np.load('phi.npy')
xv = np.load('xv.npy')
yv = np.load('yv.npy')
brightness_comp =np.load('brightness.npy')
# pd.DataFrame(phi).to_csv("phi.csv",header=None, index=None)
# pd.DataFrame(xv).to_csv("xv.csv",header=None, index=None)
# pd.DataFrame(yv).to_csv("yv.csv",header=None, index=None)
# xv = np.array(pd.read_csv('xv.csv',header=None))
# yv = np.array(pd.read_csv('yv.csv',header=None))
# phi = np.array(pd.read_csv('phi.csv',header=None))

x = np.linspace(0,width,phi.shape[0])
y = np.linspace(0,height,phi.shape[1])
a,b = np.meshgrid(x, y)

area_grid = np.zeros((phi.shape[0],phi.shape[1]))
for i in range(0,phi.shape[0]):
    for j in range(0,phi.shape[1]):
        area_grid[i,j] = area(i,j,xv,yv)
area_grid = area_grid/A_t
loss = calculate_loss(area_grid,brightness_comp)
# phi = solve_poisson(area_grid,loss,1000)


# 3D height map
fig1 = plt.figure()
ax = fig1.add_subplot(111, projection='3d')
#ax.plot_surface(a,b, phi)
ax.plot_surface(a[1:-1,1:-1],b[1:-1,1:-1], phi[1:-1,1:-1])
#ax.plot_surface(a[2:-2,2:-2],b[2:-2,2:-2], phi[2:-2,2:-2])
plt.title('phi as 3d height map')

#grid
fig2 = plt.figure()
#plt.plot(xv,yv)
plt.plot(xv[1:-2,1:-2],yv[1:-2,1:-2])
ax = plt.gca() 
ax.set_aspect(1)

# fig3 = plt.figure()
# ax = plt.gca() 
# ax.set_aspect(1)
plt.pcolormesh(a,b,loss)

plt.show()