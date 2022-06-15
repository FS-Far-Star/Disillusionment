import math 
import matplotlib 
import matplotlib.pyplot as plt 
import numpy as np
from PIL import Image
from numpy import *
import os

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
#print(np_img.shape)

'''Operations'''
total_brightness = sum(np_img)
brightness_percent = np.zeros((np_img.shape[0],np_img.shape[1]))

for i in range(0,np_img.shape[0]):
    for j in range(0,np_img.shape[1]):
        brightness_percent[i,j] = np_img[i,j]/total_brightness

# ?????????????????????/

#initialize grid
grid = np.zeros((np_img.shape[0],np_img.shape[1]))
cell_num = grid.shape[0]*grid.shape[1]
height = 0.1    #meter
width = 0.1    #meter
A_t = height * width 
grid = grid + A_t/cell_num  #uniform grid

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

loss = grid - brightness_percent
grad = np.array(np.gradient(loss,0.1/brightness_percent.shape[0]))
print(grad.shape)

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
