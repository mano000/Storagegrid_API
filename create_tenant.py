from sgwsapi import *
import json
import os
import getpass

#Main program:
# Get environment variables
# SSO username and password with admin rights

api_url = ''
api_user = os.getenv('USER')
api_passwd= ""


api_passwd = getpass.getpass(api_user+" Enter your password:")


#Get auth token:


resp = get_auth_token(api_user,api_passwd)
if resp.status_code != 200:
   raise Exception('POST /authorize/ {}'.format(resp.status_code) + " Error: "+resp.json()["message"]["text"] )

print('Auth Token {}'.format(resp.json()["data"]))
auth_token=resp.json()["data"]



response = get_tenants_accounts(auth_token)



#Let's create a new test tenant.


respo= create_new_tenant(auth_token,'Mariano_test2',100000000,'qwerty123456')

#if respo.status_code != 201:
    #print (respo).json()['message']
    #print (respo).json()['errors']
print (json.dumps(respo.json(), indent=1))
   # raise Exception('POST /create new tenant {}'.format(respo.status_code))

