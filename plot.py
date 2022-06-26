import imp
from basics import *

xv = np.array(pd.read_csv('data/xv.csv',header=None))
yv = np.array(pd.read_csv('data/yv.csv',header=None))
phi = np.array(pd.read_csv('data/phi.csv',header=None))
step = np.load('data/step.npy')
data = np.load('data/data.npy')

#------Plot phi, as color map or 3d height map
# fig1 = plt.figure()
# plt.pcolormesh(a,b,phi)
# plt.title('phi as color map')

# fig2 = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(a,b, phi)
# plt.title('phi as 3d height map')
# plt.show()

#------Plot grid as a mesh
fig3 = plt.figure()
ps = 3  #plot spacing
plt.plot(xv[0:-1:ps,0:-1:ps],yv[0:-1:ps,0:-1:ps])
plt.plot(np.transpose(xv)[0:-1:ps,0:-1:ps],np.transpose(yv)[0:-1:ps,0:-1:ps])
ax = plt.gca() 
ax.set_aspect(1)

fig_img = plt.figure()
plt.imshow(np_img,cmap='gray')

#-----Plot step size and error
fig4 = plt.figure()
plt.plot(*zip(*step))
plt.title('step size for generations')  #allows check for convergence

fig5 = plt.figure()
plt.plot(*zip(*data))
plt.title('error for generations')
#------------------------------
plt.show()
