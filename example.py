from sgwsapi import *
from global_secrets import api_get_url,api_password,api_username,api_default_group,tenant_account_for_test
import json



#This is an example of how to use the API calls:

# Get environment variables
# SSO username and password with admin rights

api_url = api_get_url()
api_user = api_username()
api_passwd= api_password()

#Get auth token:


resp = get_auth_token(api_user,api_passwd)
if resp.status_code != 200:
    raise Exception('POST /authorize/ {}'.format(resp.status_code) + " Error: "+resp.json()["message"]["text"] )

print('Auth Token {}'.format(resp.json()["data"]))
auth_token=resp.json()["data"]



# Get grid health:
print (json.dumps(get_health(auth_token).json(), indent=1))

# Get grid alarms:
print (json.dumps(get_alarms(auth_token).json(), indent=1))

# Get health topology:
print (json.dumps(get_health_topology(auth_token).json(), indent=1))

# Get list of admin users:
print (json.dumps(get_admin_users(auth_token).json(), indent=1))


#Get the list of accounts"

response = get_tenants_accounts(auth_token)

if response.status_code != 200:
    raise Exception('POST //api/v3/grid/accounts?limit=25 {}'.format(response.status_code) + " Error: "+response.json()["message"]["text"] )

#For each tenant account get the bucket usage:

for items in response.json()['data']:
   print('Account id: {}, account Name: {}'.format(items['id'], items['name']))
   tenantid='{}'.format(items['id'])
   buckets_response=get_storage_usage_in_tenant( tenantid , auth_token)
   if buckets_response.status_code != 200:
        raise Exception('POST /api/v3/grid/accounts/id/usage {}'.format(buckets_response.status_code) + " Error: "+buckets_response.json()["message"]["text"] )
   
   for buckets in buckets_response.json()['data']['buckets']:
            print('{} size: {} TB numbers of ojects:{}'.format(buckets['name'], buckets['dataBytes']/1099511627776, buckets['objectCount']))
   print ("---------------------------------------------- ")





#Get tenant auth token:


resp = get_tenant_token(api_user,api_passwd,tenant_account_for_test())
if resp.status_code != 200:
    raise Exception('POST /authorize/ {}'.format(resp.status_code) + " Error: "+resp.json()["message"]["text"] )

print('Auth Token for tenant {}'.format(resp.json()["data"]))
auth_token_tenant=resp.json()["data"]



# Get tenant space usage:
print (json.dumps(get_usage(auth_token_tenant).json(), indent=1))



