# coding: utf-8
import sys
import unittest
import os
import re
"""
Adds dynamically the parent path of the 'src' folder to the system path
"""
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from generate_report import report_creation

class TestReportCreation(unittest.TestCase):
    def test_error_pattern(self):
        pattern = re.compile(r"\[([\d -:]+)\] ERROR: (\w+) ([\w| ]+) on (server\d)")
        line = "[2025-05-07 03:03:21] ERROR: Service mysql failed to start on server2"
        expected = {
            "Timestamp": "2025-05-07 03:03:21",
            "Server": "server2",
            "ErrorType": "Service",
            "Message": "Service mysql failed to start"
        }
        self.assertEqual(report_creation(pattern, line), expected)
    def test_access_pattern(self):
        pattern = re.compile(r"\[([\d -:]+)\] INFO: User (\w+) logged (\w+) from ([\d.]+)")
        line = "[2025-05-04 20:50:12] INFO: User charlie logged out from 192.168.2.15"
        expected = {
            "Timestamp": "2025-05-04 20:50:12",
            "User": "charlie",
            "IP": "192.168.2.15",
            "Action": "LOGOUT"
        }
        self.assertEqual(report_creation(pattern, line), expected)
    def test_auth_fail_pattern(self):
        pattern = re.compile(r"\[([\d -:]+)\] FAILED LOGIN: ([\w ]+) for user (\w+) from ([\d.]+)")
        line = "[2025-05-04 20:50:12] FAILED LOGIN: Invalid password for user alice from 192.168.2.15"
        expected = {
            "Timestamp": "2025-05-04 20:50:12",
            "User": "alice",
            "IP": "192.168.2.15",
            "Message": "Invalid password"
        }
        self.assertEqual(report_creation(pattern, line), expected)
    def test_security_pattern(self):
        pattern = re.compile(r"\[([\d -:]+)\] ERROR: ([\w ]+) attempt by ([\d.]+)")
        line = "[2025-05-04 20:50:12] ERROR: Unauthorized access attempt by 192.168.2.15"
        expected = {
            "Timestamp": "2025-05-04 20:50:12",
            "IP Source": "192.168.2.15",
            "Attempted Action": "Unauthorized access"
        }
        self.assertEqual(report_creation(pattern, line), expected)
    def test_backup_pattern(self):
        pattern = re.compile(r"\[([\d -:]+)\] INFO: Backup (\w+) successfully on (\w+)")
        line = "[2025-05-04 20:50:12] INFO: Backup completed successfully on server1"
        expected = {
            "Timestamp": "2025-05-04 20:50:12",
            "Server": "server1",
            "Status": "completed"
        }
        self.assertEqual(report_creation(pattern, line), expected)
    def test_server1_sys_pattern(self):
        pattern = re.compile(r"\[([\d -:]+)\] WARNING: High (\w+ usage) on server1 - \w+: (\d+)%")
        line = "[2025-05-04 20:50:12] WARNING: High CPU usage on server1 - CPU: 95%"
        expected = {
            "Timestamp": "2025-05-04 20:50:12",
            "Metric": "CPU usage",
            "Value": "95%"
        }
        self.assertEqual(report_creation(pattern, line), expected)



if __name__ == "__main__":
    unittest.main()