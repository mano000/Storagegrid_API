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


def get_tenant_token (username, password, accountId):

    auth_json={
        "accountId": accountId,
        "username": username,
        "password": password ,
        "cookie": "true",
        "csrfToken": "false"
    }
    return requests.post(_url('/api/v3/authorize'), json=auth_json, verify=verify)



#Operations at tenant level:

#Get tenants accounts

def get_tenants_accounts(authtoken):

    headers={'Authorization': 'Bearer ' + authtoken }
    return requests.get (_url('/api/v3/grid/accounts?limit=250'), headers=headers , verify=verify)


def get_tenant_by_name (authtoken, tenant_name):
    #Returns the tenant id that match the name
    query=get_tenants_accounts(authtoken)
    for items in query.json()['data']:
        if items['name']==tenant_name:
            return items['id']
       





#Gets the storage usage information for the Storage Tenant Account

def get_storage_usage_in_tenant(tenant_id, authtoken):

    headers={'Authorization': 'Bearer ' + authtoken }
    return requests.get (_url('/api/v3/grid/accounts/{}/usage'.format(tenant_id)), headers=headers , verify=verify)


#Creates a new Storage Tenant Account

def create_new_tenant(authtoken, account_name,quota,root_password):
   
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
def get_usage(tenant_authtoken):
    headers={'Authorization': 'Bearer ' + tenant_authtoken }
    return requests.get(_url('/api/v3/org/usage'), headers=headers, verify=verify)

    


#Inside a  Tenant


def create_new_tenant_user_group(tenant_authtoken, group_name, bucket_name):
    
    #/org/groups   Creates a new Tenant User Group only with access to a specific bucket.
    #This group can operate over the bucket but not over the tenant, and can generate S3 keys.

    headers={'Authorization': 'Bearer ' + tenant_authtoken }
    body={
                "displayName": group_name,
                "policies": {
                    "management": { 
                    "manageAllContainers": False,
                    "manageEndpoints": False,
                    "manageOwnS3Credentials": True,
                    "rootAccess": False },
                    "s3": {
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Action": "s3:*",
                                    "Resource": [
                                        "arn:aws:s3:::"+bucket_name,
                                        "arn:aws:s3:::"+bucket_name+"/*"
                                    ],
                            }
                                ]                     
                            }
                        },
                "uniqueName": "federated-group/"+group_name
                }

    data=body
    #For debug:
    print (json.dumps(data, indent=1))
    

    
    return requests.post(_url('/api/v3/org/groups'), json=data, headers=headers, verify=verify)

def create_new_tenant_user_group_noS3access(tenant_authtoken, group_name, bucket_name):
    
    #/org/groups   Creates a new Tenant User Group only with access to a specific bucket.
    #This group can operate over the bucket but not over the tenant, and can generate S3 keys.

    headers={'Authorization': 'Bearer ' + tenant_authtoken }
    body={
                "displayName": group_name,
                "policies": {
                    "management": { 
                    "manageAllContainers": False,
                    "manageEndpoints": False,
                    "manageOwnS3Credentials": True,
                    "rootAccess": False }
                        },
                "uniqueName": "federated-group/"+group_name
                }

    data=body
    #For debug:
    print (json.dumps(data, indent=1))
    

    
    return requests.post(_url('/api/v3/org/groups'), json=data, headers=headers, verify=verify)
                

def create_new_bucket(tenant_authtoken,bucket_name, region):
    #/org/containers
    #Create a bucket for an S3 tenant account
    headers={'Authorization': 'Bearer ' + tenant_authtoken }
    data={
            "name": bucket_name,
            "region": region,
           
    }
    #For debug:
    print (json.dumps(data, indent=1))

    return requests.post(_url('/api/v3/org/containers'), json=data, headers=headers, verify=verify)

#/org/containers/{bucketName}/last-access-time

#Determines if LAT is enable on a bucket
def get_last_access_time(tenant_authtoken,bucket_name):
     headers={'Authorization': 'Bearer ' + tenant_authtoken }
     return requests.get (_url('/api/v3/org/containers/{}/last-access-time'.format(bucket_name)), headers=headers , verify=verify)


