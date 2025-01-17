# logtweak
Logtweak is a Python utility that polls log files on a system for new lines, applies a custom-defined 'tweak' function to the string output, and then appends the output to a new file location.

The format of the config.ini file is as follows:
```
[name-of-custom-tweak]
fn_path = /path/to/py/file/containing/custom/tweak/function
src_log = /path/to/src/log/file
dst_log = /path/to/dst/log/file
```

The Python code in the file referenced by fn_path must start with the line...

`def tweak_fn_template(loglines):`

...  and inside this function you define how to parse the array of new log entries form the src_log file that is passwed to the function by the loglines argument. You must return a string pucntuated with newline characters. The code in your fn_path file is loaded at runtime after being leared about in the config.ini file. 

An `install.sh` file has been provided to install all the files into the `/opt/logtweak` directory and to create, enable, and start a new systemd service called logtweak.service.

Two example fn_path files have been provided:
* tweak-fn-001.py: This parses a NetApp BXP Connector log file for the ds_occmauth_1 container to a one-line format, removing all non-human logon events
* tweak-fn-002.py: This parses a NetApp BXP DataSense log file for the ds_nginx_1 container removing all non-human events

In the example config.ini file, these two fn_path files have been mapped to the tweak_fn_001 and tweak_fn_002 sections respectively, with the tweak_fn_002 section commented-out. 
