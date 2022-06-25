import numpy as np
phi = np.arange(100.0).reshape((10,10))
print(phi)
phi = np.rot90(phi, 3)
print(phi)