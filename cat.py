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
# A = plt.imread("download.jpg",'jpg')
# plt.imshow(A); 
# plt.show()

# Read image, convert to greyscale, save as greyscale.png, convert to array
img = Image.open('download.jpg').convert('L')
img.save('greyscale.png')
np_img = np.array(img)
#print(np_img.shape)

'''Operations'''
total_brightness = sum(np_img)
average_brightness = total_brightness/(np_img.shape[0]*np_img.shape[1])
#print(average_brightness)

for i in range(0,np_img.shape[0]):
    for j in range(0,np_img.shape[1]):
        np_img[i,j] = np_img[i,j] - average_brightness

# Array back to image
Image.fromarray(np_img).show()



