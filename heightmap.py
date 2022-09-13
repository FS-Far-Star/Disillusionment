from functions import *
from loading import *

'''calculate heightmap'''
guess = np.ones((xv.shape[0],xv.shape[1]))    #initial guess
zv = guess

max_diff = []
for i in range(1,40):
    d = proj_distance*np.ones((xv.shape[0],xv.shape[1]))      # projection distance is specified in init
    d = np.subtract(d,zv)                           #actual distance from exit surface to wall 
    normal = norm(xv,yv,spacing,d)
    div = div_norm(normal)                          #divergance of normal 
    assert round(np.sum(div),5) == 0
    # As before, the input to the poisson solver needs to sum to zero

    zv = solve_poisson(guess,div,poisson_requirement)
    # You MUST NOT: scale zv by a factor, as zv is determined by slopes
    # You CAN ?   : offshift zv by a constant, but this have a physical meaning

    max_diff.append((i,(np.max(zv)-np.min(zv))))
    # print('max',np.max(zv))
    # print('min',np.min(zv))
    # print(np.min(zv))

'''save data'''
if testing == False:
    pd.DataFrame(zv).to_csv("data/zv.csv",header=None, index=None)
    np.save('data/max_diff',max_diff)
else: 
    pd.DataFrame(zv).to_csv("testing_data/zv.csv",header=None, index=None)
    np.save('testing_data/max_diff',max_diff)

# Plot heightmap, as color map or 3d height map

fig4 = plt.figure()
plt.plot(*zip(*max_diff))

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(xv,yv,zv)
# plt.title('complete contour')
plt.show()

# points = np.c_[xv.reshape(-1), yv.reshape(-1), zv.reshape(-1)]
# cloud = pv.PolyData(points)
# surf = cloud.delaunay_2d()
# surf.plot(show_edges=True)
print('complete')