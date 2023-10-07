from dataclasses import dataclass
from typing import Optional

@dataclass
class Appointment:
  id: int
  name: str
  description: Optional[str]
  start_date: str
  start_time: str
  end_date: str
  end_time: str