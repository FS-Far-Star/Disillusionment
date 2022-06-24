import numpy as np
phi = np.arange(100.0).reshape((10,10))
phi[0,:],phi[:,0],phi[-1,:],phi[:,-1] = phi[1,:],phi[:,1],phi[-2,:],phi[:,-2]
print(phi)