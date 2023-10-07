from src.management.Database import DatabaseManagement
from src.queries.reminders import select_values
from src.domain.common.Appointment import Appointment

class Appointments:
  def __init__(self, database_management: DatabaseManagement):
    self.database_management = database_management
  
  # TODO: make this more generic: def get_all for and you pass the schema and dataclass
  def get_all_appointments(self) -> list[Appointment]:
    values = self.database_management.cursor.execute(select_values).fetchall()
    return [Appointment(v) for v in values]