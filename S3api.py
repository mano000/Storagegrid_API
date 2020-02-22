
import json
import boto3
import boto3.session
from botocore.errorfactory import ClientError
import random
import string
from global_secrets import grid_endpoint, s3_access_key,s3_secret_key


#Set the endpoint and generate a unique bucket name
endpoint = grid_endpoint()

access_key = s3_access_key()
secret_key = s3_secret_key()



#bucket_name = 'tmp-bucket-' + ''.join([random.choice(string.ascii_lowercase) for i in range(4)])
bucket_name = 'public-bucket6'
print("Using bucket: " + bucket_name)




#Do not use the example below in production - disabling SSL verification is discouraged!
#When using a self-signed certificate, make sure to pass it into the constructor:
#s3 = session.resource(service_name='s3', endpoint_url=endpoint, verify='server_cert.pem')

session = boto3.session.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
s3 = session.resource(service_name='s3', endpoint_url=endpoint, verify=True)
client = s3.meta.client

#Create new bucket for S3 accoununt
bucket = s3.Bucket(bucket_name)
bucket.create()


#List all buckets for S3 account
bucket.wait_until_exists()
for bucket in s3.buckets.all():
    print(bucket.name)
#Enable bucket versioning


bucket.Versioning().enable()


print (bucket.Versioning().status)

policy = {
    "Statement": [
        {
            "Sid":"AddPerm",
            "Effect":"Allow",
            "Principal": "*",
            "Action":["s3:ListBucket"],
            "Resource":["urn:sgws:s3:::" + bucket.name]
        }
    ]
}

bucket.Policy().put(Policy=json.dumps(policy))

#Put a new object to a bucket
obj = s3.Object(bucket.name, 'my-key')
obj.put(Body='This is my object\'s data',
        Metadata={'customerid': '1234', 'location': 'Madrid'},
        ServerSideEncryption='AES256')

#Copy an existing object
obj.wait_until_exists()
copied_obj = s3.Object(bucket.name, 'my-copied-key')
copied_obj.copy_from(CopySource={ 'Bucket': obj.bucket_name, 'Key': obj.key })

#get object from bucket

response = obj.get()
data = response['Body'].read()
metadata = response['Metadata']
print("Data: %s // Metadata: %s" % (data, metadata))

#list all objects in a bucket:

for obj in bucket.objects.all():
    print(obj.key)

#cors = bucket.Cors()
#Doing some test with head operation.

s3 = boto3.client('s3',endpoint_url=endpoint)
try:
    print(s3.head_object(Bucket='public-bucket6', Key='my-key'))
except ClientError:
    # Not found
    print ("Error key not found!")
    pass
#delete all objects
for obj in bucket.object_versions.all():
    obj.delete()
#Finally delete the bucket:

#bucket.delete()
