import boto3
cluster_name = 'my_cluster'
service_name = 'Lab6_Service'
task_name = "hello_world"

ecs_client=boto3.client('ecs')
ec2_client = boto3.client('ec2')

#create cluster
print('Creating cluster ')
response = ecs_client.create_cluster(clusterName=cluster_name)

print(response)

print('\n\n')
#create ec2 instance
print('Container Instance ')
response = ec2_client.run_instances(
    ImageId = "",
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
     IamInstanceProfile={
        "Name": "Lab"
        },
    SecurityGroups = ['default'],
    KeyName='',
    UserData = "#!/bin/bash \n echo ECS_CLUSTER ="+cluster_name+ " >> /etc/ecs/ecs.config",
   
)

print(response)

print('\n\nTask Definition ')
#create a task definition
ec2=boto3.resource('ec2')
response = ecs_client.register_task_definition(
    containerDefinitions = [
        {
            "name" : "wordpress",
            "links" : [
                "mysql"
                ],
            "image" : "wordpress",
            "essential":True,
            "portMappings": [
                {
                    "containerPort" : 80,
                    "hostPort" : 80
                    }
                ],
            "memory" : 300,
            "cpu":10
            },
        {
            "environment" : [
                {
                    "name" : "",
                    "value" : ""
                    }
                ],
            "name": "mysql",
            "image": "mysql",
            "cpu":10,
            "memory":300,
            "essential":True
            }
        ],
    family = "hello_world"
    )


print(response)

print('\n\nCreating Service ')

response = ecs_client.create_service(
    cluster = cluster_name,
    serviceName = service_name,
    loadBalancers=[
        {
            'targetGroupArn': 'arn:aws:elasticloadbalancing:us-east-2:022173025504:targetgroup/my-target-group/db36b68044d3b328',
            
            'containerName': 'wordpress',
            'containerPort': 80
        },
    ],
    taskDefinition=task_name,
    desiredCount=4,
    clientToken='request_identifier_string',
    deploymentConfiguration={
        'maximumPercent':200,
        'minimumHealthyPercent':50
        }
    )

print(response)
print('\n\n')


def lambda_handler():#event, context):
    # create filter for instances in running state
    filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    # filter the instances based on filters() above
    instances = ec2.instances.filter(Filters=filters)
    # instantiate empty array
    RunningInstances = []

    for instance in instances:
        # for each instance, append to array and print instance id
        RunningInstances.append(instance.id)
        print('Cluster Instance - ')
        print(instance.id)
    ec2.instances.filter(InstanceIds=RunningInstances).terminate()


def terminate_ecs() :
    try:
        response = ecs_client.update_service(
            cluster=cluster_name,
            service=service_name,
            desiredCount=0
            )

        #delete service
        response = ecs_client.delete_service(
            cluster=cluster_name,
            service = service_name
            )
        print(response)
        print('\n\n')
    except:
        print('Sevice not found/not active')

    response = ecs_client.list_task_definitions(
        familyPrefix = task_name,
        status = 'ACTIVE'
        )
    #print('********',response)
    #deregister all task definitions
    for task_definition in response["taskDefinitionArns"]:
        deregister_response=ecs_client.deregister_task_definition(
            taskDefinition = task_definition
            )
        print(deregister_response)
        print('\n\n')

    #terminate vm's
    response = ecs_client.list_container_instances(
         cluster=cluster_name
        )
    #print('*****',response)
    if response["containerInstanceArns"]:
        container_instance_resp = ecs_client.describe_container_instances(
            cluster=cluster_name,
            containerInstances=response["containerInstanceArns"]
            )

        #print('******',container_instance_resp)
        for ec2_instnace in container_instance_resp["containerInstances"]:
            ec2_termination_resp = ec2_client.terminate_instances(
                DryRun=False,
                InstanceIds=[
                    ec2_instance["ec2InstanceId"],
                    ]
                )
    lambda_handler()
    #delete cluster
    response = ecs_client.delete_cluster(
        cluster = cluster_name
        )

    print(response)
    print('\n\n')
    
        

c=input('Do u want to terminate : Enter y/n ')

if c=='y':
    terminate_ecs()
            
    
