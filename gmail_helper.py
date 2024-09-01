import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os.path

class GmailPortalHelper:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        self.credentials = self.login()

    def login(self):
        creds = None
        token_path = 'token.json'
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        return creds

    def send_email(self, subject, body, receiver):
        service = build('gmail', 'v1', credentials=self.credentials)

        message = MIMEText(body)
        message['to'] = receiver
        message['from'] = 'wkrak98@gmail.com'
        message['subject'] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message = {
            'raw': raw
        }

        try:
            result = service.users().messages().send(userId='me', body=message).execute()
            print(f"Message sent successfully: {result['id']}")
        except Exception as error:
            print(f"An error occurred: {error}")

# Przykład użycia:
if __name__ == '__main__':
    gmail_helper = GmailPortalHelper()
    gmail_helper.send_email(
        subject="Test Email",
        body="This is a test email sent using Gmail API.",
        receiver="wkrak98@gmail.com"
    )
