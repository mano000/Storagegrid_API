import os
import boto3
import s3fs

fs = s3fs.S3FileSystem(
    anon=False, 
    profile_name='default', # Use credentials from the [RSIROSS] section of ~/.aws/credentials 
    client_kwargs={'endpoint_url': 'https://ross.science.roche.com'} # Set endpoint URL to ROSS
)



bucket = 'storagegrid-training'

test = fs.ls(bucket) # List files in a bucket

print (test)


filename= "test1.txt"


print filename

result = fs.put(filename,bucket + "/" + filename)
print result
