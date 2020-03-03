
from sgwsapi import create_new_bucket,get_tenant_token, get_tenant_by_name, get_auth_token,create_new_tenant_user_group, create_new_tenant_user_group_noS3access
import json
import os
import getpass


# Get environment variables
# SSO username and password with admin rights

api_url = ''
api_user = os.getenv('USER')
api_passwd= ''
tenant_id=''


#Authenticate on the grid
api_passwd = getpass.getpass(api_user+" Enter your password:")

auth_token=get_auth_token(api_user,api_passwd).json()["data"]


#Search for the tenant_id
tenant_name= raw_input("Please enter the tenant name: ")

tenant_id=get_tenant_by_name(auth_token,tenant_name)


print ("The tenant id is "+tenant_id)


#Authenticate against specific tenant:

resp = get_tenant_token(api_user,api_passwd,tenant_id)

if resp.status_code != 200:
    raise Exception('POST /authorize/ {}'.format(resp.status_code) + " Error: "+resp.json()["message"]["text"] )

print('Auth Token for tenant {}'.format(resp.json()["data"]))
auth_token_tenant=resp.json()["data"]


#
bucket_name= raw_input ("Please enter the bucket name: ")

region= raw_input ("please enter the region name(eu-kau-1, us-east-1, us-west-1): ")


#Call create_new_bucket

respo=create_new_bucket(auth_token_tenant,bucket_name,region)


if respo.status_code == 201:
    print (json.dumps(respo.json(), indent=1))
else:

    print (json.dumps(respo.json(), indent=1))
    raise Exception('POST /api/v3/org/container {}'.format(respo.status_code))

#Add the group to the tenant with the desired bucket policy :

group_name= raw_input("Please enter the admin group name: ")

respo=create_new_tenant_user_group(auth_token_tenant,group_name,bucket_name)


if respo.status_code == 201:
    print (json.dumps(respo.json(), indent=1))
else:

    print (json.dumps(respo.json(), indent=1))
    raise Exception('POST /api/v3/org/groups {}'.format(respo.status_code))

users_group_name=raw_input("Please enter the users group name with no S3 access: ")

response=create_new_tenant_user_group_noS3access(auth_token_tenant,users_group_name,bucket_name)

if response.status_code == 201:
    print (json.dumps(response.json(), indent=1))
else:

    print (json.dumps(response.json(), indent=1))
    raise Exception('POST /api/v3/org/groups {}'.format(response.status_code))
