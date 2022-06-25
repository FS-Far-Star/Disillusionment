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
img = Image.open('cat.png').convert('L')
# img.save('greyscale.png')
np_img = np.array(img)
np_img = np.rot90(np_img, 2)
np_img = np.fliplr(np_img)
# print(np_img)

# Array back to image
#Image.fromarray(np_img).show()

'''initialize system'''
# Real world parameters
height = 0.1    #meter, acrylic block height
width = 0.1    #meter, acrylic block width
A_t = height*width  #total_area
spacing_x = height/np_img.shape[0]
spacing_y = height/np_img.shape[0]
#print(spacing)
# Coordinate system
x = np.linspace(0,width,np_img.shape[0]+1)
y = np.linspace(0,height,np_img.shape[1]+1)
xv, yv = np.meshgrid(x, y)  
# print(xv[0,1],xv[0,2])
# print(yv[0,1],yv[2,1])

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
brightness_comp = np_img/total_brightness
np.save('brightness',brightness_comp)

loss = calculate_loss(area_grid,brightness_comp)

'''solve poisson'''
data = []
step = []
limit = 66
for calculation in range(1,limit+1):
    '''solve poisson'''
    guess = np.ones((np_img.shape[0],np_img.shape[1]))
    phi = solve_poisson(guess,loss,1000)
    phi[0,:],phi[:,0],phi[-1,:],phi[:,-1] = phi[1,:],phi[:,1],phi[-2,:],phi[:,-2]
    # colormap
    # plt1 = plt.pcolormesh(a,b,phi)1

    # 3D height map
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot_surface(a,b, phi)
    # plt.title('phi as 3d height map')
    # plt.show()

    '''morph grid'''
    grad = calc_grad(phi,spacing_x,spacing_y)
    # print(grad)
    step_size = find_step_size(xv,yv,grad)
    print(step_size)
    delta_x = grad[0]*step_size
    delta_y = grad[1]*step_size
    xv[1:-1,1:-1] += delta_x[1:,1:]
    yv[1:-1,1:-1] += delta_y[1:,1:]

    # plot points
    # if calculation%10 == 0:
    # #     plt.plot(xv,yv)
    # #     ax = plt.gca() 
    # #     ax.set_aspect(1)
    # #     plt.show()
    
    # Plot vector field
    #plt.quiver(a[0:-1:3,0:-1:3],b[0:-1:3,0:-1:3],delta_x[0:-1:3,0:-1:3],delta_y[0:-1:3,0:-1:3])
    # ax = plt.gca() 
    # ax.set_aspect(1)
    # plt.quiver(a,b,delta_x,delta_y)
    # plt.show()

    #3D height map
        # fig1 = plt.figure()
        # ax = fig1.add_subplot(111, projection='3d')
        # ax.plot_surface(a,b,phi)
        #ax.plot_surface(a[1:-1,1:-1],b[1:-1,1:-1], phi[1:-1,1:-1])
        # plt.title('phi as 3d height map of generation {}'.format(calculation))
        #plt.show()

        # np.save('phi{}'.format(calculation),phi)
        # np.save('xv{}'.format(calculation),xv)
        # np.save('yv{}'.format(calculation),yv)

    #check
    for i in range(0,xv.shape[0]-1):
        for j in range(0,yv.shape[1]-1):
            if xv[i,j] > xv[i,j+1]:
                xv[i,j] = xv[i,j+1]
            if yv[i,j] > yv[i+1,j]:
                yv[i,j] = yv[i+1,j]

    area_grid = area_grid_update(xv,yv)
    area_grid = area_grid/A_t
    print('generation',calculation)
    loss = calculate_loss(area_grid,brightness_comp)
    data.append((calculation,np.sum(np.multiply(loss,loss))))
    step.append((calculation,step_size))
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
ax.plot_surface(a,b, phi)
#ax.plot_surface(a[1:-1,1:-1],b[1:-1,1:-1], phi[1:-1,1:-1])
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
plt.plot(np.transpose(xv),np.transpose(yv))
# plt.plot(xv[1:-2,1:-2],yv[1:-2,1:-2])
# plt.plot(np.transpose(xv)[1:-2,1:-2],np.transpose(yv)[1:-2,1:-2])
ax = plt.gca() 
ax.set_aspect(1)

fig3 = plt.figure()
plt.plot(*zip(*step))
plt.show()



