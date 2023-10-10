import logging
from src.services.AuthenticationService import AuthenticationService
from src.services.CalendarService import CalendarService 
from src.services.FunctionService import FunctionService 
from src.domain.google.Event import EventCreation, EventFetch
from src.domain.common.Function import Function
from src.management.Database import DatabaseManagement
from src.domain.common.Appointment import Appointment

class GoogleManager:
  def __init__(self, function_service: FunctionService, authentication_service: AuthenticationService, database_management: DatabaseManagement):

    logging.debug(f"Instantiating GoogleManager")

    self.authentication_service = authentication_service
    self.credential = self.authentication_service.authenticate_google()
    self.database_management = database_management


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

    # hallucinations of ChatGPT, and this is not being set by default on the class
    event.start["timeZone"] = "America/Sao_Paulo"
    event.end["timeZone"] = "America/Sao_Paulo"

    logging.info("Creating one event in to Google Calendar")
    logging.debug(f"Event to be created: \n{event}")

    value = self.calendar_service._create_event(event)

    # TODO: start_time and end_time is not correctly here
    appointment = Appointment(id=1, name=event.summary, 
                              start_date=event.start["dateTime"].split('T')[0], 
                              start_time=event.start["dateTime"].split('T')[1].replace(':', '-'), 
                              end_date=event.end["dateTime"].split('T')[0],
                              end_time=event.end["dateTime"].split('T')[1].replace(':', '-'), 
                              description=event.description)
    
    logging.debug(f"Creating Appointment: {appointment}")

    self.database_management.repository.insert_one(appointment)
    return value