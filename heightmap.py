from functions import *
from basics import *

if testing == False:
    xv = np.array(pd.read_csv('data/xv.csv',header=None))
    yv = np.array(pd.read_csv('data/yv.csv',header=None))
elif testing == True:
    xv = np.array(pd.read_csv('testing_data/xv.csv',header=None))
    yv = np.array(pd.read_csv('testing_data/yv.csv',header=None))

'''calculate heightmap'''
zv = 0.02*np.ones((np_img.shape[0],np_img.shape[1]))    #initial guess
#print(zv)

# for i in range(1,height_requirement):
d = 0.2*np.ones((np_img.shape[0],np_img.shape[1]))
#print(d)
k = d - zv  #actual height
#print(k)

#for i in range(0,3):
normal = calc_norm(xv,yv,spacing_x,spacing_y,k)      #3D array containing x,y components of normal vectors
div = div_norm(normal) 
#print(div[0:10,0:10])                                 #divergance of normal 
zv = solve_poisson(zv,div,poisson_requirement)
#k = d -zv



# Plot heightmap, as color map or 3d height map
fig1 = plt.figure()
plt.pcolormesh(a,b,zv)
#plt.pcolormesh(a,b,div[:-1,:-1])
# plt.title('heightmap as color map')
fig2 = plt.figure()
ax = fig2.add_subplot(111, projection='3d')
ax.plot_surface(a,b,0.01*zv)
#ax.plot_surface(a,b,div[:-1,:-1])
#plt.title('heightmap as 3d height map')
plt.show()