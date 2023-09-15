import os
import logging
from datetime import datetime

log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

#filename = datetime.now().strftime("olivia-oracle-%m/%d/%Y %I:%M:%S %p.log").replace('/', '-').replace(':', '-').replace(' ', '_')
filename = datetime.now().strftime("olivia-oracle.log")

# Construct the full log path
log_path = os.path.join(log_directory, filename)


class LogHandler:
  def __init__(self, level=logging.INFO):
    self.level = level
    logging.basicConfig(filename=log_path, encoding="UTF-8", level=self.level, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p %Z')