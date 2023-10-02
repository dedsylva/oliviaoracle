import os
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# https://console.cloud.google.com/ --> settings of project
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/calendar']
GOOGLE_CREDENTIALS_FILE = '../credentials.json'

class AuthenticationService:

  def __init__(self):
    self.creds = None
  
  def authenticate_google(self):
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            self.creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not self.creds or not self.creds.valid:
      if self.creds and self.creds.expired and self.creds.refresh_token:
        self.creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
                GOOGLE_CREDENTIALS_FILE, GOOGLE_SCOPES)
        self.creds = flow.run_local_server(port=0)

      # Save the credentials for the next run
      with open('token.pickle', 'wb') as token:
        pickle.dump(self.creds, token)
    
    return self.creds
