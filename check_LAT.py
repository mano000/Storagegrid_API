
from sgwsapi import *
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

#Get the list of accounts"

response = get_tenants_accounts(auth_token)

if response.status_code != 200:
    raise Exception('POST //api/v3/grid/accounts?limit=25 {}'.format(response.status_code) + " Error: "+response.json()["message"]["text"] )

#For each tenant account get the bucket usage:

for items in response.json()['data']:
   print('Account id: {}, account Name: {}'.format(items['id'], items['name']))
   tenantid='{}'.format(items['id'])
    #Authenticate against specific tenant:
   resp = get_tenant_token(api_user,api_passwd,tenantid)
   if resp.status_code != 200:
         #raise Exception('POST /authorize/ {}'.format(resp.status_code) + " Error: "+resp.json()["message"]["text"] )
         print ("error accesing this tenant: "+resp.json()["message"]["text"])
   else:
        print('Auth Token for tenant {}'.format(resp.json()["data"]))
        auth_token_tenant=resp.json()["data"]

        buckets_response=get_storage_usage_in_tenant( tenantid , auth_token)
        if buckets_response.status_code != 200:
                raise Exception('POST /api/v3/grid/accounts/id/usage {}'.format(buckets_response.status_code) + " Error: "+buckets_response.json()["message"]["text"] )
   
        for buckets in buckets_response.json()['data']['buckets']:
              check=get_last_access_time(auth_token_tenant,buckets['name'])
              print(buckets['name'])
              print(json.dumps(check.json()['data']))
                    
              print ("---------------------------------------------- ")



