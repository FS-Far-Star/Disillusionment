#-------------------------Importing----------------------------------------------------------
import imp
import math 
import matplotlib 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from PIL import Image
import os
import pandas as pd 
import pyvista as pv
import warnings
warnings.filterwarnings('ignore')

#clear eveyrthing
clear = lambda: os.system('cls')
clear()

#-------------------------User input----------------------------------------------------------
name_of_file = 'images/cat_real.png'
#https://www.img2go.com/compress-image
#image resize website

# Real world parameters
height = 100    #mm, acrylic block height
width = 100    #mm, acrylic block width
thickness = 3   #mm, acrylic block thickness

# Solving parameters
poisson_requirement = 1000   #usually enough to converge
sigma = 1.94                 #over-relaxation factor
morph_grid_requirement = 200 #usually 100 is enough, depends on size though
height_requirement = 3       #

# Physics
n1 = 1          # refractive indice of air   
eta = 1.48899    # refractive indice of acrylic block

#-------------------------Basic operations----------------------------------------------------------
if 'real' in name_of_file:
    testing = False
else:
    testing = True
# This system is in place so that data for the large file can be stored and untouched, while testing can be done with smaller files

'''read image'''
img = Image.open(name_of_file).convert('L') #read image, convert to greyscale
np_img = np.array(img)
# np_img = np.fliplr(np.rot90(np_img, 2))  #correctly orient photo so that the result is readable
    # Actually, you shouldn't mess with the photo at all

'''Calculate spacing'''
spacing = width/np_img.shape[0]   
#for the sake of simplicity, the image used is a square, so the spacings are equal

'''Plotting Coordinate system'''
x,y = np.linspace(0,width-spacing,np_img.shape[0]), np.linspace(0,height-spacing,np_img.shape[1])
a,b = np.meshgrid(x,y)
x,y = np.linspace(0,width,np_img.shape[0]+1), np.linspace(0,height,np_img.shape[1]+1)
c,d = np.meshgrid(x,y)

'''Calculate total area'''
A_t = height*width  #total_area

'''Brightness calculation'''
total_brightness = np.sum(np_img)           
brightness_comp = np_img/total_brightness
# Normalized brightness composition