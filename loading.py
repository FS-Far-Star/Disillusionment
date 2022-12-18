from init import *

k = pd.read_excel('testing_data/1.xlsx','Sheet1')
k = np.array(k)
print(k)
a = k[:,1]
b =[]
for i in a:
    # print(type(i),i)
    if type(i) == int:
        b.append(i)
# print(b)
plt.hist(b,6)
plt.title('Pit size distribution for 775C, 30 seconds')
plt.xlabel('Diameter/nm')
plt.ylabel('Number')
plt.show()

if testing == False:
    xv = np.array(pd.read_csv('data/xv.csv',header=None))
    yv = np.array(pd.read_csv('data/yv.csv',header=None))
    phi = np.array(pd.read_csv('data/phi.csv',header=None))
    step = np.load('data/step.npy')
    data = np.load('data/data.npy')
    zv_path = 'data/zv.csv'
    check = os.path.isfile(zv_path)
    if check == True:
        zv = np.array(pd.read_csv('data/zv.csv',header=None))
    else:
        zv= []
else: 
    xv = np.array(pd.read_csv('testing_data/xv.csv',header=None))
    yv = np.array(pd.read_csv('testing_data/yv.csv',header=None))
    phi = np.array(pd.read_csv('testing_data/phi.csv',header=None))
    step = np.load('testing_data/step.npy')
    data = np.load('testing_data/data.npy')
    zv_path = 'testing_data/zv.csv'
    check = os.path.isfile(zv_path)
    if check == True:
        zv = np.array(pd.read_csv('testing_data/zv.csv',header=None))
    else:
        zv= []

# print(np.max(zv)-np.min(zv))