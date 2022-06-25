import numpy as np
from PIL import Image
import matplotlib.pyplot as plt 
img = Image.open('download1.png').convert('L')

A = np.array(img)

G = np.array([[-1,-1,-1], [-1, 8,-1,], [-1,-1,-1,]])
B = np.zeros(A.shape)
for i in range(1, B.shape[0]- 1): 
    for j in range(1, B.shape[1]- 1): 
        for k in range(3): 
            for l in range(3): 
                B[i, j] += G[k, l]*A[i- 1 + k, j- 1 + l]
                if abs(B[i,j])<30:
                    B[i,j]=0

# plt.imshow(B, cmap='gray')
# plt.show()