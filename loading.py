from basics import *

if testing == False:
    xv = np.array(pd.read_csv('data/xv.csv',header=None))
    yv = np.array(pd.read_csv('data/yv.csv',header=None))
    zv = np.array(pd.read_csv('data/zv.csv',header=None))
    phi = np.array(pd.read_csv('data/phi.csv',header=None))
    step = np.load('data/step.npy')
    data = np.load('data/data.npy')
else: 
    xv = np.array(pd.read_csv('testing_data/xv.csv',header=None))
    yv = np.array(pd.read_csv('testing_data/yv.csv',header=None))
    zv = np.array(pd.read_csv('testing_data/zv.csv',header=None))
    phi = np.array(pd.read_csv('testing_data/phi.csv',header=None))
    step = np.load('testing_data/step.npy')
    data = np.load('testing_data/data.npy')
