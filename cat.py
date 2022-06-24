import math 
import matplotlib 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from PIL import Image
from numpy import *
import os
from shapely.geometry import Polygon
from functions import *
from numba import jit
import pandas as pd 

import warnings
warnings.filterwarnings('ignore')

#clear eveyrthing
clear = lambda: os.system('cls')
clear()

# Read and show image
# A = plt.imread("download.png",'png')
# plt.imshow(A); 
# plt.show()

# Read image, convert to greyscale, save as greyscale.png, convert to array
img = Image.open('download1.png').convert('L')
img.save('greyscale.png')
np_img = np.array(img)
# np_img = np.rot90(np_img, 2)
# np_img = np.fliplr(np_img)
# print(np_img)

# Array back to image
#Image.fromarray(np_img).show()

'''initialize system'''
# Real world parameters
height = 0.1    #meter, acrylic block height
width = 0.1    #meter, acrylic block width
A_t = height*width  #total_area
spacing = height/np_img.shape[0]
#print(spacing)
# Coordinate system
x = np.linspace(0,width,np_img.shape[0]+1)
y = np.linspace(0,height,np_img.shape[1]+1)
xv, yv = np.meshgrid(x, y)  

# Plotting stuff------------------
x = np.linspace(0,width,np_img.shape[0])
y = np.linspace(0,height,np_img.shape[1])
a,b = np.meshgrid(x, y)
#--------------------------------


area_grid = np.zeros((np_img.shape[0],np_img.shape[1]))
for i in range(0,np_img.shape[0]):
    for j in range(0,np_img.shape[1]):
        area_grid[i,j] = area(i,j,xv,yv)
area_grid = area_grid/A_t
#print(np.sum(area_grid))
#print(area_grid)

'''Image Processing'''
total_brightness = np.sum(np_img)
brightness_comp = np.array(img)/total_brightness
np.save('brightness',brightness_comp)

loss = calculate_loss(area_grid,brightness_comp)

'''solve poisson'''
data =[]
limit = 50
for calculation in range(1,limit+1):
    '''solve poisson'''
    phi = solve_poisson(area_grid,loss,1000)
    phi[0,:],phi[:,0],phi[-1,:],phi[:,-1] = phi[1,:],phi[:,1],phi[-2,:],phi[:,-2]
    # colormap
    # plt1 = plt.pcolormesh(a,b,phi)

    # 3D height map
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot_surface(a,b, phi)
    # plt.title('phi as 3d height map')
    # plt.show()

    '''morph grid'''
    grad = np.gradient(phi,spacing)
    delta_x = grad[0]*spacing/10
    delta_y = grad[1]*spacing/10
    # Plot vector field
    #plt.quiver(a[0:-1:10,0:-1:10],b[0:-1:10,0:-1:10],delta_x[0:-1:10,0:-1:10],delta_y[0:-1:10,0:-1:10])
    #plt.quiver(a,b,delta_x,delta_y)

    # plot points
    if calculation%50 == 0:
    #     plt.plot(xv,yv)
    #     ax = plt.gca() 
    #     ax.set_aspect(1)
    #     plt.show()

    #3D height map
        fig1 = plt.figure()
        ax = fig1.add_subplot(111, projection='3d')
        ax.plot_surface(a,b,phi)
        #ax.plot_surface(a[1:-1,1:-1],b[1:-1,1:-1], phi[1:-1,1:-1])
        plt.title('phi as 3d height map of generation {}'.format(calculation))
        #plt.show()

        # np.save('phi{}'.format(calculation),phi)
        # np.save('xv{}'.format(calculation),xv)
        # np.save('yv{}'.format(calculation),yv)

    # morph grid
    xv[1:-1,1:-1] -= delta_x[1:,1:]
    yv[1:-1,1:-1] -= delta_y[1:,1:]

    area_grid = area_grid_update(xv,yv)
    area_grid = area_grid
    print('generation',calculation)
    loss = calculate_loss(area_grid,brightness_comp)
    data.append((calculation,(cost(area_grid,brightness_comp))))
#----------------- end of iterations----------------

#save data
np.save('xv',xv)
np.save('yv',yv)
np.save('phi',phi)
# pd.DataFrame(phi).to_csv("phi.csv",header=None, index=None)
# pd.DataFrame(xv).to_csv("xv.csv",header=None, index=None)
# pd.DataFrame(yv).to_csv("yv.csv",header=None, index=None)

# 3D height map
phi = np.load('phi.npy')
fig1 = plt.figure()
ax = fig1.add_subplot(111, projection='3d')
#ax.plot_surface(a,b, phi)
ax.plot_surface(a[1:-1,1:-1],b[1:-1,1:-1], phi[1:-1,1:-1])
#ax.plot_surface(a[2:-2,2:-2],b[2:-2,2:-2], phi[2:-2,2:-2])
plt.title('phi as 3d height map')

# fig5 = plt.figure()
# ax = fig5.add_subplot(111, projection='3d')
# #ax.plot_surface(a,b, phi)
# ax.plot_surface(a,b,phi)
# #ax.plot_surface(a[2:-2,2:-2],b[2:-2,2:-2], phi[2:-2,2:-2])
# plt.title('phi as 3d height map, with edges')

# grid
fig2 = plt.figure()
plt.plot(xv,yv)
plt.plot(xv[0:-1:10,0:-1:10],yv[0:-1:10,0:-1:10])
ax = plt.gca() 
ax.set_aspect(1)

fig3 = plt.figure()
plt.plot(*zip(*data))
plt.show()



