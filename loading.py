import math 
import matplotlib 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from PIL import Image
from numpy import *
from shapely.geometry import Polygon
from functions import *
import pandas as pd 

import warnings
warnings.filterwarnings('ignore')  

height = 0.1    #meter, acrylic block height
width = 0.1    #meter, acrylic block width

# phi = np.load('phi.npy')
# xv = np.load('xv.npy')
# yv = np.load('yv.npy')
xv = np.array(pd.read_csv('xv.csv',header=None))
yv = np.array(pd.read_csv('yv.csv',header=None))
phi = np.array(pd.read_csv('phi.csv',header=None))

x = np.linspace(0,width,phi.shape[0])
y = np.linspace(0,height,phi.shape[1])
a,b = np.meshgrid(x, y)

plt.plot(xv[1:-1:,1:-1],yv[1:-1:,1:-1])
ax = plt.gca() 
ax.set_aspect(1)
plt.show()