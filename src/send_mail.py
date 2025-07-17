#coding = utf-8

"""
- OS error: CPU or RAM
- New type of log detected for an update
- Unautorised authentification
- More than 3 times wrong authentification
"""

import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle

# ✅ Portée d'autorisation
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    creds = None
    # Le fichier token.pickle contient les tokens d'accès actuels
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Si pas de credentials valides
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Sauvegarder les credentials pour la prochaine exécution
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f'OK! Message envoyé, ID : {sent_message["id"]}')
        return sent_message
    except Exception as e:
        print(f'[ERREUR] Une erreur est survenue : {e}')


if __name__ == '__main__':
    service = gmail_authenticate()
    email = create_message(
        sender="lespoyler31@gmail.com",
        to="pythontests609@gmail.com",
        subject="Alerte critique",
        message_text="Bonjour,\nUne alerte a été détectée sur le serveur."
    )
    send_message(service, 'me', email)
