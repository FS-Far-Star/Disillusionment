import imp

from matplotlib.ft2font import HORIZONTAL
from loading import *
import numpy as np
from stl import mesh

side = xv.shape[0]

vertices = []
for i in range(0,side):
    for j in range(0,side):
        vertices.append([xv[i,j],yv[i,j],zv[i,j]+1])
k = len(vertices)

for i in range(0,side):
    vertices.append([xv[i,0],yv[i,0],0])

s = len(vertices)
print(s)

for i in range(0,side):
    vertices.append([xv[i,-1],yv[i,-1],0])

# for j in range(0,side):
#     vertices.append([xv[0,j],yv[0,j],0])
# for j in range(0,side):
#     vertices.append([xv[-1,j],yv[-1,j],0])
vertices = np.array(vertices)

def find(i,j):
    return i*side+j

faces = []
for i in range(0,side-1):
    for j in range(0,side-1):
        faces.append([find(i,j),find(i+1,j),find(i,j+1)])
        faces.append([find(i+1,j),find(i,j+1),find(i+1,j+1)])
for i in range(0,side-1):
    faces.append([find(i,0),k+i,k+i+1])
    faces.append([find(i,0),find(i+1,0),k+i+1])
for i in range(0,side-1):
    faces.append([(i+1)*side-1,s+i,s+i+1])
    faces.append([(i+1)*side-1,(i+2)*side-1,s+i+1])
faces = np.array(faces)

# Create the mesh
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        cube.vectors[i][j] = vertices[f[j],:]

# Write the mesh to file "cube.stl"
cube.save('cube.stl')