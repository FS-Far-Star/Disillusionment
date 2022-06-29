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

for i in range(1,2):
    d = np.ones((np_img.shape[0],np_img.shape[1]))
    d = np.subtract(d,zv)  #actual height
    normal = calc_norm(xv,yv,spacing_x,spacing_y,d)
    div = div_norm(normal)                          #divergance of normal 
    zv = solve_poisson2(zv,div,poisson_requirement)
    zv -= np.min(zv)        # offset ok because neumann boundary condition, abs. height doesn't matter
    zv = zv*spacing_x     # is this even legal???

# Plot heightmap, as color map or 3d height map

# fig1 = plt.figure()
# plt.pcolormesh(a,b,zv)
# plt.title('heightmap as color map')
fig2 = plt.figure()
ax = fig2.add_subplot(111, projection='3d')
ax.plot_surface(a,b, zv)
plt.title('heightmap as 3d height map')
plt.show()