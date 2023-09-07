from googleapiclient.discovery import build

class CalendarService:

  def __init__(self, credentials):
    self.credentials = credentials
    self.service = build('calendar', 'v3', credentials=self.credentials)
    