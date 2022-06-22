import math 
import matplotlib 
import matplotlib.pyplot as plt 
import numpy as np
from PIL import Image
from numpy import *
import os
from shapely.geometry import Polygon

def area(i,j,xv,yv):
    '''the area of the i th, j th polygon'''
    x=[xv[i,j],xv[i+1,j],xv[i+1,j+1],xv[i,j+1]]
    y=[yv[i,j],yv[i+1,j],yv[i+1,j+1],yv[i,j+1]]
    shape = Polygon(zip(x, y))
    return shape.area


#cost function
def cost(a,b):
    if a.shape != b.shape:
        return  'the inputs do not have the same dimensions'
    else: 
        c = a-b
        return np.sum(np.multiply(c,c))

def f(phi,i,j): #built-in neunmann boundary condition
    if i == -1:
        a = 1
    elif i == phi.shape[0]:
        a = phi.shape[0]-1
    else:
        a = i
    if j == -1:
        b = 1
    elif j == phi.shape[1]:
        b = phi.shape[1]-1
    else:
        b = j
    return(phi[a,b])
