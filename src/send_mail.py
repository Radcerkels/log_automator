#coding = utf-8

import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import sys

# ✅ Portée d'autorisation
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    creds = None
    """token.pickle file stores the user's access and refresh tokens, and is created automatically"""
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    """If there are no (valid) credentials available, let the user log in."""

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        """Save the credentials for the next run"""
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def messageFilter(report):

        print(f"Report found: {report}")
        if report.startswith("security"):
            subject = "Security Alert"
            message_text = f"[ERROR] A security alert has been detected in {report}..."
            return subject, message_text
        elif report.startswith("error"):
            subject = "Error Alert"
            message_text = f"[ERROR] An error has been detected in {report}..."
            return subject, message_text
        elif report.startswith("auth_fail"):
            subject = "Authentication Failure Alert"
            message_text = f"[ERROR] An authentication failure has been detected in {report}..."
            return subject, message_text
        elif report.startswith("server1_sys") or report.startswith("server2_sys") or report.startswith("server3_sys"):
            subject = "System Alert"
            message_text = f"[WARNING] High system usage detected in {report}..."
            return subject, message_text
        return None, None    


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f'OK! Message sended, ID : {sent_message["id"]}')
        return sent_message
    except Exception as e:
        print(f'[ERROR] An error occured : {e}')


def send_mail():

    """
    This function is used to send email alerts based on reports in the reports directory.
    So if you want to send an email, you must have a report in reports/ directory
    """
    reportPath = os.path.join(os.getcwd(), "reports")
    if not os.path.exists(reportPath) or not os.listdir(reportPath):
        sys.exit("No reports found. Exiting...")
    
    service = gmail_authenticate()
    """Iterate through each report in the reports directory and send an email alert."""
    general_message = ""
    for report in os.listdir(reportPath):
        subject , message_text = messageFilter(report)

        """If subject or message_text is None, it means no alert was found in the report"""
        if not subject or not message_text:
            continue

        email = create_message(
            sender="lespoyler31@gmail.com",
            to="pythontests609@gmail.com",
            subject=subject,
            message_text=message_text)
        
        send_message(service, 'me', email)
        general_message += f"{subject} : {message_text}\n"

    if not general_message:
        sys.exit("No alerts found. Exiting...")
    email = create_message(
            sender="lespoyler31@gmail.com",
            to="pythontests609@gmail.com",
            subject="Global system alert(s) report(s)",
            message_text=general_message)
    send_message(service, 'me', email)
