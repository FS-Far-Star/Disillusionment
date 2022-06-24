import numpy as np
x1 = np.arange(100.0).reshape((100))
np.save('test',x1)
x2 = np.load('test.npy')
print(x2)