import math
regStu=list()
print('Course Registration System')
fileStudentR=open("student.txt","r")
fileStudentW=open("student.txt","a")
fileStuCo=open("student_course.txt","a")
while True :
    n=int(input("\nEnter : \n1 to register\n2 to quit\n"))
    if n==2 :
        break

    else :
        name = input('Enter your name : ')

        roll = input('Enter your Roll No. : ')
        for line in fileStudentR:
            stu=line.split()
            regStu.append(stu[0])
        err=0
        if roll in regStu:
            err=1
            print('Student is already registered!!')
        if err==0 :
            semester = input('Enter Semester : ')
            branch = input('Enter the branch : ')
            
            fileStudentW.write('{} {} {} {}\n'.format(roll,name,semester,branch))
            fileCourse=open("course.txt","r")
            fileHss=open("hss_elective.txt","r")
            fileElec=open("electives.txt","r")
            flag=0
            flag1=0
            elec=0
            hsselec=0
            print("\nMandatory Courses:")
            for line in fileCourse:
                course = line.split()
                
                if course[0] == semester:
                    

                    if(course[2].startswith("Elective_")) :
                       flag=1
                       elec+=1
                    elif course[2].startswith("Elective") :
                        flag1=1
                        hsselec+=1
                    else:
                        print(course[1],course[2])
                        fileStuCo.write('{} {} {} {} {}\n'.format(roll,name,semester,course[1],course[2]))


            if flag1==1:
                print('\nHSS Elective Courses : ')
                print("Choose %d course(s) : " % hsselec)
                courseId=dict()
                for line in fileHss:
                       course=line.split()
                       x=int(course[0][2])
                       if x== math.ceil(int(semester)/2):
                           courseId[course[0]]=course[1]
                           print(course[0],course[1])
                i=0
                while i < hsselec:
                    s=input('Enter courseId : ')
                    if s in courseId : 
                        fileStuCo.write('{} {} {} {} {}\n'.format(roll,name,semester,s,courseId[s]))
                        i+=1
                    else :
                        print('Enter a valid subject code!!')
                       
            if flag==1:
                print('\nElective Courses : ')
                print("Choose %d course(s) : " % elec)
                courseId=dict()
                for line in fileElec:
                    course=line.split()
                    x=int(course[0][2])
                    if x== math.ceil(int(semester)/2):
                        courseId[course[0]]=course[1]
                        print(course[0],course[1])
                i=0
                while i < elec:
                    s=input('Enter courseId : ')
                    if s in courseId : 
                        fileStuCo.write('{} {} {} {} {}\n'.format(roll,name,semester,s,courseId[s]))
                        i+=1
                    else :
                        print('Enter a valid subject code!!')

            print('\nRegistered Successfully!!\n')
            fileCourse.close()
            fileHss.close()
            fileElec.close()
          
fileStudentW.close()
fileStuCo.close()
fileStudentR.close()






