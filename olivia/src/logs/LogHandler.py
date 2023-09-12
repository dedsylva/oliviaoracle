import logging

class LogHandler:
  def __init__(self, level=logging.INFO):
    self.level = level
    logging.basicConfig(filename="%m-%d-%Y_%I-%M-%S.log", encoding="UTF-8", level=self.level, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p %Z')