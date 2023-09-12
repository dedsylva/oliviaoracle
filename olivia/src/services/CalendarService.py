import logging
import datetime
from googleapiclient.discovery import build
from src.aux.utils import get_month_name
from src.domain.google.Event import Event

class CalendarService:

  def __init__(self, credentials):
    self.credentials = credentials
    self.service = build('calendar', 'v3', credentials=self.credentials)

  def get_calendar_service(self):
    return self.service

  @staticmethod
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
        
  def get_upcoming_events(self, number_of_days):
    logging.DEBUG(f"Getting Upcoming Events for {number_of_days} days")

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # TODO: replace print with logging
    print('Getting List of 10 events')
    events_result = self.service.events().list(
                        calendarId='primary', 
                        timeMin=now,
                        maxResults=number_of_days, 
                        singleEvents=True,
                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
      logging.WARN("No upcoming events found")
      return "{\"descrption\": \"no events found for the next\" + number_of_days + \" days\"}"
    else:
      logging.DEBUG("Got the following events from Google Calendar API")
      logging.DEBUG(events)
      return events

  @staticmethod
  def create_response_message(events):
    logging.DEBUG(f"Creating Response Message for events:")
    logging.DEBUG(events)

    for event in events:
      # start information
      event_date_start, event_time_start = event['start'].get('dateTime', event['start'].get('date')).split('T')
      year_start, month_start, day_start = event_date_start.split("-")

      # end information
      event_date_end, event_time_end = event['end'].get('dateTime', event['start'].get('date')).split('T')
      year_end, month_end, day_end = event_date_end.split("-")

      return "{\"event_name\": " + event['summary']+ ", \"day_start\": " + day_start + ", \"month_start\": "+ get_month_name(month_start) + " , \"year_start\": " + year_start + " , \"time_start\": " + CalendarService.handle_time_and_create_response_message(event_time_start) + ", \"day_end\": " + day_end + ", \"month_end\": "+ get_month_name(month_end) + " , \"year_end\": " + year_end + " , \"time_end\": " + CalendarService.handle_time_and_create_response_message(event_time_end) + "}"
  
  def _create_event(self, event: Event):
    # https://developers.google.com/calendar/api/v3/reference/events/insert#python
    self.service.events().insert(
                            calendarId='primary', 
                            body=event).execute()