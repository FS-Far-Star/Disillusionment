from init import *
from functions import *

'''Coordinate system'''
x = np.linspace(0,width,np_img.shape[0]+1)
y = np.linspace(0,height,np_img.shape[1]+1)
xv, yv = np.meshgrid(x, y)  
#xv and yv saves the real position of the points, the index of the matrix saves the order of the points       

'''Solve Poisson and morph the grid'''
data = []
step = []
collision_counter = 0
#-------------------------Start of iterations----------------------------------------------------------
for calculation in range(1,morph_grid_requirement+1):
    area_grid = area_grid_update(xv,yv,A_t)     
    #calculate area based on new coordinates, result is normalized

    loss = calculate_loss(area_grid,brightness_comp)
    assert round(np.sum(loss),4) == 0
    # Note: 1. the input to the poisson solver, in this case loss, must sum to zero for solution to be stable
    #       2. From a geometric argument, if any of the shapes is not convex, or outer border is moved, then sum of 
    #          area grid will not be 1. If that happens, loss will not sum to zero. 

    #Solve Poisson
    guess = np.ones((np_img.shape[0],np_img.shape[1]))
    phi = solve_poisson(guess,-loss,poisson_requirement)

    # Plot phi, as color map or 3d height map
    # fig1 = plt.figure()
    # plt.pcolormesh(a,b,phi)
    # plt.title('phi as color map')
    # fig2 = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot_surface(a,b, phi)
    # plt.title('phi as 3d height map')
    # plt.show()

    # Morph the grid
    grad = calc_grad(phi)

    # grad[1][0,:] = grad2[1][0,:]
    # grad[1][-1,:] = grad2[1][-1,:]
    # grad[1][:,0] = grad2[1][:,0]
    # grad[1][:,-1] = grad2[1][:,-1]

    # grad[0][:,0] = grad2[0][:,0]
    # grad[0][:,-1] = grad2[0][:,-1]
    # grad[0][-1,:] = grad2[0][-1,:]
    # grad[0][0,:] = grad2[0][0,:]

    step_size = find_step_size(xv,yv,grad)      
    # find appropriate step size so that points don't surpass ones with higher index
    delta_x = grad[0]*step_size                 
    delta_y = grad[1]*step_size

    print('step_size',step_size)
    if round(step_size,8) == 0:
        # if step size is too small, stop wasting time
        break
    elif np.max(delta_x) < 1e-6 and np.max(delta_y) < 1e-6:
        print('Step size too small, interrupted')
        break

    xv += delta_x            # gradient descend
    yv += delta_y

    # Plot the mesh
    # plt.plot(xv,yv)
    # plt.plot(np.transpose(xv),np.transpose(yv))
    # ax = plt.gca() 
    # ax.set_aspect(1)
    # plt.show()
    
    # Plot vector field
    # ps = 1    #plot spacing
    # plt.quiver(c[::ps,::ps],d[::ps,::ps],grad[0][::ps,::ps],grad[1][::ps,::ps])
    # ax = plt.gca() 
    # ax.set_aspect(1)
    # plt.show()

    # # Plot vector field
    # ps = 1    #plot spacing
    # plt.quiver(c[::ps,::ps],d[::ps,::ps],delta_x[::ps,::ps],delta_y[::ps,::ps])
    # ax = plt.gca() 
    # ax.set_aspect(1)
    # plt.show()

    # Check for collision, shouldn't happen at all as step size was chosen to avoid it
    for i in range(0,xv.shape[0]-1):
        for j in range(0,yv.shape[1]-1):
            if xv[i,j] > xv[i,j+1]:
                collision_counter +=1
                # xv[i,j] = xv[i,j+1]
                # print('collision')
            if yv[i,j] > yv[i+1,j]:
                collision_counter +=1
                # yv[i,j] = yv[i+1,j]
                # print('collision')
    # And indeed it never happens

    print(round(calculation/morph_grid_requirement*100,3),'%','complete')
    data.append((calculation,np.sum(np.multiply(loss,loss))))
    step.append((calculation,step_size))
#----------------- end of iterations----------------
if collision_counter == 0:
    pass
else: 
    print('collision:',collision_counter)

# Plot loss as a color map, it is expected to be highly uniform
# fig1 = plt.figure()
# plt.pcolormesh(a,b,loss)
# plt.show()

'''save data'''
if testing == False:
    # np.save('data/xv',xv)
    # np.save('data/yv',yv)
    # np.save('data/phi',phi)
    np.save('data/data',data)
    np.save('data/step',step)
    pd.DataFrame(phi).to_csv("data/phi.csv",header=None, index=None)
    pd.DataFrame(xv).to_csv("data/xv.csv",header=None, index=None)
    pd.DataFrame(yv).to_csv("data/yv.csv",header=None, index=None)
elif testing == True:
    # np.save('testing_data/xv',xv)
    # np.save('testing_data/yv',yv)
    # np.save('testing_data/phi',phi)
    np.save('testing_data/data',data)
    np.save('testing_data/step',step)
    pd.DataFrame(phi).to_csv("testing_data/phi.csv",header=None, index=None)
    pd.DataFrame(xv).to_csv("testing_data/xv.csv",header=None, index=None)
    pd.DataFrame(yv).to_csv("testing_data/yv.csv",header=None, index=None)

print('Calculation completed.')
