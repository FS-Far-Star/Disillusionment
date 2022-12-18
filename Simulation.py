import imp
from loading import *
from functions import *
import random

error = False

k = np.mean(zv)
zv = (zv-k)*1.5+k
print('max_diff',np.max(zv)-np.min(zv))
side = xv.shape[0]
input = np.array([0,0,1])          #input light direction
output = np.zeros((np_img.shape[0],np_img.shape[1]))
print('total # of faces:',side*side*2)
counter = 0
out_of_bounds = []
record = []

for i in range(0,side-1):                                 
    for j in range(0,side-1):
        if error == False:
            a = np.array([xv[i,j],yv[i,j],zv[i,j]])
            b = np.array([xv[i+1,j],yv[i+1,j],zv[i+1,j]])
            c = np.array([xv[i+1,j+1],yv[i+1,j+1],zv[i+1,j+1]])
            d = np.array([xv[i,j+1],yv[i,j+1],zv[i,j+1]])
        elif error == True:
            a = np.array([xv[i,j],yv[i,j],zv[i,j]]) + [random.uniform(0, 10)/1000,random.uniform(0, 10)/1000,random.uniform(0, 10)/1000]
            b = np.array([xv[i+1,j],yv[i+1,j],zv[i+1,j]]) + [random.uniform(0, 10)/1000,random.uniform(0, 10)/1000,random.uniform(0, 10)/1000]
            c = np.array([xv[i+1,j+1],yv[i+1,j+1],zv[i+1,j+1]]) + [random.uniform(0, 10)/1000,random.uniform(0, 10)/1000,random.uniform(0, 10)/1000]
            d = np.array([xv[i,j+1],yv[i,j+1],zv[i,j+1]]) + [random.uniform(0, 10)/1000,random.uniform(0, 10)/1000,random.uniform(0, 10)/1000]
        # for surface defined by abd
        abd_centre = find_centre(a,b,d)
        abd_area = find_area(a,b,d)         #projected area

        normal = find_normal(a,b,d)*-1
        parallel = np.dot(input,normal)*normal
        orthogonal = input - parallel
        dot_product = np.dot(orthogonal,normal)
        assert round(dot_product, 10) == 0.0          # protection
        out_orth = eta*orthogonal
        out = out_orth+parallel
        distance_to_go = proj_distance - abd_centre[2]
        scale = distance_to_go/out[2]
        offset = out*scale
        landing = abd_centre+offset
        closest_abd = landing//spacing
        x = int(closest_abd[1])
        y = int(closest_abd[0])
        
        if x > side-2 or y > side-2 or x < 0 or y < 0:
            counter +=1
            out_of_bounds.append(('abd',i,j))
        else: 
            output[x,y] += abd_area

        # for surface defined by bcd
        bcd_centre = find_centre(b,c,d)
        bcd_area = find_area(b,c,d)         #projected area

        normal = find_normal(b,c,d)*-1
        parallel = np.dot(input,normal)*normal
        orthogonal = input - parallel
        dot_product = np.dot(orthogonal,normal)
        assert round(dot_product, 10) == 0.0          # protection
        out_orth = eta*orthogonal
        out = out_orth+parallel
        distance_to_go = proj_distance - bcd_centre[2]
        scale = distance_to_go/out[2]
        offset = out*scale
        landing = bcd_centre+offset
        closest_bcd = landing//spacing
        x = int(closest_bcd[1])
        y = int(closest_bcd[0])

        if x > side-2 or y > side-2 or x < 0 or y < 0:
            counter +=1
            out_of_bounds.append(('bcd',i,j))
        else: 
            output[x,y] += bcd_area

        record.append((j,i,closest_abd[:-1],closest_abd[:-1]))
        # print('area',abd_area)
        # print('normal',normal)
        # print('parallel',parallel)
        # print('orthogonal',orthogonal)
        # print('dot',c)
        # print('out',out)
        # print('landing',landing)
        # print('closest',closest)
print('faces out of bounds:',counter)
# print('Out of bounds list:', out_of_bounds)

# max = np.max(output)
# scale = 256/max
# output *= scale
# print(output)
# print(np.max(output))

record = np.array(record)
pd.DataFrame(record).to_csv("testing_data/record.csv",header=None, index=None)
error = 0
for (a,b,c,d) in record:
    if round(c[0]-a,3) !=0 or round(c[1]-b,3):
        error += 1
    if round(d[0]-a,3) !=0 or round(d[1]-b,3):
        error += 1
print('number of errors:',error)

sum = np.sum(output)
average = sum/side**2
scale = 64/average
output*=scale
print('scaling',scale)

overwrite = 0
for i in range(0,np_img.shape[0]):
    for j in range(0,np_img.shape[1]):
        if output[i,j]>256:
            output[i,j]=256
            overwrite += 1
print('Brightness overwrite:',overwrite)

# output = np.rot90(output, 2)

image = Image.fromarray(output)
plt.imsave('Result.png', image, cmap='gray')
image.show()
print('complete')