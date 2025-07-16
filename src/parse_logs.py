#coding=utf-8

import os
import re
from datetime import datetime
from generate_report import report_creation
from archive import archive


def filenamesWithDate():
    
    """
    We change keys (file's names) and add date for repots and logs
    """
    date = str(datetime.now().date())
    """
    Names_Logs contain all .log files names and regex which can help us to identify importants elements
    for the creation of reports
    compiled_pattern change raw_strings of Names_Logs into regex objects which permit and more easy research
    """

    Names_Logs = {f"access_{date}.log": r"\[([\d -:]+)\] INFO: User (\w+) logged (\w+) from ([\d.]+)",
              f"error_{date}.log": r"\[([\d -:]+)\] ERROR: (\w+) ([\w| ]+) on (server\d)",
              f"auth_fail_{date}.log": r"\[([\d -:]+)\] FAILED LOGIN: ([\w ]+) for user (\w+) from ([\d.]+)",
              f"server1_sys_{date}.log": r"\[([\d -:]+)\] WARNING: High (\w+ usage) on server1 - \w+: (\d+)%", 
              f"server2_sys_{date}.log": r"\[([\d -:]+)\] WARNING: High (\w+ usage) on server2 - \w+: (\d+)%",
              f"server3_sys_{date}.log": r"\[([\d -:]+)\] WARNING: High (\w+ usage) on server3 - \w+: (\d+)%",
              f"backup_{date}.log": r"\[([\d -:]+)\] INFO: Backup (\w+) successfully on (\w+)",
              f"security_{date}.log": r"\[([\d -:]+)\] ERROR: ([\w ]+) attempt by ([\d.]+)"}
    compiled_patterns = {key: re.compile(value) for key, value in Names_Logs.items()}

    """
    Names_Reports contains values which are lists of dictionary. We will use the pandas modulo for
    the creation of .csv reports.
    """
    Names_Reports = {f"access_{date}.log": [],
              f"error_{date}.log": [],
              f"auth_fail_{date}.log": [],
              f"server1_sys_{date}.log": [],
              f"server2_sys_{date}.log": [],
              f"server3_sys_{date}.log": [],
              f"backup_{date}.log": [],
              f"security_{date}.log": []}
    return compiled_patterns , Names_Reports


"""
parse_log_file() take a .log file in parameter and return a dictionary which will be append in
Names_Reports
"""

def parse_log_file(log):



    logs_dir = os.path.join(os.getcwd(), "logs")  
    """logs/ creation"""
    os.makedirs(logs_dir , exist_ok=True)

    """report/ creation"""
    os.makedirs(os.path.join(os.getcwd(),"reports") , exist_ok=True)


    """Date of modification in our script"""

    Names_Logs_update, Names_Reports_update = filenamesWithDate()
#    for key, value in Names_Reports.items():
#        key = re.sub(r"date", date, key)
#        Names_Reports_update[key] = value
    
#    for key, value in compiled_patterns.items():
#        key = re.sub(r"date", date, key)
#        Names_Logs_update[key] = value
    
    """organization of logs in sample_logs/ in another .log file"""
    with open(log) as log_file:
        for line in log_file:
            find = False
            for key, regex in Names_Logs_update.items():

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
                        Names_Reports_update[key].append(new_line)
                        find = True
                        break
            if not find:
                with open(os.path.join(logs_dir, "other_logs.log"), "a") as file:
                    file.write(line.strip() + "\n")

    return Names_Reports_update



"""
This function merge created dictionaries which are output of parse_log_file(). It return
all dictionnaries in one with values which are report's names...
"""
def merge(Names_Reports_maj, report):
    for key, value in Names_Reports_maj.items():
        report.setdefault(key, []).extend(value)
    return report