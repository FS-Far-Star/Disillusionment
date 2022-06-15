import math 
import matplotlib 
import matplotlib.pyplot as plt 
import numpy as np
from PIL import Image
from numpy import *

# Read and show image
# A = plt.imread("D:\GitHub\Disillusionment\download.jpg",'jpg')
# plt.imshow(A); 
# plt.show()

# Read image, convert to greyscale, save as greyscale.png, convert to array
img = Image.open('D:\GitHub\Disillusionment\download.jpg').convert('L')
img.save('greyscale.png')
np_img = np.array(img)
#print(np_img.shape)

'''Operations'''
for i in range(0,np_img.shape[0]):
    for j in range(0,np_img.shape[1]):
        np_img[i,j] = np_img[i,j] - 100

# Array back to image
Image.fromarray(np_img).show()



