#coding=utf-8

import re

def report_creation(pattern , line):
    """
    This fonction will take a line and a pattern which match and will take the most
    usefull informations and return a dictionary with...
    """
    if pattern == re.compile(r"\[([\d -:]+)\] ERROR: (\w+) ([\w| ]+) on (server\d)"): 
        """errors"""
        result = pattern.search(line)
        if result:
            return {
             "Timestamp" : result[1],
             "Server" : result[4],
             "ErrorType" : result[2],
             "Message" : result[2] + " " + result[3]}
        else:
            return None
        
    elif pattern == re.compile(r"\[([\d -:]+)\] INFO: User (\w+) logged (\w+) from ([\d.]+)"): 
        """access"""
        result = pattern.search(line)
        if result:
            return {
             "Timestamp" : result[1],
             "User" : result[2],
             "IP" : result[4],
             "Action" : "LOG" + result[3].upper()}
        else:
            return None
        
    elif pattern == re.compile(r"\[([\d -:]+)\] FAILED LOGIN: ([\w ]+) for user (\w+) from ([\d.]+)"): 
        """Auth_fail"""
        result = pattern.search(line)
        if result:
            return {
             "Timestamp" : result[1],
             "User" : result[3],
             "IP" : result[4],
             "Message" : result[2]}
        else:
            return None
        
    elif pattern == re.compile(r"\[([\d -:]+)\] ERROR: ([\w ]+) attempt by ([\d.]+)"): 
        """Security"""
        result = pattern.search(line)
        if result:
            return {
             "Timestamp" : result[1],
             "IP Source" : result[3],
             "Attempted Action" : result[2]}
        else:
            return None
        
    elif pattern == re.compile(r"\[([\d -:]+)\] INFO: Backup (\w+) successfully on (\w+)"): 
        """backup"""
        result = pattern.search(line)
        if result:
            return {
             "Timestamp" : result[1],
             "Server" : result[3],
             "Status" : result[2]}
        else:
            return None
        
    elif pattern == re.compile(r"\[([\d -:]+)\] WARNING: High (\w+ usage) on server1 - \w+: (\d+)%"): 
        """server1_sys"""
        result = pattern.search(line)
        if result:
            return {
             "Timestamp" : result[1],
             "Metric" : result[2],
             "Value" : result[3]+"%"}
        else:
            return None
    
    elif pattern == re.compile(r"\[([\d -:]+)\] WARNING: High (\w+ usage) on server2 - \w+: (\d+)%"):
        """server2_sys"""
        result = pattern.search(line)
        if result:
            return {
             "Timestamp" : result[1],
             "Metric" : result[2],
             "Value" : result[3]+"%"}
        else:
            return None
        
    elif pattern == re.compile(r"\[([\d -:]+)\] WARNING: High (\w+ usage) on server3 - \w+: (\d+)%"):
        """server3_sys"""
        result = pattern.search(line)
        if result:
            return {
             "Timestamp" : result[1],
             "Metric" : result[2],
             "Value" : result[3]+"%"}
        else:
            return None