import imp
from init import *
from functions import *

arr = np.reshape(np.arange(0,9),(3,3))
left_right = np.flip(arr,1)
top_bot = np.flip(arr,0)
corner = np.flip(np.flip(arr,0),1)

row1 = np.concatenate((corner,top_bot,corner),axis=1)
row2 = np.concatenate((left_right,arr,left_right),axis=1)

result = np.concatenate((row1,row2,row1),axis=0)

print(result)
# print(arr)
# print(np.flip(arr,0))           # flip down
# print(np.flip(arr,1))           # flip to the left

# arr1 = np.array([1, 2, 3])

# arr2 = np.array([4, 5, 6])

# arr = np.stack((arr1, arr2), axis=1)

# print(arr)

# arr = np.stack((arr1, arr2), axis=0)

# print(arr)