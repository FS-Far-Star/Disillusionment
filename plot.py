import imp
from loading import *

#------Plot phi, as color map or 3d height map
# fig1 = plt.figure()
# plt.pcolormesh(a,b,phi)
# plt.title('phi as color map')

# fig2 = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(a,b,phi)
# plt.title('phi as 3d height map')
# plt.show()

#------Plot grid as a mesh
fig3 = plt.figure()
ps = 1  #plot spacing
lw = 0.2
plt.plot(xv[::ps,::ps],yv[::ps,::ps],linewidth = lw)
plt.plot(np.transpose(xv)[::ps,::ps],np.transpose(yv)[::ps,::ps],linewidth=lw)
ax = plt.gca() 
ax.set_aspect(1)

<<<<<<< HEAD
# fig_img = plt.figure()
# plt.imshow(img,cmap='gray')
=======
fig_img = plt.figure()
plt.imshow(np_img,cmap='gray')
>>>>>>> parent of b237432 (Merge branch 'main' of https://github.com/FS-Far-Star/Disillusionment)

#-----Plot step size and error
fig4 = plt.figure()
plt.plot(*zip(*step))
plt.title('step size for generations')  #allows check for convergence

fig5 = plt.figure()
plt.plot(*zip(*data))
plt.title('error for generations')
#------------------------------

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
