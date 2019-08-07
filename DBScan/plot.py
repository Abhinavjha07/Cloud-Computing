import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.style.use(['ggplot'])

data = np.loadtxt("output.txt",usecols=(0,1,2,3),delimiter=' ')

fig,ax = plt.subplots()
x1 = data[:,1:2]
x2 = data[:,2:3]
x3 = data[:,3:4]
co = data[:,0:1]


scat = ax.scatter(x1,x2,c = co+4) 
plt.show()
