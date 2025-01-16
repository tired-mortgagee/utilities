def tweak_fn_template(loglines):
    flag = 0
    current_log = "" 
    for i in range(len(loglines)):        
        if "\"method\": \"POST\"" in loglines[i] and i + 2 < len(loglines) and flag == 0:
            if "\"url\": \"/oauth/token\"" in loglines[i+1]:
                if "\"hostname\": \"occmauth:8420\"" not in loglines[i+2]:
                    current_log += loglines[i].split(" ")[0] + " /oauth/token "
                    current_log += (re.split('[\s,]+',loglines[i+2],maxsplit=0,flags=0))[4] + " "
                    flag = 1
        if "`User`.`email`" in loglines[i] and flag == 1:
            m = re.search('`User`\.`email` = \'([a-zA-Z0-9_@\.\!\#\$\%\&\*\+\-\/\=\?\^\`\{\|\}\~]+)\'', loglines[i])
            if m is not None:
                current_log += m.group(1) + " "
                flag = 2
            else:
                current_log = "ERROR PARSING LOG (A001)"
                current_log += "\n"
                flag = 0
        if "\"statusCode\":" in loglines[i] and flag == 2:
            m = re.search('\"statusCode\": ([0-9]+)', loglines[i])
            if m is not None:
                current_log += m.group(1)
            else:
                current_log = "ERROR PARSING LOG (A002)"
            current_log += "\n"
            flag = 0
    return(current_log)
