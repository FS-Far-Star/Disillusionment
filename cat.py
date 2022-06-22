import imp
import math 
import matplotlib 
import matplotlib.pyplot as plt 
import numpy as np
from PIL import Image
from numpy import *
import os
from shapely.geometry import Polygon
from functions import *

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
np_img = np.rot90(np_img, 2)
np_img = np.fliplr(np_img)
#print(np_img)

# Array back to image
#Image.fromarray(np_img).show()

'''initialize coordinate system'''
height = 0.1    #meter, acrylic block height
width = 0.1    #meter, acrylic block width
A_t = height*width  #total_area
x = np.linspace(0,width,np_img.shape[0]+1)
y = np.linspace(0,height,np_img.shape[1]+1)
#print(len(x))
xv, yv = np.meshgrid(x, y)  
# print(xv)
# print(yv)

area_grid = np.zeros((np_img.shape[0],np_img.shape[1]))
for i in range(0,np_img.shape[0]):
    for j in range(0,np_img.shape[1]):
        area_grid[i,j] = area(i,j,xv,yv)
area_grid = area_grid/A_t
#print(area_grid)

'''Image Processing'''
total_brightness = np.sum(np_img)
#print(total_brightness)
brightness_comp = np.array(img)/total_brightness
#print(brightness_comp)

# print(cost(area_grid,brightness_comp))

loss = area_grid - brightness_comp
# grad = np.array(np.gradient(loss,width/brightness_comp.shape[0]))

'''solve poisson'''
phi = area_grid     #initial guess
print('intial cost:',cost(area_grid,brightness_comp)) 
print(np.amax(loss))
#print(phi)

#plotting stuff------------------
x = np.linspace(0,width,np_img.shape[0])
y = np.linspace(0,height,np_img.shape[1])
a,b = np.meshgrid(x, y)
#--------------------------------
for calculation in range(1,4):
    '''solve poisson'''
    for iteration in range(0,100):
        it = phi
        for i in range(0,phi.shape[0]-1):
            for j in range(0,phi.shape[1]-1):
                delta = f(phi,i-1,j) + f(phi,i+1,j) + f(phi,i,j-1) + f(phi,i,j+1) - 4*f(phi,i,j) + loss[i,j]
                delta = delta/4*1.94    #1.94 is overcorrection factor
                #print(delta)
                it[i,j] += delta
        phi = it
        # print(phi)
        # print('-------------------')
    plt1 = plt.pcolormesh(a,b,phi)

    '''morph grid'''
    grad = np.gradient(phi)
    delta_x = -grad[0]
    delta_y = -grad[1]
    # print(grad[0].shape)

    for i in range(0,np_img.shape[0]):
        for j in range(0,np_img.shape[1]):
            xv[i,j] += delta_x[i,j]
            yv[i,j] += delta_y[i,j]

    for i in range(0,np_img.shape[0]):
        for j in range(0,np_img.shape[1]):
            area_grid[i,j] = area(i,j,xv,yv)
    print('cost of generation',calculation,':',cost(area_grid,brightness_comp)) 
    print(np.amax(loss))
    loss = area_grid - brightness_comp
    # plt.pcolormesh(a,b,phi)
    # plt.show()




