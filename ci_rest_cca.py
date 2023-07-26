#!/usr/bin/python
import requests
import json

au_fields = "id,uuid,ip,status,mappedStatus,statusMessage,type,publicKeyHash,os,certRevoked,tenantId,opStatus,upgradeType"
dc_fields = "id,dsTypeId,vendorModelId,vendor,model,foundationIp,type"
user_fields = "id,email"
monitor_group_fields = "id,groupType,created"
monitor_fields = "id,description,status,objectType,expression,created,monitorType,correctiveActions,resolutionExpression,resolutionType"
api_key = "REDACTED"
tenant_header = {"X-CloudInsights-ApiKey" : api_key}
tenant_url = "REDACTED"

print("***** ACQUISITION UNITS *****\n")
request_url = tenant_url+"rest/v1/au/acquisitionUnits"
response = requests.get(request_url,headers=tenant_header)
for au in response.json():
   print("Acquisition Unit: " + au["name"])
   for au_field in au_fields.split(","):
      if au_field in au:   
         print(au_field + ": " + str(au[au_field]))
   print("\n")

print("***** DATA COLLECTORS *****\n")
request_url = tenant_url+"rest/v1/collector/datasources"
response = requests.get(request_url,headers=tenant_header)
print(json.dumps(response.json(), indent=1))
for dc in response.json():
   print("Data Collector: " + dc["name"])
   for dc_field in dc_fields.split(","):
      if dc_field in dc:
         print(dc_field + ": " + str(dc[dc_field]))
   print("\n")   

print("***** USERS *****\n")
request_url = tenant_url+"rest/v1/users"
response = requests.get(request_url,headers=tenant_header)
for user in response.json()["users"]:
   print("User: " + user["name"])
   for user_field in user_fields.split(","):
      if user_field in user:
         print(user_field + ": " + str(user[user_field]))
   print("ApplicationRoles: " + json.dumps(user["applicationRoles"]))       
   print("\n")

print("***** MONITOR GROUPS *****\n")
request_url = tenant_url+"rest/v1/monitors/groups"
response = requests.get(request_url,headers=tenant_header)
for group in response.json():
   print("Monitor Group: " + group["name"])
   for monitor_group_field in monitor_group_fields.split(","):
      if monitor_group_field in group:
         print(monitor_group_field + ": " + str(group[monitor_group_field]))
   print("\n")

print("***** MONITORS *****\n")
request_url = tenant_url+"rest/v1/monitors/monitors"
response = requests.get(request_url,headers=tenant_header)
for monitor in response.json():
   print("Monitor: " + monitor["name"])
   for monitor_field in monitor_fields.split(","):
      if monitor_field in monitor:
         print(monitor_field + ": " + str(monitor[monitor_field]))
   print("Filters: " + json.dumps(monitor["filters"])) 
   print("Conditions: " + json.dumps(monitor["conditions"]))
   print("ResolutionConditions: " + json.dumps(monitor["resolutionConditions"]))
   print("GroupBy: " + json.dumps(monitor["groupBy"]))
   print("\n")

