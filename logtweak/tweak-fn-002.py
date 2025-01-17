def tweak_fn_template(loglines):
    current_log = ""
    for i in range(len(loglines)):
        line = loglines[i]
        if re.search('GET /health', line) is None \
               and re.search('GET /upgrade', line) is None\
               and re.search('GET /api/v1\.36/license_info', line) is None \
               and re.search('GET /api/v1\.36/working_environment\?filter_not_in_scope_environments=false', line) is None:
            m = re.search('\{(.*)\}\s*$', line)
            if m is not None: 
                current_log += line.split(" ")[0]
                payload = m.group(1).split(",")
                current_log += " " + payload[3].split(":")[1]
                current_log += " " + payload[1].split(":")[1]
                current_log += " " + payload[2].split(":")[0]
                current_log += " " + re.sub('\"', '', payload[4].split(":")[1])
            current_log += "\n"
    return(current_log)

