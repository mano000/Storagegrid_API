from sgwsapi import create_new_tenant_user_group,get_tenant_token
from global_secrets import federated_group_for_test,tenant_account_for_test,bucket_for_test
import json
import os
import getpass

# Get environment variables
# SSO username and password with admin rights

api_url = ''
api_user = os.getenv('USER')
api_passwd= ""

tenant_id= tenant_account_for_test()
group= federated_group_for_test()
bucket= bucket_for_test()

api_passwd = getpass.getpass(api_user+" Enter your password:")


#Authenticate against specific tenant:

resp = get_tenant_token(api_user,api_passwd,tenant_id)




if resp.status_code != 200:
    raise Exception('POST /authorize/ {}'.format(resp.status_code) + " Error: "+resp.json()["message"]["text"] )

print('Auth Token for tenant {}'.format(resp.json()["data"]))
auth_token_tenant=resp.json()["data"]




#Call create_new_tenant_user_group:

respo=create_new_tenant_user_group(auth_token_tenant,group,bucket)


if respo.status_code == 201:
    print (json.dumps(respo.json(), indent=1))
else:

    print (json.dumps(respo.json(), indent=1))
    raise Exception('POST /api/v3/org/groups {}'.format(respo.status_code))
