import os
import time
from datetime import datetime
import threading
import logging
from src.database.schemas.reminders import create_table, insert_value, select_value, delete_table
from src.management.Singleton import Singleton
from src.repository.Repository import Repository
from src.domain.common.Appointment import Appointment

class DatabaseManagement(metaclass=Singleton):
  def __init__(self):
    logging.info("Starting Database Management Class")
    self.started = False
    self._thread = None
    self.con = None
    self.cursor = None
    self.repository = None

    # Always clean databases
    if os.path.exists("olivia.db"):
      os.remove("olivia.db")

    if os.path.exists("olivia.db-journal"):
      os.remove("olivia.db-journal")

  def validate_connection(self):
      logging.debug("testing creating appointments table")
      self.cursor.execute(create_table)

      logging.debug("testing inserting value in appointments table")
      self.cursor.execute(insert_value)

      logging.debug("testing selecting value in appointments table")
      value = self.cursor.execute(select_value).fetchone()

      assert value == (1, "Test", "2023-10-08", "2-49", "2023-10-09", "2-40", None)
      logging.debug("testing deleting appointments table")
      self.cursor.execute(delete_table)

      logging.info("Connection validated")

      return True

  
  def initialize_database(self):
    if not self.con:
      import sqlite3

      try:
        logging.info("Connecting to olivia database")
        self.con = sqlite3.connect("olivia.db")
        self.cursor = self.con.cursor()
        self.repository = Repository(table="appointments", cursor=self.cursor)

        if(self.validate_connection()) :
          logging.info("creating appointments table")
          self.cursor.execute(create_table)

          logging.info("inserting value in appointments table")
          self.cursor.execute(insert_value)


      except Exception as e:
        self.con = None
        self.cursor = None
        self.repository = None
        logging.error("Error when trying to connect to olivia database")
        logging.error(e)
        exit(-1)

    else:
      logging.warn("Trying to create Database already initialized.")

  
  @staticmethod
  def check_time(appointment_start_date, appointment_start_time, current_date, current_time):
    appointment_start_date = [int(app) for app in appointment_start_date]
    appointment_start_time = [int(app) for app in appointment_start_time]

    if appointment_start_date != current_date:
      return False, ""
    # appointment is now
    elif appointment_start_time == current_time:
      return True, "now!"
    # appointment is in 1 hour
    elif appointment_start_time[0] == current_time[0] and (appointment_start_time[1] - current_time[1]) == 60:
      return True, "in 1 hour"
    # appointment is in 30 min
    elif appointment_start_time[0] == current_time[0] and (appointment_start_time[1] - current_time[1]) == 30:
      return True, "in 30 minutes"
    # appointment is in 15 min
    elif appointment_start_time[0] == current_time[0] and (appointment_start_time[1] - current_time[1]) == 15:
      return True, "in 15 minutes"
    # appointment is in 5 min
    elif appointment_start_time[0] == current_time[0] and (appointment_start_time[1] - current_time[1]) == 5:
      return True, "in 5 minutes"
    else:
      return False, ""

  @staticmethod
  def send_reminder(name, description, timing):
    # TODO: this should be sent to elevenlabs api to voice
    logging.info(f"Reminder: {name}{description if description else ''} is starting {timing}")

  def reminder(self):
    self.initialize_database()
    time.sleep(3)
    cache = {}
    while True:
      # get appointments from the database
      appointments = [Appointment(*a) for a in self.repository.get_all()]

      # check if appointment is to happen this day. If so caches it and waits 5 minutes 
      local_date_time = time.localtime()
      current_date = [local_date_time.tm_year, local_date_time.tm_mon, local_date_time.tm_mday]
      current_time = [local_date_time.tm_hour, local_date_time.tm_min]
      for appointment in appointments:
        appointment_start_date = appointment.start_date.split('-')
        appointment_start_time = appointment.start_time.split('-')

        check, timing = DatabaseManagement.check_time(appointment_start_date, appointment_start_time, current_date, current_time)
        if check:
          DatabaseManagement.send_reminder(appointment.name, appointment.description, timing)

        else:
          logging.debug("Reminder Thread: Sleeping for 60 seconds")

        time.sleep(60)

   
  def _start(self):
    if not self.started and not self._thread:
      self._thread = threading.Thread(target=self.reminder)
      self._thread.daemon = True # allows thread to exit when main program exits
      logging.info("Starting Reminder Thread")
      self._thread.start()
      self.started = True
    else:
      logging.warn("Trying to start a thread that is already running")

  def _stop(self):
    if self.started and self._thread:
      logging.info("Stopping Reminder Thread")
      self._thread.join()
      self.started = False
      self._thread = None
      self.con = None
      self.cursor = None
      self.repository = None
    else:
      logging.warn("Trying to stop a thread that is already closed")
