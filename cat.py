import math 
import matplotlib 
import matplotlib.pyplot as plt 
import numpy as np
from PIL import Image
from numpy import *
import os
from shapely.geometry import Polygon

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
#print(np_img)

'''initialize coordinate system'''
height = 0.1    #meter, acrylic block height
width = 0.1    #meter, acrylic block width
A_t = height*width  #total_area
x = np.linspace(0,width,np_img.shape[0]+1)
y = np.linspace(0,height,np_img.shape[1]+1)
#print(len(x))
xv, yv = np.meshgrid(x, y)  
#print(xv)       


def area(i,j):
    '''the area of the i th, j th polygon'''
    x=[xv[i,j],xv[i+1,j],xv[i+1,j+1],xv[i,j+1]]
    y=[yv[i,j],yv[i+1,j],yv[i+1,j+1],yv[i,j+1]]
    shape = Polygon(zip(x, y))
    return shape.area
#print(area(1,1))
area_grid = np.zeros((np_img.shape[0],np_img.shape[1]))
for i in range(0,np_img.shape[0]):
    for j in range(0,np_img.shape[1]):
        area_grid[i,j] = area(i,j)/A_t
#print(area_grid)

'''Image Processing'''
total_brightness = np.sum(np_img)
#print(total_brightness)
brightness_comp = np.array(img)/total_brightness
#print(brightness_comp)

#cost function
def cost(a,b):
    if a.shape != b.shape:
        return  'the inputs do not have the same dimensions'
    else: 
        sum = 0
        for i in range(0,a.shape[0]):
            for j in range(0,a.shape[1]):
                sum += (a[i,j]-b[i,j])**2
        return sum

loss = area_grid - brightness_comp
grad = np.array(np.gradient(loss,width/brightness_comp.shape[0]))
print(cost(area_grid,brightness_comp))



# u = np.zeros((183,276))
# v = np.zeros((183,276))
# for i in range(0,grad.shape[1]):
#     for j in range(0,grad.shape[2]):
#         u = grad[0,i,j]
#         v = grad[1,i,j]
# print(u)
# x,y = np.meshgrid(np.linspace(0,loss.shape[0],1),np.linspace(0,loss.shape[1],1))

# plt.quiver(x,y,u,v)
# plt.show()


# Field Plotting
# x = grid.shape[0]
# y = grid.shape[1]
# direction = math.sqrt(loss)


# Array back to image
#Image.fromarray(loss).show()
