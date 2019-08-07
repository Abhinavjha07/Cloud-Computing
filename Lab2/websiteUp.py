import boto3

s3 = boto3.client('s3')

website_configuration = {
    'ErrorDocument' : {'Key':'error.html'},
    'IndexDocument' : {'Suffix':'index.html'}
}

s3.put_bucket_website(
    Bucket='bucket191998',
    WebsiteConfiguration=website_configuration
    )
bucket_name='bucket191998'
files = ('index.html','error.html')
for x in files:
        s3.upload_file(x,bucket_name,x,ExtraArgs={'ACL':'public-read','ContentType': 'text/html'})
