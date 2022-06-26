import imp
import math 
import matplotlib 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from PIL import Image
import os
import pandas as pd 

import warnings
warnings.filterwarnings('ignore')

#clear eveyrthing
clear = lambda: os.system('cls')
clear()

name_of_file = 'images/cat_small.png'
#https://www.img2go.com/compress-image
#image resize website

# Real world parameters
height = 0.1    #meter, acrylic block height
width = 0.1    #meter, acrylic block width
thickness = 0.02   #meter, acrylic block thickness

# Solving parameters
poisson_requirement = 10000   #usually enough to converge
morph_grid_requirement = 200 #usually 100 is enough
height_requirement = 3       #
