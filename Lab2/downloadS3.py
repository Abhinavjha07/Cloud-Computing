import boto3
import botocore

bucket= ''

key = 'sample.txt'

s3=boto3.resource('s3')

try:
    s3.Bucket(bucket).download_file(key,'downloaded.txt')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code']=="404":
        print("Error")
    else:
        raise
