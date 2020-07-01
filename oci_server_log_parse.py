#!/usr/bin/python

### OCI server.log parser

# imports
import sys
from datetime import datetime
import re

# command line args
if(len(sys.argv) != 2):
    print("usage: oci_server_log_parse.py <server_log_file>")
    exit(1)

# read the file
obj_file = open(sys.argv[1],"r")

# arg initialisation 
int_counter = 0
dict_current = {}
dict_results = {}
string_timestamp = ""
string_now = str(datetime.now())

# interate through every line in the file 
for string_line in obj_file:
    string_timestamp = (string_line.split(","))[0]
    if(int_counter == 0):
        string_start = string_timestamp
    # look for transaction start messages and store the timestamp and the datasource
    obj_matches = re.search("<<<  Start Transaction.*originId\:[0-9]+\(([a-zA-Z0-9\-\_]+)\)",string_line)
    if(obj_matches is not None):
        string_datasource = obj_matches.group(1)
        if(string_datasource not in dict_current):
            dict_current[string_datasource] = string_timestamp
    # look for transaction end messages, calculate and store the execution time
    obj_matches = re.search(">>>  End Transaction.*originId\:[0-9]+\(([a-zA-Z0-9\-\_]+)\)",string_line)
    if(obj_matches is not None):
        string_datasource = obj_matches.group(1)
        if(string_datasource in dict_current):
            datetime_first = datetime.strptime(dict_current[string_datasource],"%Y-%m-%d %H:%M:%S")
            datetime_second = datetime.strptime(string_timestamp,"%Y-%m-%d %H:%M:%S")
            int_seconds = (datetime_second - datetime_first).seconds
            if(string_datasource in dict_results):
                dict_results[string_datasource] = dict_results[string_datasource] + "\t"+str(int_seconds)
            else:
                dict_results[string_datasource] = str(int_seconds)
            del dict_current[string_datasource]
    int_counter += 1
string_end = string_timestamp

# print timing information
print("execution timestamp: "+string_now)
print("log start timestamp: "+string_start)
print("log end timestamp:   "+string_end)
print("")

# print the results dictionary using casefold order of keys
list_keys = sorted(dict_results.keys(),key=str.casefold)
for string_key in list_keys:
    print(string_key+"\t"+dict_results[string_key])

