from basics import *
from functions import *

'''Coordinate system'''
x = np.linspace(0,width,np_img.shape[0]+1)
y = np.linspace(0,height,np_img.shape[1]+1)
xv, yv = np.meshgrid(x, y)  #xv and yv saves the real position of the points, the index of the matrix saves the order of the points       

'''Solve Poisson and morph the grid'''
data = []
step = []
#----------------- start of iterations--------------
for calculation in range(1,morph_grid_requirement+1):
    area_grid = area_grid_update(xv,yv,A_t)     #calculate area based on new coordinates, result is normalized
    print('generation',calculation)
    loss = calculate_loss(area_grid,brightness_comp)
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

    #Morph the grid
    grad = calc_grad(phi)   # calculate graident
    step_size = find_step_size(xv,yv,grad)      # find appropriate step size so that points don't surpass ones with higher index
    # print(step_size)
    delta_x = grad[0]*step_size                 
    delta_y = grad[1]*step_size 
    xv[1:-1,1:-1] += delta_x[1:,1:]             # gradient descend
    yv[1:-1,1:-1] += delta_y[1:,1:]

    # Plot the mesh
    # plt.plot(xv,yv)
    # plt.plot(np.transpose(xv),np.transpose(yv))
    # ax = plt.gca() 
    # ax.set_aspect(1)
    # plt.show()
    
    # Plot vector field
    # ps = 3    #plot spacing
    # plt.quiver(a[0:-1:ps,0:-1:ps],b[0:-1:ps,0:-1:ps],delta_x[0:-1:ps,0:-1:ps],delta_y[0:-1:ps,0:-1:ps])
    # ax = plt.gca() 
    # ax.set_aspect(1)
    # plt.show()

    #check for collision, shouldn't happen at all as step size was chosen to avoid it
    for i in range(0,xv.shape[0]-1):
        for j in range(0,yv.shape[1]-1):
            if xv[i,j] > xv[i,j+1]:
                xv[i,j] = xv[i,j+1]
                print('collision')
            if yv[i,j] > yv[i+1,j]:
                yv[i,j] = yv[i+1,j]
                print('collision')

    data.append((calculation,np.sum(np.multiply(loss,loss))))
    step.append((calculation,step_size))
#----------------- end of iterations----------------
    
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

