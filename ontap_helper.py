#!/usr/bin/python

# imports
import argparse
import requests
import logging
import httplib
import json
import sys
import os
import re

# disable warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# chcek and set environment variables
os.environ['no_proxy'] = '*'
str_username = os.environ['ONTAP_USER']
str_password = os.environ['ONTAP_PASS']
if (os.environ.get('ONTAP_USER') is None):
   sys.exit("ontap_helper.py: error: Environment variable ONTAP_USER needs to be set.")
if (os.environ.get('ONTAP_PASS') is None):
   sys.exit("ontap_helper.py: error: Environment variable ONTAP_PASS needs to be set.\n" +
            "                        Enter the following commands:\n" +
            "                           export ONTAP_PASS=<password>\n" +
            "                           history -d `history | tail -n 2 | head -n 1 | awk '{print $1}'`\n")
os.environ['no_proxy'] = '*'
str_username = os.environ['ONTAP_USER']
str_password = os.environ['ONTAP_PASS']

# function ontap_version:
# run when operator uses 'version' verb
# retrieves ontap version fom the SVM
def ontap_version(in_args):
   response = requests.get("https://"+in_args.svm+"/api/cluster?fields=version", auth=(str_username, str_password), verify=False)
   print "status_code: " + str(response.status_code)
   if (response.status_code == 200):
      print (json.loads(response.content))["version"]["full"]
   else:
      print "ontap_helper.py: error: " + str(json.loads(response.content))

# function ontap_snapmirror_show:
# run when operator uses 'snapmirror_show' verb
# retrieves snapmirror relationship information fom the svm
def ontap_snapmirror_show(in_args):
   if (in_args.uuid):
      # if uuid provided, show detailed statistics
      response = requests.get("https://"+in_args.svm+"/api/snapmirror/relationships/"+in_args.uuid+"/transfers", auth=(str_username, str_password), verify=False)
      print "status_code: " + str(response.status_code)
      print "note: this shows active transfers for the relationship with uuid "+in_args.uuid
      if (response.status_code == 200):
         print response.content
      else:
         print "ontap_helper.py: error: " + str(json.loads(response.content))
   else:
      # show general statistics for all snapmirror relationships
      response = requests.get("https://"+in_args.svm+"/api/snapmirror/relationships", auth=(str_username, str_password), verify=False)
      print "status_code: " + str(response.status_code)
      if (response.status_code == 200):
         print("uuid,src_path,dst_path,healthy,state")
         for obj_record in (json.loads(response.content))["records"]:
            print str(obj_record["uuid"])+","+str(obj_record["source"]["path"])+","+ \
                  str(obj_record["destination"]["path"])+","+str(obj_record["healthy"])+","+ \
                  str(obj_record["state"])
      else:
         print "ontap_helper.py: error: " + str(json.loads(response.content))

# function ontap_snapmirror_upate:
# run when operator uses 'snapmirror_update' verb
# triggers a snapmirror update operation on the specified relationship
def ontap_snapmirror_update(in_args):
   response = requests.post("https://"+in_args.svm+"/api/snapmirror/relationships/"+in_args.uuid+"/transfers", '{}', auth=(str_username, str_password), verify=False)
   print "status_code: " + str(response.status_code)
   if (response.status_code == 200 or response.status_code == 201):
      print "update on releationship "+in_args.uuid+" commenced"
   else:
      print "ontap_helper.py: error: " + str(json.loads(response.content))

# function ontap_snapmirror_break:
# run when operator uses 'snapmirror_break' verb
# triggers a snapmirror break operation on the specified relationship
def ontap_snapmirror_break(in_args):
   response = requests.patch("https://"+in_args.svm+"/api/snapmirror/relationships/"+in_args.uuid, '{"state": "broken_off"}', auth=(str_username, str_password), verify=False)
   print "status_code: " + str(response.status_code)
   if (response.status_code == 200 or response.status_code == 201 or response.status_code == 202):
      print "break of releationship "+in_args.uuid+" complete"
   else:
      print "ontap_helper.py: error: " + str(json.loads(response.content))

# function ontap_volume_show:
# run when operator uses 'volume_show' verb
# retrieves volume information from the svm
def ontap_volume_show(in_args):
   if (in_args.uuid):
      response = requests.get("https://"+in_args.svm+"/api/storage/volumes/"+in_args.uuid, auth=(str_username, str_password), verify=False)
      print "status_code: " + str(response.status_code)
      if (response.status_code == 200):
         print response.content
      else:
         print "ontap_helper.py: error: " + str(json.loads(response.content))
   else:
      response = requests.get("https://"+in_args.svm+"/api/storage/volumes", auth=(str_username, str_password), verify=False)
      print "status_code: " + str(response.status_code)
      if (response.status_code == 200):
         print("uuid,name")
         for obj_record in (json.loads(response.content))["records"]:
            print str(obj_record["uuid"])+","+str(obj_record["name"])
      else:
         print "ontap_helper.py: error: " + str(json.loads(response.content))

# function ontap_volume_mount:
# run when operator uses 'volume_mount' verb
# triggers a volume mount operation to the specified path in the svm namespace
def ontap_volume_mount(in_args):
   response = requests.patch("https://"+in_args.svm+"/api/storage/volumes/"+in_args.uuid, '{"nas": {"path": "'+in_args.path+'"}}', auth=(str_username, str_password), verify=False)
   print "status_code: " + str(response.status_code)
   if (response.status_code == 200 or response.status_code == 201 or response.status_code == 202):
      print "mount of voume "+in_args.uuid+" to path "+in_args.path+" complete"
   else:
      print "ontap_helper.py: error: " + str(json.loads(response.content))

# function ontap_share_create:
# run when operator uses 'share_create' verb
# triggers a share creation operation to specified path in the svm namespace
def ontap_share_create(in_args):
   response = requests.post("https://"+in_args.svm+"/api/protocols/cifs/shares", '{"svm": {"name": "'+in_args.svm+'"}, "name": "'+in_args.share+'", "path": "'+in_args.path+'"}', auth=(str_usern
ame, str_password), verify=False)
   print "status_code: " + str(response.status_code)
   if (response.status_code == 200 or response.status_code == 201 or response.status_code == 202):
      print "creation of share "+in_args.share+" to path "+in_args.path+" complete"
   else:
      print "ontap_helper.py: error: " + str(json.loads(response.content))

# function ontap_share_show:
# run when operator uses 'share_show' verb
# retrieves a list of shares from the specified svm
def ontap_share_show(in_args):
   response = requests.get("https://"+in_args.svm+"/api/protocols/cifs/shares", auth=(str_username, str_password), verify=False)
   print "status_code: " + str(response.status_code)
   if (response.status_code == 200 or response.status_code == 201 or response.status_code == 202):
      print("name")
      for obj_record in (json.loads(response.content))["records"]:
         print str(obj_record["name"])
   else:
      print "ontap_helper.py: error: " + str(json.loads(response.content))

# function ontap_volume_snapshot_policy:
# run when operator uses 'volume_snapshot_policy' verb
# applies a snapshot policy to the specified volume
def ontap_volume_snapshot_policy(in_args):
   response = requests.patch("https://"+in_args.svm+"/api/storage/volumes/"+in_args.uuid, '{"snapshot_policy": "'+in_args.policy+'"}', auth=(str_username, str_password), verify=False)
   print "status_code: " + str(response.status_code)
   if (response.status_code == 200 or response.status_code == 201 or response.status_code == 202):
      print "snapshot policy "+in_args.policy+" applied to volume "+in_args.uuid
   else:
      print "ontap_helper.py: error: " + str(json.loads(response.content))

# function main:
if __name__ == "__main__":

   # instantiate argparse and set subparsers
   obj_argparser = argparse.ArgumentParser()
   obj_subparsers = obj_argparser.add_subparsers()
   #obj_subparser01 = obj_subparsers.add_parser("version")
   #obj_subparser01.add_argument("svm", help="Name of SVM to query")
   #obj_subparser01.set_defaults(func=ontap_version)
   obj_subparser02 = obj_subparsers.add_parser("snapmirror_show")
   obj_subparser02.add_argument("svm", help="Name of SVM to query")
   obj_subparser02.add_argument("uuid", help="UUID of the SnapMirror relationship", type=str, nargs='?')
   obj_subparser02.set_defaults(func=ontap_snapmirror_show)
   obj_subparser03 = obj_subparsers.add_parser("snapmirror_update")
   obj_subparser03.add_argument("svm", help="Name of SVM to query")
   obj_subparser03.add_argument("uuid", help="UUID of the SnapMirror relationship")
   obj_subparser03.set_defaults(func=ontap_snapmirror_update)
   obj_subparser04 = obj_subparsers.add_parser("snapmirror_break")
   obj_subparser04.add_argument("svm", help="Name of SVM to query")
   obj_subparser04.add_argument("uuid", help="UUID of the SnapMirror relationship")
   obj_subparser04.set_defaults(func=ontap_snapmirror_break)
   obj_subparser05 = obj_subparsers.add_parser("volume_show")
   obj_subparser05.add_argument("svm", help="Name of SVM to query")
   obj_subparser05.add_argument("uuid", help="UUID of the volume", type=str, nargs='?')
   obj_subparser05.set_defaults(func=ontap_volume_show)
   obj_subparser06 = obj_subparsers.add_parser("volume_mount")
   obj_subparser06.add_argument("svm", help="Name of SVM to query")
   obj_subparser06.add_argument("uuid", help="UUID of the volume")
   obj_subparser06.add_argument("path", help="Path in the namespace")
   obj_subparser06.set_defaults(func=ontap_volume_mount)
   obj_subparser07 = obj_subparsers.add_parser("share_create")
   obj_subparser07.add_argument("svm", help="Name of SVM to query")
   obj_subparser07.add_argument("share", help="Name of new CIFS share")
   obj_subparser07.add_argument("path", help="Path in the namespace")
   obj_subparser07.set_defaults(func=ontap_share_create)
   obj_subparser08 = obj_subparsers.add_parser("share_show")
   obj_subparser08.add_argument("svm", help="Name of SVM to query")
   obj_subparser08.set_defaults(func=ontap_share_show)
   obj_subparser09 = obj_subparsers.add_parser("volume_snapshot_policy")
   obj_subparser09.add_argument("svm", help="Name of SVM to query")
   obj_subparser09.add_argument("uuid", help="UUID of the volume")
   obj_subparser09.add_argument("policy", help="Name of snapshot policy to apply")
   obj_subparser09.set_defaults(func=ontap_volume_snapshot_policy)
   ns_args = obj_argparser.parse_args()

   # type and syntax checking on command line args
   obj_regexp = re.compile(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$|^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](\.[a-zA-Z0-9\-]{2,}){0,6}$')
   if (not(obj_regexp.match(ns_args.svm))):
      sys.exit("ontap_helper.py: error: 'svm' argument is not in a hostname or IP address format")
   obj_regexp = re.compile(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
   if (obj_regexp.match(ns_args.svm)):
      sys.exit("ontap_helper.py: error: 'svm' argument uses an IP address format, please use a hostname format and adjust /etc/hosts if required")

   # apply verb from command line
   ns_args.func(ns_args)
