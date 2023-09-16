import logging
from src.services.AuthenticationService import AuthenticationService
from src.services.CalendarService import CalendarService 
from src.services.FunctionService import FunctionService 
from src.domain.google.Event import EventCreation, EventFetch
from src.domain.common.Function import Function

class GoogleManager:
  def __init__(self, function_service: FunctionService, authentication_service: AuthenticationService):

    logging.debug(f"Instantiating GoogleManager")

    self.authentication_service = authentication_service
    self.credential = self.authentication_service.authenticate_google()

    self.calendar_service = CalendarService(self.credential)
    self.function_service = function_service
    self.function_service._add(Function("get_events", self.get_events, EventFetch))
    self.function_service._add(Function("create_event", self.create_event, EventCreation))

    logging.debug(f"Added the following functions: {self.function_service._get()}")

  def get_events(self, event_fetch: EventFetch):
    logging.info("Getting events from Google Calendar")

    events = self.calendar_service._get_events(event_fetch)
    return CalendarService.create_response_message(events)
  
  def create_event(self, event: EventCreation):
    logging.info("Creating one event in to Google Calendar")
    logging.debug(f"Event to be created: \n{event}")
    self.calendar_service._create_event(event)