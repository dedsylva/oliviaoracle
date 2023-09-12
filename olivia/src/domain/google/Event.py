from dataclasses import dataclass
from EventTime import EventTime
from typing import Optional

@dataclass
class Event:
  summary: str
  location: str
  description: str
  start: list[EventTime]
  end: list[EventTime]
  attendees: Optional[str] = None