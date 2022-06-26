from init import *
from shapely.geometry import Polygon
import numba
from numba import jit

import logging;
logger = logging.getLogger("numba");
logger.setLevel(logging.ERROR)

@jit
def area(i,j,xv,yv):
    '''calculate the area of the i th, j th polygon, assume convex?'''
    x=[xv[i,j],xv[i+1,j],xv[i+1,j+1],xv[i,j+1]]
    y=[yv[i,j],yv[i+1,j],yv[i+1,j+1],yv[i,j+1]]
    shape = Polygon(zip(x, y))
    return shape.area

# @jit    #cost function
# def cost(a,b):
#     if a.shape != b.shape:
#         return  'the inputs do not have the same dimensions'
#     else: 
#         c = a-b
#         return np.sum(np.multiply(c,c))

@jit    #built-in neunmann boundary condition
def f(phi,i,j): 
    if i == -1:
        a = 1
    elif i == phi.shape[0]:
        a = phi.shape[0]-2
    else:
        a = i
    if j == -1:
        b = 1
    elif j == phi.shape[1]:
        b = phi.shape[1]-2
    else:
        b = j
    return(phi[a,b])

@jit   #the numpy grad is unfortunately too advanced
def calc_grad(phi,spacing_x,spacing_y):
    grad_x = np.zeros((phi.shape[0],phi.shape[1]))
    grad_y = np.zeros((phi.shape[0],phi.shape[1]))
    for i in range(0,phi.shape[0]-1):
        for j in range(0,phi.shape[1]-1):
            grad_x[i,j] = (f(phi,i,j+1)-f(phi,i,j-1))/spacing_x
            grad_y[i,j] = (f(phi,i+1,j)-f(phi,i-1,j))/spacing_y
    grad = [grad_x,grad_y]
    return grad

@jit    #solve poisson with relaxation
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

@jit    #calculate the loss matrix
def calculate_loss(area_grid,brightness_comp):
    loss = area_grid - brightness_comp
    return loss

@jit    #find the maximum allowed step size, then divide by two
def find_step_size(xv,yv,grad):
    min_dt = 100
    for i in range(1,xv.shape[0]-2):
        for j in range(1,xv.shape[1]-2):
            if grad[0][i,j]<0:
                s = (xv[i,j-1] - xv[i,j])/grad[0][i,j]
            if grad[0][i,j]>0:
                s = (xv[i,j+1] - xv[i,j])/grad[0][i,j]
            #print(s)
            min_dt = min(s,min_dt)
    for i in range(1,yv.shape[0]-2):
        for j in range(1,yv.shape[1]-2):
            if grad[1][i,j]<0:
                s = (yv[i-1,j] - yv[i,j])/grad[1][i,j]
            if grad[1][i,j]>0:
                s = (yv[i+1,j] - yv[i,j])/grad[1][i,j]
            min_dt = min(s,min_dt)
    return min_dt/2
