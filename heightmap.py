from functions import *
from loading import *

'''calculate heightmap'''
zv = 2*np.ones((xv.shape[0],xv.shape[1]))    #initial guess

max_diff = []
for i in range(1,20):
    d = 1000*np.ones((xv.shape[0],xv.shape[1]))
    d = np.subtract(d,zv)  #actual height
    normal = norm(xv,yv,spacing_x,spacing_y,d)
    div = div_norm(normal)                          #divergance of normal 
    #print(div)
    zv = solve_poisson2(zv,div,poisson_requirement)
    # zv -= np.sum(div)
    zv -= np.min(zv)        # offset ok because neumann boundary condition, abs. height doesn't matter
    #zv = zv*spacing_x     # is this even legal???
    max_diff.append((i,(np.max(zv)-np.min(zv))))

    print(np.max(zv))
    # print(np.min(zv))

'''save data'''
if testing == False:
    pd.DataFrame(zv).to_csv("data/zv.csv",header=None, index=None)
else: 
    pd.DataFrame(zv).to_csv("testing_data/zv.csv",header=None, index=None)

# Plot heightmap, as color map or 3d height map

fig4 = plt.figure()
plt.plot(*zip(*max_diff))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xv,yv,zv)
plt.title('complete contour')
plt.show()

points = np.c_[xv.reshape(-1), yv.reshape(-1), zv.reshape(-1)]
cloud = pv.PolyData(points)
surf = cloud.delaunay_2d()
surf.plot(show_edges=True)
print('complete')
