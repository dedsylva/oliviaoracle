from src.services.AuthenticationService import AuthenticationService
from src.services.CalendarService import CalendarService 

class GoogleManager:
  def __init__(self):

    self.authentication_service = AuthenticationService()
    self.credential = self.authentication_service.authenticate_google()

    self.calendar_service = CalendarService(self.credential)

  def get_events(self, number_of_events=10):

    events = self.calendar_service.get_upcoming_events(number_of_events)
    CalendarService.create_response_message(events)