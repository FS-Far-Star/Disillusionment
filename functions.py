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
    '''calculate the area of the i th, j th polygon, assume convex?'''
    x=[xv[i,j],xv[i+1,j],xv[i+1,j+1],xv[i,j+1]]
    y=[yv[i,j],yv[i+1,j],yv[i+1,j+1],yv[i,j+1]]
    shape = Polygon(zip(x, y))
    return abs(shape.area)

@jit    #cost function
def cost(a,b):
    if a.shape != b.shape:
        return  'the inputs do not have the same dimensions'
    else: 
        c = a-b
        return np.sum(np.multiply(c,c))

@jit    #built-in neunmann boundary condition
def f(phi,i,j): 
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

@jit    #solve poisson
def solve_poisson(phi,loss,iteration):
    for iteration in range(0,iteration):
        it = phi
        for i in range(0,phi.shape[0]):
            for j in range(0,phi.shape[1]):
                delta = f(phi,i-1,j) + f(phi,i+1,j) + f(phi,i,j-1) + f(phi,i,j+1) - 4*f(phi,i,j) + loss[i,j]
                delta = delta/4*1.94    #1.94 is overcorrection factor
                #print(delta)
                it[i,j] += delta
        phi = it
    return phi

@jit    # update area of every grid
def area_grid_update(xv,yv):
    area_grid = np.zeros((xv.shape[0]-1,xv.shape[1]-1))
    for i in range(0,xv.shape[0]-1):
        for j in range(0,xv.shape[1]-1):
            area_grid[i,j] = area(i,j,xv,yv)
    return area_grid

def calculate_loss(area_grid,brightness_comp):
    loss = area_grid - brightness_comp
    loss[0,:] = 0
    loss[-1,:] = 0
    loss[:,0] = 0
    loss[:,-1] = 0
    return loss