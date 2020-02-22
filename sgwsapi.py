import requests
import urllib3
import json
from global_secrets import api_get_url,api_default_group


#Disable warning if not using certificate:

verify=False
if verify !=True :
    urllib3.disable_warnings()


def _url(path):
    url=api_get_url()
    
    return url + path


#Operations on authorization

#Authenticate:
def get_auth_token(username, password):

    auth_json={
        "username": username,
        "password": password ,
        "cookie": "true",
        "csrfToken": "false"
    }
    return requests.post(_url('/api/v3/authorize'), json=auth_json, verify=verify)


def get_csrf_token (username, password):

    auth_json={
        "username": username,
        "password": password ,
        "cookie": "true",
        "csrfToken": "true"
    }
    return requests.post(_url('/api/v3/authorize'), json=auth_json, verify=verify)



#Operations at tenant level:

#Get tenants accounts

def get_tenants_accounts(authtoken):

    headers={'Authorization': 'Bearer ' + authtoken }
    return requests.get (_url('/api/v3/grid/accounts?limit=250'), headers=headers , verify=verify)


#Gets the storage usage information for the Storage Tenant Account

def get_storage_usage_in_tenant(tenant_id, authtoken):

    headers={'Authorization': 'Bearer ' + authtoken }
    return requests.get (_url('/api/v3/grid/accounts/{}/usage'.format(tenant_id)), headers=headers , verify=verify)


#Creates a new Storage Tenant Account

def create_new_tenant(authtoken, account_name,quota,root_password):
    #headers={'X-Csrf-Token':'' + authtoken }
    headers={'Authorization': 'Bearer ' + authtoken }
   
    data_json= "{ \"name\":\""+ account_name +"\",\"capabilities\": [\"management\",\"s3\" ],\"policy\": {\"useAccountIdentitySource\": false,\"allowPlatformServices\": false,\"quotaObjectBytes\":"+ str(quota) +"},\"password\": \""+ root_password +"\",\"grantRootAccessToGroup\":\""+ api_default_group()+"\"}"
    
    data=json.loads(data_json)
   
    return requests.post(_url('/api/v3/grid/accounts'), json=data, headers=headers, verify=verify)



#Operations on alarms:

def get_alarms(authtoken):
    headers={'Authorization': 'Bearer ' + authtoken }
    return requests.get(_url('/api/v3/grid/alarms'), headers=headers, verify=verify)


def get_health(authtoken):
    headers={'Authorization': 'Bearer ' + authtoken }
    return requests.get(_url('/api/v3/grid/health'), headers=headers, verify=verify)

def get_health_topology(authtoken):
    headers={'Authorization': 'Bearer ' + authtoken }
    return requests.get(_url('/api/v3/grid/health/topology'), headers=headers, verify=verify)


#Operations on Users 


#Lists Grid Administrator Users

def get_admin_users(authtoken):
    headers={'Authorization': 'Bearer ' + authtoken }
    return requests.get(_url('/api/v3/grid/users'), headers=headers, verify=verify)

    #operations on tenants... needs a X-Csrf-Token
def get_usage(csrf_authtoken):
    headers={'Authorization': 'Bearer ' + csrf_authtoken }
    return requests.get(_url('/api/v3/org/usage'), headers=headers, verify=verify)

    

################################################################
#Inside a  Tenant
############TO BE IMPLEMENTED##################################

def create_new_tenant_user_group(csrf_authtoken):
    #/org/groups   Creates a new Tenant User Group
    headers={'Authorization': 'Bearer ' + csrf_authtoken }
    body={
                "displayName": "Developers",
                    "policies": {
                    "management": {
                    "manageAllContainers": "false",
                    "manageEndpoints": "false",
                    "manageOwnS3Credentials": "true",
                    "rootAccess": "false"
              },
                "s3": {
                    "Id": "123456",
                    "Version": "2015-09-08",
                "Statement": [
                        {
                            "Sid": "string",
                            "Effect": "Allow",
                            "Action": "s3:GetObject",
                            "NotAction": "s3:GetObject",
                            "Resource": [
                                "arn:aws:s3:::mybucket/myobject"
                            ],
                            "NotResource": [
                                "arn:aws:s3:::mybucket/myobject"
                            ],
                "Condition": {
                    "condition_type": {
                    "condition_key": "condition_value"
                            }
                        }
                    }
                    ]                     
                       }
                     },
                    "uniqueName": "federated-group/developers"
                }

                

def create_new_bucket(csrf_authtoken,bucket_name, region):
    #/org/containers
    #Create a bucket for an S3 tenant account
    data=   {
            "name": bucket_name,
            "region": region,
            "compliance": {
                "autoDelete": "false",
                "legalHold": "false",
                "retentionPeriodMinutes": 2629800
            }
    }

###################TO BE IMPLEMENTED##################333

