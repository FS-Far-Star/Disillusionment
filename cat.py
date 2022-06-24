import imp
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
img = Image.open('download.png').convert('L')
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
#print(total_brightness)
brightness_comp = np.array(img)/total_brightness
#print(np.sum(brightness_comp))
#print(brightness_comp)

# print(cost(area_grid,brightness_comp))
loss = area_grid - brightness_comp

'''solve poisson'''
phi = area_grid     #initial guess
print('intial cost:',cost(area_grid,brightness_comp)) 
print(np.amax(abs(loss)))

# plt.pcolormesh(a,b,loss)
# plt.show()
data =[]
for calculation in range(1,101):
    '''solve poisson'''
    phi = solve_poisson(phi,loss,200)
    
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
    delta_x = grad[0]*spacing
    delta_y = grad[1]*spacing

    # Plot vector field
    plt.quiver(a[0:-1:10,0:-1:10],b[0:-1:10,0:-1:10],delta_x[0:-1:10,0:-1:10],delta_y[0:-1:10,0:-1:10])
    #plt.quiver(a,b,delta_x,delta_y)
    ax = plt.gca() 
    ax.set_aspect(1)
    # plt.show()
    
    # print(xv.shape)
    # print(delta_x.shape)
    xv[1:-1,1:-1] -= delta_x[1:,1:]
    yv[1:-1,1:-1] -= delta_y[1:,1:]

    #check
    # for i in range(1,np_img.shape[0]):
    #     for j in range(1,np_img.shape[1]):
    #         if xv[i,j] < xv[i-1,j]:
    #             xv[i,j] = xv[i-1,j]
    #         elif xv[i,j] > 0.1:
    #             xv[i,j] = 0.1
    #         if yv[i,j] < yv[i,j-1]:
    #             yv[i,j] = yv[i-1,j]
    #         elif yv[i,j] > 0.1:
    #             yv[i,j] = 0.1
        
    for i in range(0,np_img.shape[0]):
        for j in range(0,np_img.shape[1]):
            area_grid[i,j] = area(i,j,xv,yv)
    # print('cost of generation',calculation,':',cost(area_grid,brightness_comp)) 
    # print(np.amax(abs(loss)))
    print('generation',calculation)
    loss = area_grid - brightness_comp

    data.append((calculation,(cost(area_grid,brightness_comp))))
    # plt.pcolormesh(a,b,loss)
    # plt.show()

# 3D height map
fig1 = plt.figure()
ax = fig1.add_subplot(111, projection='3d')
ax.plot_surface(a,b, phi)
plt.title('phi as 3d height map')

# grid
fig2 = plt.figure()
plt.plot(xv[0:-1:10,0:-1:10],yv[0:-1:10,0:-1:10])
ax = plt.gca() 
ax.set_aspect(1)

fig3 = plt.figure()
plt.plot(*zip(*data))
plt.show()



