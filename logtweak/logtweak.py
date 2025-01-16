#!/usr/bin/python

import os
import time
import re
import configparser

# used to store all of the relevant information for a log tweak
class tweaker:
    def __init__(self,src,dst,name,tweak_fn):
        self.src_log = src          # path of the source log file
        self.dst_log = dst          # path where the tweaked log entries get written to
        self.name = __name__        # name of the tweak (must be unique)
        self.tweak_fn = tweak_fn    # name of the function for this tweak (must be unique)
        self.fh = ""                # persistent file handle for the src_log

# globals
tweak_list = []
config = configparser.ConfigParser()

#####
# simple function to loop forever
def loop_forever():

    # open all the src files and store the file handle in the tweak_list
    for tweak in tweak_list:
        tweak.fh = open(tweak.src_log, "r")
        tweak.fh.seek(0,2)

    # forever
    while True:

        # iterate through each tweak
        for tweak in tweak_list:

            # work out if the end location of the file has changed since last iteration
            fh_before = tweak.fh.tell()
            tweak.fh.seek(0,2)

            # if it has changed store the new end location, run the tweak function, and write the tweaked logs
            if fh_before != tweak.fh.tell():
                tweak.fh.seek(fh_before)
                logstring = tweak.fh.read()
                loglines = logstring.split("\n")
                result = eval(tweak.tweak_fn)
                dst_fh = open(tweak.dst_log, "a")
                dst_fh.write(str(result))
                dst_fh.close()

        # sleep before the next iteration
        time.sleep(int(config["general"]["sleep"]))

#####
# todo: signal handling
# todo: log rotation

#####
# main
if __name__ == "__main__":

    # todo: do we need any command line argument parsing?

    # read config file    
    config.read('config.ini')

    # todo: lots of checking of the config file

    # iterate through the scetions in the config file and populate the tweak_list
    for section in config.sections():
        if section != "general":    # ignore the general section
            # read in the python code for this tweak function
            file = open(config[section]["fn_path"], "r")
            tweak_code = file.read()
            file.close()
            # rename the tweak function 
            tweak_code = re.sub('def tweak_fn_template', "def parse_%s" % section, tweak_code)
            # load the code to define the tweak function
            exec(tweak_code)
            # store all the relevant information in the tweak_list for later
            tweak_list.append(tweaker(config[section]["src_log"],config[section]["dst_log"],section,"parse_%s(loglines)" % section))

    # forever
    loop_forever()
    
