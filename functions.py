import math 
import matplotlib 
import matplotlib.pyplot as plt 
import numpy as np
from PIL import Image
from numpy import *
import os
from shapely.geometry import Polygon
import numba
from numba import jit

import logging;
logger = logging.getLogger("numba");
logger.setLevel(logging.ERROR)

def area(i,j,xv,yv):
    '''the area of the i th, j th polygon'''
    x=[xv[i,j],xv[i+1,j],xv[i+1,j+1],xv[i,j+1]]
    y=[yv[i,j],yv[i+1,j],yv[i+1,j+1],yv[i,j+1]]
    shape = Polygon(zip(x, y))
    return abs(shape.area)


#cost function
@jit
def cost(a,b):
    if a.shape != b.shape:
        return  'the inputs do not have the same dimensions'
    else: 
        c = a-b
        return np.sum(np.multiply(c,c))

@jit
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

#solve poisson
@jit
def solve_poisson(phi,loss,iteration):
    for i in range(0,iteration):
        it = phi
        for i in range(0,phi.shape[0]):
            for j in range(0,phi.shape[1]):
                delta = f(phi,i-1,j) + f(phi,i+1,j) + f(phi,i,j-1) + f(phi,i,j+1) - 4*f(phi,i,j) + loss[i,j]
                delta = delta/4*1.94    #1.94 is overcorrection factor
                #print(delta)
                it[i,j] += delta
    return it