#coding=utf-8

import os
import re
from datetime import datetime
from generate_report import report_creation
from archive import archive


"""
Names_Logs contain all .log files names and regex which can help us to identify importants elements
for the creation of reports
compiled_pattern change raw_strings of Names_Logs into regex objects which permit and more easy research
"""
Names_Logs = {"access_date.log": r"\[([\d -:]+)\] INFO: User (\w+) logged (\w+) from ([\d.]+)",
              "error_date.log": r"\[([\d -:]+)\] ERROR: (\w+) ([\w| ]+) on (server\d)",
              "auth_fail_date.log": r"\[([\d -:]+)\] FAILED LOGIN: ([\w ]+) for user (\w+) from ([\d.]+)",
              "server1_sys_date.log": r"\[([\d -:]+)\] WARNING: High (\w+ usage) on server1 - \w+: (\d+)%", 
              "server2_sys_date.log": r"\[([\d -:]+)\] WARNING: High (\w+ usage) on server2 - \w+: (\d+)%",
              "server3_sys_date.log": r"\[([\d -:]+)\] WARNING: High (\w+ usage) on server3 - \w+: (\d+)%",
              "backup_date.log": r"\[([\d -:]+)\] INFO: Backup (\w+) successfully on (\w+)",
              "security_date.log": r"\[([\d -:]+)\] ERROR: ([\w ]+) attempt by ([\d.]+)"}
compiled_patterns = {key: re.compile(value) for key, value in Names_Logs.items()}

"""
Names_Reports contains values which are lists of dictionary. We will use the pandas modulo for
the creation of .csv reports.
"""
Names_Reports = {"access_date.log": [],
              "error_date.log": [],
              "auth_fail_date.log": [],
              "server1_sys_date.log": [],
              "server2_sys_date.log": [],
              "server3_sys_date.log": [],
              "backup_date.log": [],
              "security_date.log": []}

def parse_log_file(log):
    """
    parse_log_file() take a .log file in parameter and return a dictionary which will be append in
    Names_Reports
    """
    logs_dir = os.path.join(os.getcwd(), "logs")  
    """logs/ creation"""
    os.makedirs(logs_dir, exist_ok=True)

    report_dir =  os.path.join(os.getcwd(),"reports") 
    """report/ creation"""
    os.makedirs(report_dir, exist_ok=True)

    """
    We change keys (file's names) and add date for repots and logs
    """
    date = str(datetime.now().date() )
    """Date of modification in our script"""

    Names_Logs_maj, Names_Reports_maj = {} , {}
    for key, value in Names_Reports.items():
        key = re.sub(r"date", date, key)
        Names_Reports_maj[key] = value
    
    for key, value in compiled_patterns.items():
        key = re.sub(r"date", date, key)
        Names_Logs_maj[key] = value
    
    """organization of logs in sample_logs/ in another .log file"""
    with open(log) as log_file:
        for line in log_file:
            find = False
            for key, regex in Names_Logs_maj.items():

                """
                The "find" boolean help for logs without match. Its goal is to give us alert when 
                all regex don't match
                """
                if regex.search(line):
                    with open(os.path.join(logs_dir, key), "a") as file:
                        file.write(line.strip() + "\n")
                    new_line = report_creation(regex, line)
                    if new_line:
                        """
                        if we find correspondance, we take importants information for reports
                        """
                        Names_Reports_maj[key].append(new_line)
                        find = True
                        break
            if not find:
                with open(os.path.join(logs_dir, "other_logs.log"), "a") as file:
                    file.write(line.strip() + "\n")

    return Names_Reports_maj



"""
This function merge created dictionaries which are output of parse_log_file(). It return
all dictionnaries in one with values which are report's names...
"""
def merge(Names_Reports_maj, report):
    for key, value in Names_Reports_maj.items():
        report.setdefault(key, []).extend(value)
    return report