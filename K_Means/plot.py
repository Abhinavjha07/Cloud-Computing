import numpy as np
import matplotlib.pyplot as plt

plt.style.use(['ggplot'])

data = np.loadtxt("output2.txt",usecols=(0,1,2),delimiter=' ')

fig,ax =plt.subplots()
x1 = data[:,1:2]
x2 = data[:,2:3]
x3 = data[:,0:1]

scat = ax.scatter(x1,x2,c=x3)
plt.show()
