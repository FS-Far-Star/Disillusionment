import imp
from matplotlib.ft2font import HORIZONTAL
from loading import *
import numpy as np
from stl import mesh

side = xv.shape[0]
def find(i,j):
    # Note!!!!! DO NOT use with -1 syntax
    return i*side+j
s = np.max(zv)
lift = thickness - s

vertices = []
# All locations on the mesh
for i in range(0,side):                                 
    for j in range(0,side):
        vertices.append([xv[i,j],yv[i,j],zv[i,j]+lift])
k = len(vertices)

# Extend for sides
for i in range(0,side):                                 
    vertices.append([xv[i,0],yv[i,0],0])

for i in range(0,side):
    vertices.append([xv[i,-1],yv[i,-1],0])

for j in range(0,side):
    vertices.append([xv[0,j],yv[0,j],0])
for j in range(0,side):
    vertices.append([xv[-1,j],yv[-1,j],0])

faces = []
for i in range(0,side-1):
    for j in range(0,side-1):
        faces.append([find(i,j),find(i+1,j),find(i,j+1)])
        faces.append([find(i+1,j),find(i,j+1),find(i+1,j+1)])

for i in range(0,side-1):                                   #vertical, side 1
    faces.append([i*side,k+i,k+i+1])
    faces.append([i*side,(i+1)*side,k+i+1])
for i in range(0,side-1):                                   #vertical, opposite of side 1
    faces.append([(i+1)*side-1,k+side+i,k+side+i+1])
    faces.append([(i+1)*side-1,(i+2)*side-1,k+side+i+1])

for j in range(0,side-1):                                   #horizontal, side 2
    faces.append([j,k+side*2+j,k+side*2+j+1])
    faces.append([j,j+1,k+side*2+j+1])
for j in range(0,side-1):                                   #horizontal, opposite of side 2
    faces.append([k-side+j,k+side*3+j,k+side*3+j+1])
    faces.append([k-side+j,k-side+j+1,k+side*3+j+1])

faces.append([k,k+side,k+side*3])                        #back face
faces.append([k+side,k+side*3,k+side*4-1])

# print(vertices[k])
# print(vertices[k+side])
# print(vertices[k+side*3])
# print(vertices[k+side*4-1])

vertices = np.array(vertices)
faces = np.array(faces)

# Create the mesh
cad = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        cad.vectors[i][j] = vertices[f[j],:]

# Write the mesh to file "cad.stl"
cad.save('CAD.stl')
print('complete')