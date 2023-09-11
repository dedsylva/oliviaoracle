from src.services.AuthenticationService import AuthenticationService
from src.services.CalendarService import CalendarService 
from src.management.Functions import Functions

class GoogleManager:
  def __init__(self):

    self.authentication_service = AuthenticationService()
    self.credential = self.authentication_service.authenticate_google()

    self.calendar_service = CalendarService(self.credential)
    self.functions = Functions()
    self.functions._add("get_events", self.get_events, "number_of_days")

  def get_events(self, number_of_days=10):

    events = self.calendar_service.get_upcoming_events(number_of_days)
    CalendarService.create_response_message(events)