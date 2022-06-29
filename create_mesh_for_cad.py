import imp
from basics import *
xv = np.array(pd.read_csv('testing_data/xv.csv',header=None))
yv = np.array(pd.read_csv('testing_data/yv.csv',header=None))
zv = np.array(pd.read_csv('testing_data/zv.csv',header=None))

output = np.zeros((xv.shape[0]*xv.shape[1],3))
print(output.shape)
print(xv.shape)
print(xv.shape[0]-1)

for i in range(0,10):
    print(i)

for i in range(0,xv.shape[0]):
    for j in range(0,xv.shape[1]):
        #print(i*xv.shape[0]+j)
        output[i*xv.shape[0]+j,0]=xv[i,j]
        output[i*xv.shape[0]+j,1]=yv[i,j]
        output[i*xv.shape[0]+j,2]=zv[i,j]
print(output)

pd.DataFrame(output).to_csv("testing_data/output.csv",header=None, index=None)

#absolute rubbish at the moment, does not work