import numpy as np


data = np.genfromtxt('resume_dataset.csv',usecols=(0,1,2),delimiter = ',',dtype = np.str)
skill = np.genfromtxt('resume_dataset.csv',usecols=(1),delimiter=',',dtype=np.str)

#print(skill[1:])

s = set(skill[1:])
print(s)

for i in s:
    with open(i,'w') as fi : 
        for j in range(len(data)):
            if data[j,1] == i:
                str = data[j,0]+'\t'+data[j,2]+'\n'
                fi.write(str)

        fi.write('\n')


    
        
    


