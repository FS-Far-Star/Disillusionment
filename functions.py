from unicodedata import mirrored
from init import *
from shapely.geometry import Polygon
import numba
from numba import jit

import logging;
logger = logging.getLogger("numba")
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

def dupe(arr):
    left_right = np.flip(arr,1)
    top_bot = np.flip(arr,0)
    corner = np.flip(np.flip(arr,0),1)
    row1 = np.concatenate((corner,top_bot,corner),axis=1)
    row2 = np.concatenate((left_right,arr,left_right),axis=1)
    result = np.concatenate((row1,row2,row1),axis=0)
    return result

@jit   #the numpy grad is unfortunately too advanced
def calc_grad(arr,sp=spacing):
    result = dupe(arr)
    side = arr.shape[0]
    grad_x, grad_y = np.zeros((side+1,side+1)) , np.zeros((side+1,side+1))
    for i in range(0,side+1):
        for j in range(0,side+1):
            a = i+side
            b = j+side
            grad_x[i,j] = (result[a,b]-result[a,b-1])/sp
            grad_y[i,j] = (result[a,b]-result[a-1,b])/sp
    grad = [grad_x,grad_y]
    return np.array(grad)

@jit    #solve poisson with relaxation
def solve_poisson(phi,loss,iteration,dx=spacing,dy=spacing,tolerance=1e-9):
	max_change = 100
    i = 0
	while i < iteration and max_change>tolerance:
		phi_old = phi
		# center
		phi[1:-1,1:-1] = (dy**2*(phi_old[1:-1,2:]+phi_old[1:-1,:-2])+dx**2*(phi_old[:-2,1:-1]+phi_old[2:,1:-1])+(dx*dy)**2*loss[2:nx,2:ny])/(2*(dx**2+dy**2))
		# left edge
		phi[0,1:-1] = (dy**2*(phi_old[0,2:]+phi_old[0,:-2])+dx**2*(phi_old[1,1:-1]*2)+(dx*dy)**2*loss[0,1:-1])/(2*(dx**2+dy**2))
		# right edge
		phi[-1,1:-1] = (dy**2*(phi_old[-1,2:]+phi_old[-1,:-2])+dx**2*(phi_old[-2,1:-1]*2)+(dx*dy)**2*loss[-1,1:-1])/(2*(dx**2+dy**2))
		# top edge
		phi[1:-1,0] = (dy**2*(phi_old[1:-1,1]*2)+dx**2*(phi_old[:-2,0]+phi_old[2:,0])+(dx*dy)**2*loss[1:-1,0])/(2*(dx**2+dy**2))
		# bottom edge
		phi[1:-1,-1] = (dy**2*(phi_old[1:-1,-2]*2)+dx**2*(phi_old[:-2,-1]+phi_old[2:,-1])+(dx*dy)**2*loss[1:-1,-1])/(2*(dx**2+dy**2))
		# top left corner
		phi[0,0] = (dy**2*(phi_old[0,1]*2)+dx**2*(phi_old[1,0]*2)+(dx*dy)**2*loss[0,0])/(2*(dx**2+dy**2))
		# top right corner
		phi[-1,0] = (dy**2*(phi_old[-1,1]*2)+dx**2*(phi_old[-2,0]*2)+(dx*dy)**2*loss[-1,0])/(2*(dx**2+dy**2))
		# bottom left corner
		phi[0,-1] = (dy**2*(phi_old[0,-2]*2)+dx**2*(phi_old[1,-1]*2)+(dx*dy)**2*loss[0,-1])/(2*(dx**2+dy**2))
		# bottom right corner
		phi[-1,-1] = (dy**2*(phi_old[-1,-2]*2)+dx**2*(phi_old[-2,-1]*2)+(dx*dy)**2*loss[-1,-1])/(2*(dx**2+dy**2))
		max_change = (phi-phi_old).max()
        i += 1
    return phi

@jit    # update area of every grid
def area_grid_update(xv,yv,A_t):
    area_grid = np.zeros((xv.shape[0]-1,xv.shape[1]-1))
    for i in range(0,xv.shape[0]-1):
        for j in range(0,xv.shape[1]-1):
            area_grid[i,j] = area(i,j,xv,yv)
    return area_grid/A_t

@jit    #calculate the loss matrix
def calculate_loss(area_grid,brightness_comp):
    loss = area_grid - brightness_comp
    return loss

@jit    #find the maximum allowed step size, then divide by two
def find_step_size(xv,yv,grad):
    min_dt = 1000000
    for i in range(1,xv.shape[0]-1):
        for j in range(1,xv.shape[1]-1):
            if grad[0][i,j]<0:
                s = (xv[i,j-1] - xv[i,j])/grad[0][i,j]
            if grad[0][i,j]>0:
                s = (xv[i,j+1] - xv[i,j])/grad[0][i,j]
            min_dt = min(s,min_dt)    
    for i in range(1,yv.shape[0]-1):
        for j in range(1,yv.shape[1]-1):
            if grad[1][i,j]<0:
                s = (yv[i-1,j] - yv[i,j])/grad[1][i,j]
            if grad[1][i,j]>0:
                s = (yv[i+1,j] - yv[i,j])/grad[1][i,j]
            min_dt = min(s,min_dt)
    return min_dt/2

#calculate the normal vectors of the mirror surface
def norm(xv,yv,spacing,d):
    normal = np.zeros((xv.shape[0],xv.shape[1],2))
    for i in range(0,xv.shape[0]):
        for j in range(0,xv.shape[1]):
            u = (j+1)*spacing
            v = (i+1)*spacing   #coordinates of pixels on the image plane
            normal[i,j,0] = np.tan((np.arctan((u-xv[i,j])/d[i,j]))/(eta-n1))
            normal[i,j,1] = np.tan((np.arctan((v-yv[i,j])/d[i,j]))/(eta-n1))
    return normal

# def norm(xv,yv,spacing,d):
#     normal = np.zeros((xv.shape[0],xv.shape[1],2))
#     for i in range(0,xv.shape[0]-1):
#         for j in range(0,xv.shape[1]-1):
#             u = j*spacing
#             v = i*spacing
#             # q_p = (u-xv[i,j],v-yv[i,j])
#             squared = (u-xv[i,j]) * (u-xv[i,j]) + (v-yv[i,j]) * (v-yv[i,j])
#             k = eta * np.sqrt(squared + d[i,j]**2) - d[i,j]
#             normal[i,j] = (u-xv[i,j],v-yv[i,j])/k
#     return normal

def div_norm(normal):
    div = np.zeros([normal.shape[0],normal.shape[1]])
    x = dupe(normal[:,:,0])
    y = dupe(normal[:,:,1])
    side = div.shape[0]
    for i in range(0,side):
        for j in range(0,side):
            a = i+side
            b = j+side
            delta_x = (x[a,b]-x[a,b-1])/spacing
            delta_y = (y[a,b]-y[a-1,b])/spacing
            div[i,j] = delta_x + delta_y
    k = np.mean(div)
    for i in range(0,div.shape[0]):
        for j in range(0,div.shape[1]): 
            div[i,j] -= k                               
    return div

def find_centre(a,b,c):
    x = (a[0]+b[0]+c[0])/3
    y = (a[1]+b[1]+c[1])/3
    z = (a[2]+b[2]+c[2])/3
    return np.array([x,y,z])

def find_normal(a,b,c):
    v = b-a
    w = c-a
    normal = np.cross(v,w)
    magnitude = np.sqrt(normal[0]**2+normal[1]**2+normal[2]**2)
    return normal/magnitude
    # return normal

@jit
def find_area(a,b,c):
    x = [a[0],b[0],c[0]]
    y = [a[1],b[1],c[1]]
    shape = Polygon(zip(x,y))
    return shape.area
