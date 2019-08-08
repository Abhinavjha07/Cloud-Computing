import boto3
import time
'''
To create a security group
    ec2 = boto3.client('ec2')
    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId','')

    try:
        response = ec2.create_security_group(GroupName='Lab2',Description='Open HTTP',VpcId=vpc_id)

        security_group_id = response['GroupId']
        print('Security group created %s in vpc %s' %(security_group_id,vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId = security_group_id,
            IpPermissions = [
                {
                    'IpProtocol' : 'tcp',
                    'FromPort':80,
                    'ToPort':80,
                    'IpRanges': [{'CidrIp':'0.0.0.0/0'}]}
                ])

        print('Ingress Sucessfully Set %s' % data)
    except ClientError as e :
        print(e)
'''

# To launch new instance

ec2 = boto3.resource('ec2',region_name="us-east-2")

user_data_script = """
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
aws s3 cp s3://bucket191998/index.html /var/www/html/
aws s3 cp s3://bucket191998/error.html /var/www/html/

"""

new_instance = ec2.create_instances(
    ImageId= '',
    MinCount = 1,
    MaxCount= 1,
    InstanceType = 't2.micro',
    SecurityGroups = ['Lab2'],
    KeyName = "",
    UserData = user_data_script
    )


print('New Instance created.')



instance = new_instance[0]
instance.create_tags(Tags=[{'Key':'Name','Value':"LAB2"}])

while instance.state['Name'] not in ('running','stopped'):
    time.sleep(10)
    print("Instance state is: %s" % instance.state)
    instance.load()

if instance.state['Name'] == 'running':
    print("\nInstance is now running and instance details are:")
    print("Instance Size:" + str(instance.instance_type))
    print("Instance State:" + str(instance.state))
    print("Instance Launch Time:" + str(instance.launch_time))
    print("Instance Public DNS:" + str(instance.public_dns_name))
    print("Instance Private DNS:" + str(instance.private_dns_name))
    print("Instance Public IP:" + str(instance.public_ip_address))
    print("Instance Private IP:" + str(instance.private_ip_address))
    
    
