import boto.ec2.autoscale

from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.cloudwatch import MetricAlarm
from boto.ec2.autoscale import ScalingPolicy
import boto.ec2.cloudwatch

access_key_id='';
secret_access_key='';


REGION = 'us-east-2'
AMI = ''
TYPE = 't2.micro'
KEYNAME = ''
SECURITY = 'Lab2'
Data = '''
#! /bin/bash

yum update -y
yum install awscli
amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
yum install -y httpd mariadb-server
systemctl start httpd
systemctl enable httpd
usermode -a -G apache ec2-user
chown -R ec2-user:apache /var/www
chmod 2775 /var/www
find /var/www -type d -exec chmod 2775 {} \;
find /var/www -type f -exec chmod 0664 {} \;

'''
#Command to copy a file from local machine to ec2 instance
'''

'''


print('\nConneting to ec2 autoscale\n')
conn=boto.ec2.autoscale.connect_to_region(region_name=REGION,aws_access_key_id=access_key_id,
                                          aws_secret_access_key=secret_access_key)


print('\nCreating launch configuration\n')

launch=LaunchConfiguration(name="LAB4",image_id=AMI,key_name=KEYNAME,instance_type=TYPE,
                           security_groups=[SECURITY],user_data=Data,instance_monitoring=True)

conn.create_launch_configuration(launch)

asg=AutoScalingGroup(group_name="My_AutoScaling_Group",availability_zones=['us-east-2a'],
                     launch_config=launch,min_size=1,max_size=2,connection=conn)

conn.create_auto_scaling_group(asg)

print('\nCreating scaling policies\n')

scalingUpPolicy = ScalingPolicy(name='ScalingUpPolicy',
                                adjustment_type='ChangeInCapacity',
                                as_name=asg.name,
                                scaling_adjustment=1,
                                cooldown=180)

scalingDownPolicy = ScalingPolicy(name='ScalingDownPolicy',
                                  adjustment_type='ChangeInCapacity',
                                  as_name=asg.name,
                                  scaling_adjustment=-1,
                                  cooldown=180)

conn.create_scaling_policy(scalingUpPolicy)
conn.create_scaling_policy(scalingDownPolicy)

scalingUpPolicy = conn.get_all_policies(as_group='My_AutoScaling_Group', policy_names=['ScalingUpPolicy'])[0]

scalingDownPolicy = conn.get_all_policies(as_group='My_AutoScaling_Group', policy_names=['ScalingDownPolicy'])[0]

print('\nCreating cloudwatch alarm\n')

cloudwatch = boto.ec2.cloudwatch.connect_to_region(REGION,
                                                   aws_access_key_id=access_key_id,
                                                   aws_secret_access_key=secret_access_key)

alarm_dimensions={'AutoScalingGroupName':'My_AutoScaling_Group'}

scale_up_alarm = MetricAlarm(
    name='scale_up_on_cpu',namespace = 'AWS/EC2',
    metric='CPUUtilization', statistic = 'Average',
    comparison='>',threshold='80',
    period='60',evaluation_periods=2,
    alarm_actions=[scalingUpPolicy.policy_arn],
    dimensions=alarm_dimensions)

cloudwatch.create_alarm(scale_up_alarm)

scale_down_alarm = MetricAlarm(
    name='scale_down_on_cpu',namespace='AWS/EC2',
    metric='CPUUtilization',statistic='Average',
    comparison='<',threshold='30',
    period = '60',evaluation_periods=2,
    alarm_actions=[scalingDownPolicy.policy_arn],
    dimensions=alarm_dimensions)

cloudwatch.create_alarm(scale_down_alarm)


print('\nDONE\n')
#to delete autoscale group
''' asg.shutdown_instances()
    asg.delete()'''

#to delete launch configuration
''' launch.delete()'''
    
    




