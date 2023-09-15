from dataclasses import dataclass
from typing import Optional

@dataclass
class EventTime:
  dateTime: str
  timezone: str

@dataclass
class EventCreation:
  summary: str
  location: str
  description: str
  start: list[EventTime]
  end: list[EventTime]
  attendees: Optional[str] = None

@dataclass
class EventFetch:
  number_of_days: int
