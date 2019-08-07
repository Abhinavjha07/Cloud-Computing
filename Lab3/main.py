import boto3
import time

def create_Instance(k):
   
    
    new_instances = ec2.create_instances(
        ImageId= 'ami-8c122be9',
        MinCount = 1,
        MaxCount= k,
        InstanceType = 't2.micro',
        SecurityGroups = ['default'],
        KeyName = "Abhi"
        )
    for instance in new_instances:
        instance.create_tags(Tags=[{'Key':'Name','Value':"LAB3"}])
        while instance.state['Name'] not in ('running','stopped'):
            time.sleep(10)
            print("Instance_ID: %s and State is: %s" % (instance.id,instance.state))
            instance.load()

    print("%d instances are created and are running" % k) 

ec2 = boto3.resource('ec2',region_name='us-east-2')
while True :
    x=int(input('\nEnter:\n1 to create instances\n2 to list all running instances\n3 to check health of running instances\n4 to stop the running instances\n5 to exit\n'))
    if x==5 :
        break
    elif x==1 :
        n=int(input('\nEnter the number of instances u want to create : '))
        
        create_Instance(n)
    elif x==2 :
        print('Running Instances are : ')
        instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            print(instance.id, instance.instance_type)
    elif x==3:
        print("Status of running instances : ")
        for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
            print(status)
    elif x==4 :
        ids = []
        instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            ids.append(instance.id)
        if len(ids)>0:
            ec2.instances.filter(InstanceIds=ids).stop()
            print("All running instances are stopped")
        a = input('Do u want to terminate the instances ?')
        if len(ids)>0 and a =='yes':
             ec2.instances.filter(InstanceIds=ids).terminate()
             print("Running instances are terminated")
            

        
        


