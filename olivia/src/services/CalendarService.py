import logging
import datetime
import json
from dataclasses import asdict
from googleapiclient.discovery import build
from src.aux.utils import get_month_name
from src.domain.google.Event import EventFetch, EventCreation 
from src.management.Singleton import Singleton

class CalendarService(metaclass=Singleton):

  def __init__(self, credentials):
    self.credentials = credentials
    self.google_calendar = build('calendar', 'v3', credentials=self.credentials)

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
        
  def _get_events(self, event: EventFetch):
    number_of_days = event.number_of_days
    logging.debug(f"Getting Upcoming Events for {number_of_days} days")

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # TODO: replace print with logging
    print('Getting List of 10 events')
    events_result = self.google_calendar.events().list(
                        calendarId='primary', 
                        timeMin=now,
                        maxResults=number_of_days, 
                        singleEvents=True,
                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
      logging.warn("No upcoming events found")
      # TODO: transform this in to a generic function in utils that transforms in to chatgpt format
      return "{\"descrption\": \"no events found for the next\" + number_of_days + \" days\"}"
    else:
      logging.debug("Got the following events from Google Calendar API")
      logging.debug(events)
      return events

  @staticmethod
  def create_response_message(events):
    logging.debug(f"Creating Response Message for events:")
    logging.debug(events)

    for event in events:
      # start information
      event_date_start, event_time_start = event['start'].get('dateTime', event['start'].get('date')).split('T')
      year_start, month_start, day_start = event_date_start.split("-")

      # end information
      event_date_end, event_time_end = event['end'].get('dateTime', event['start'].get('date')).split('T')
      year_end, month_end, day_end = event_date_end.split("-")

      # TODO: transform this in to a generic function in utils that transforms in to chatgpt format
      return "{\"event_name\": " + event['summary']+ ", \"day_start\": " + day_start + ", \"month_start\": "+ get_month_name(month_start) + " , \"year_start\": " + year_start + " , \"time_start\": " + CalendarService.handle_time_and_create_response_message(event_time_start) + ", \"day_end\": " + day_end + ", \"month_end\": "+ get_month_name(month_end) + " , \"year_end\": " + year_end + " , \"time_end\": " + CalendarService.handle_time_and_create_response_message(event_time_end) + "}"
  
  def _create_event(self, event: EventCreation):
    # TODO: datetime is being created wrong. maybe something to do with timezone
    # https://developers.google.com/calendar/api/v3/reference/events/insert#python
    logging.info(f"Calling Google Calendar API for creating event")
    event = asdict(event)

    result = self.google_calendar.events().insert(
                            calendarId='primary', 
                            body=event).execute()

    if result is not None:
      logging.info(f"Success! Event created")
      logging.debug(f"Event: \n{event}")
      logging.info(f"Result: \n{result}")
    return "Event Created"