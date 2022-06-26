from functions import *
from init import *

spacing_x = width/np_img.shape[1]   #for the sake of simplicity, the image used is a square,
spacing_y = height/np_img.shape[0]  #so the spacings are equal

xv = np.array(pd.read_csv('data/xv.csv',header=None))
yv = np.array(pd.read_csv('data/yv.csv',header=None))

'''calculate heightmap'''
normal = calc_norm(xv,yv,spacing_x,spacing_y)  #3D array containing x,y components of normal vectors
div = div_norm(normal)  #divergance of normal 
guess = 0.02*np.ones((np_img.shape[0],np_img.shape[1]))
heightmap = solve_poisson(guess,div,poisson_requirement)

# Plot heightmap, as color map or 3d height map

x = np.linspace(0,width,np_img.shape[0])
y = np.linspace(0,height,np_img.shape[1])
a,b = np.meshgrid(x, y)

fig1 = plt.figure()
plt.pcolormesh(a,b,heightmap)
plt.title('heightmap as color map')
fig2 = plt.figure()
ax = fig2.add_subplot(111, projection='3d')
ax.plot_surface(a,b, heightmap)
plt.title('heightmap as 3d height map')
plt.show()