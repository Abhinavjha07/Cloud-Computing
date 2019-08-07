from shutil import copyfile
import os
n = 30
i =1
skill_set = set()
path = '/home/abhinav/5th_Semester/Cloud_Computing/Lab7-8/'
d = dict()
while i<= 30:
    f_name = str(i)+'.txt'
    
    with open(f_name,'r') as fi:
        for line in fi:
            
            l = line.split(' ')

            if l[0]=='Skills-':
                skill_set.add(l[1])
                d[f_name] = l[1]
                

    i+=1

#print(d)
for x in skill_set:
    newpath = './'+x[:len(x)-1] 
    if not os.path.exists(newpath):
            os.makedirs(newpath)

for x in skill_set:
    print(x,end=' ')
    for key,value in d.items():
        if value == x:
            print(' : ',key)
            
            dir_name = path+value[:len(value)-1]+'/'+key
            copyfile(path+key,dir_name)
            
    


