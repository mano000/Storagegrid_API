from sgwsapi import create_new_bucket,get_tenant_token
from global_secrets import tenant_account_for_test
import json
import os
import getpass

# Get environment variables
# SSO username and password with admin rights

api_url = ''
api_user = os.getenv('USER')
api_passwd= ""

tenant_id= tenant_account_for_test()

api_passwd = getpass.getpass(api_user+" Enter your password:")


#Authenticate against specific tenant:

resp = get_tenant_token(api_user,api_passwd,tenant_id)




if resp.status_code != 200:
    raise Exception('POST /authorize/ {}'.format(resp.status_code) + " Error: "+resp.json()["message"]["text"] )

print('Auth Token for tenant {}'.format(resp.json()["data"]))
auth_token_tenant=resp.json()["data"]




#Call create_new_bucket

respo=create_new_bucket(auth_token_tenant,"testbucket-api","us-east-1")


if respo.status_code == 201:
    print (json.dumps(respo.json(), indent=1))
else:

    print (json.dumps(respo.json(), indent=1))
    raise Exception('POST /api/v3/org/container {}'.format(respo.status_code))
