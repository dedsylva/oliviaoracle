from dataclasses import dataclass
from typing import Optional

@dataclass
class EventTime:
  dateTime: str
  timezone: str 

  def __post_init__(self):
    if self.timezone is None:
      self.timezone = "America/Sao_Paulo"

@dataclass
class EventCreation:
  summary: str
  location: str
  description: str
  start: EventTime
  end: EventTime
  attendees: Optional[str] = ""

@dataclass
class EventFetch:
  number_of_days: int
