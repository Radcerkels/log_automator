# coding: utf-8

import re

def report_creation(line):
    """
    This fonction will take a line and a pattern which match and will take the most
    usefull informations and return a dictionary with...
    """
    pattern = re.compile(r"\[([\d -:]+)\] ERROR: (\w+) ([\w| ]+) on (server\d)")
    result = pattern.search(line)
    """errors"""
    if result:
        return {
             "Timestamp" : result[1],
             "Server" : result[4],
             "ErrorType" : result[2],
             "Message" : result[2] + " " + result[3]} , "error"
        
    pattern = re.compile(r"\[([\d -:]+)\] INFO: User (\w+) logged (\w+) from ([\d.]+)")  
    result = pattern.search(line)
    """access"""
    if result:
        return {
             "Timestamp" : result[1],
             "User" : result[2],
             "IP" : result[4], 
             "Action" : "LOG" + result[3].upper()} , "access"
        
    pattern = re.compile(r"\[([\d -:]+)\] FAILED LOGIN: ([\w ]+) for user (\w+) from ([\d.]+)")
    result = pattern.search(line)
    """auth_fail"""
    if result:
        return {
             "Timestamp" : result[1],
             "User" : result[3],
             "IP" : result[4],
             "Message" : result[2]} , "auth"
        
    pattern = re.compile(r"\[([\d -:]+)\] ERROR: ([\w ]+) attempt by ([\d.]+)")
    result = pattern.search(line)
    """Security"""
    if result:
        return {
             "Timestamp" : result[1],
             "IP Source" : result[3],
             "Attempted Action" : result[2]} , "security"
        
    pattern = re.compile(r"\[([\d -:]+)\] INFO: Backup (\w+) successfully on (\w+)")
    result = pattern.search(line)
    """backup"""
    if result:
        return {
             "Timestamp" : result[1],
             "Server" : result[3],
             "Status" : result[2]} , "backup"

    pattern = re.compile(r"\[([\d -:]+)\] WARNING: High (\w+ usage) on server1 - \w+: (\d+)%")  
    result = pattern.search(line)
    """server1_sys"""  
    if result:
        return {
             "Timestamp" : result[1],
             "Metric" : result[2],
             "Value" : result[3]+"%"} , "server1"
    
    pattern = re.compile(r"\[([\d -:]+)\] WARNING: High (\w+ usage) on server2 - \w+: (\d+)%")
    result = pattern.search(line)
    """server2_sys"""
    if result:
        return {
             "Timestamp" : result[1],
             "Metric" : result[2],
             "Value" : result[3]+"%"} , "server2"
        
    pattern = re.compile(r"\[([\d -:]+)\] WARNING: High (\w+ usage) on server3 - \w+: (\d+)%")
    result = pattern.search(line)
    """server3_sys"""
    if result:
        return {
             "Timestamp" : result[1],
             "Metric" : result[2],
             "Value" : result[3]+"%"} , "server3"
    return None, None