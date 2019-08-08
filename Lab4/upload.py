import boto3

s3 = boto3.client('s3')

website_config = {
    'ErrorDocument' : {'Key':'error.html'},
    'IndexDocument' : {'Suffix':'homepage.html'}
    }

s3.put_bucket_website(
    Bucket = '',
    WebsiteConfiguration = website_config
    )

bucket = ''

files = ('homepage.html','Error.html','About.html','kinds.html','Types.html')

for x in files:
    s3.upload_file(x,bucket,x,ExtraArgs={'ACL':'public-read','ContentType':'text/html'})
