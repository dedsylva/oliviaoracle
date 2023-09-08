import datetime
from googleapiclient.discovery import build
from src.aux.utils import get_month_name


# https://console.cloud.google.com/ --> settings of project
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = '../credentials.json'

class CalendarService:

  def __init__(self, credentials):
    self.credentials = credentials
    self.service = build('calendar', 'v3', credentials=self.credentials)

  def get_calendar_service(self):
    return self.service

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
        
  def get_upcoming_events(self, number_of_events):

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting List of 10 events')
    events_result = self.service.events().list(
                        calendarId='primary', 
                        timeMin=now,
                        maxResults=number_of_events, 
                        singleEvents=True,
                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
      # TODO: replace print with logging
      # TODO: create custom exception
      print('No upcoming events found.')
    else:
      return events

  @staticmethod
  def create_response_message(events):
    for event in events:
      # start information
      event_date_start, event_time_start = event['start'].get('dateTime', event['start'].get('date')).split('T')
      year_start, month_start, day_start = event_date_start.split("-")

      # end information
      event_date_end, event_time_end = event['end'].get('dateTime', event['start'].get('date')).split('T')
      year_end, month_end, day_end = event_date_end.split("-")

      # TODO: create method for handling the type of messages better
      if event_date_start == event_date_end:
        print(f"{event['summary']} happens on {day_start} of {get_month_name(month_start)} of {year_start}, starting at {handle_time_and_create_response_message(event_time_start)} and ending at {handle_time_and_create_response_message(event_time_end)}")
      else:
        print(f"{event['summary']} starts on {day_start} of {get_month_name(month_start)} of {year_start} at {handle_time_and_create_response_message(event_time_start)} and it ends on {day_end} of {get_month_name(month_end)}, {year_end} at {handle_time_and_create_response_message(event_time_end)}")
