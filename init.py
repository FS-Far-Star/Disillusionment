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

name_of_file = 'images/cat_50.png'
#https://www.img2go.com/compress-image
#image resize website

# Real world parameters
height = 100    #mm, acrylic block height
width = 100    #mm, acrylic block width
thickness = 5   #mm, acrylic block thickness

# Solving parameters
poisson_requirement = 1000   #usually enough to converge
sigma = 1.94                 #over-relaxation factor
morph_grid_requirement = 160 #usually 100 is enough
height_requirement = 3       #

# Physics
n1 = 1          # refractive indice of air   
eta = 1.48899    # refractive indice of acrylic block