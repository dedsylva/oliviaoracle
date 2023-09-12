import logging
from src.domain.google.Event import Event
from src.management.Singleton import Singleton

class Events(metaclass=Singleton):

  def __init__(self):
    pass

  def _add(self, ):
    logging.DEBUG(f"Adding event")
    pass
  
  def _get(self):
    pass