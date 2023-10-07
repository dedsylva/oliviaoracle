import threading
import logging
from src.queries.reminders import create_table, insert_value, select_value, delete_table
from src.management.Singleton import Singleton

class DatabaseManagement(metaclass=Singleton):
  def __init__(self):
    logging.info("Starting Database Management Class")
    self.started = False
    self._thread = None
    self.con = None
    self.cursor = None

  def validate_connection(self):
      logging.debug("testing creating appointments table")
      self.cursor.execute(create_table)

      logging.debug("testing inserting value in appointments table")
      self.cursor.execute(insert_value)

      logging.debug("testing selecting value in appointments table")
      value = self.cursor.execute(select_value).fetchall()

      assert len(value) == 1
      assert value[0] == (1, 'Test', None, '2023-10-07', '12', '2023-10-07', '13')

      logging.debug("testing deleting appointments table")
      self.cursor.execute(delete_table)

      logging.info("Connection validated")

  
  def initialize_database(self):
    if not self.con:
      import sqlite3

      try:
        logging.info("Connecting to olivia database")
        self.con = sqlite3.connect("olivia.db")
        self.cursor = self.con.cursor()

        if(self.validate_connection()) :
          logging.info("creating appointments table")
          self.cursor.execute(create_table)


      except Exception as e:
        logging.error("Error when trying to connect to olivia database")
        logging.error(e)
        exit(-1)

    else:
      logging.warn("Trying to create Database already initialized.")


  def reminder(self):
    while True:
      self.initialize_database()

      # TODO: remove this hard coded
      n_days = 1 

      appointments = self.get_appointments(n_days)
   
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
    else:
      logging.warn("Trying to stop a thread that is already closed")
