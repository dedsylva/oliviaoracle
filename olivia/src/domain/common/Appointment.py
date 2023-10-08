from dataclasses import dataclass
from typing import Optional

@dataclass
class Appointment:
  id: int
  name: str
  start_date: str
  start_time: str
  end_date: str
  end_time: str
  description: Optional[str] | None = None