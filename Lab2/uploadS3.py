import boto3

s3=boto3.client('s3')

filename='sample.txt'
bucketName='bucket191998'

#to upload
s3.upload_file(filename,bucketName,fileName)







