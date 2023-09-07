import datetime
import pickle
import os.path
import calendar
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# https://console.cloud.google.com/ --> settings of project

SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = '../credentials.json'

def get_calendar_service():
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
          creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
              CREDENTIALS_FILE, SCOPES)
      creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)

  service = build('calendar', 'v3', credentials=creds)
  return service

def get_month_name(n): return calendar.month_name[1:][int(n)-1]

def handle_time_and_create_response_message(event_time):
  hour, minute, _ = event_time.split('-')[0].split(':')

  if int(hour) >= 12: 
    suffix = "PM"
  else:
    suffix = "AM"
  
  if int(hour) == 0 or int(hour) == 12:
    hour = 12
  else: 
    hour = int(hour)%12

  response = f"{hour}:{minute}" if int(minute) != 0 else hour
  response = f"{response} {suffix}" if suffix is not None else response

  return response
  


if __name__ == '__main__':
  service = get_calendar_service()

  # Call the Calendar API
  now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
  print('Getting List of 10 events')
  events_result = service.events().list(
                      calendarId='primary', 
                      timeMin=now,
                      maxResults=10, 
                      singleEvents=True,
                      orderBy='startTime').execute()
  events = events_result.get('items', [])

  if not events:
    print('No upcoming events found.')
  for event in events:
    # start information
    event_date_start, event_time_start = event['start'].get('dateTime', event['start'].get('date')).split('T')
    year_start, month_start, day_start = event_date_start.split("-")

    # end information
    event_date_end, event_time_end = event['end'].get('dateTime', event['start'].get('date')).split('T')
    year_end, month_end, day_end = event_date_end.split("-")

    # TODO: transform this in to class
    # TODO: create method for handling the type of messages better
    if event_date_start == event_date_end:
      print(f"{event['summary']} happens on {day_start} of {get_month_name(month_start)} of {year_start}, starting at {handle_time_and_create_response_message(event_time_start)} and ending at {handle_time_and_create_response_message(event_time_end)}")
    else:
      print(f"{event['summary']} starts on {day_start} of {get_month_name(month_start)} of {year_start} at {handle_time_and_create_response_message(event_time_start)} and it ends on {day_end} of {get_month_name(month_end)}, {year_end} at {handle_time_and_create_response_message(event_time_end)}")
