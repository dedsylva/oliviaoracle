import logging
from src.database.queries.BaseQuery import BaseQuery

class Repository:
  def __init__(self, table, cursor):
    logging.debug("Instantiating Repository Class")
    self.table = table
    self.base_queries = BaseQuery(self.table)
    self.cursor = cursor

  def get_one(self, id):
    logging.debug(f"Getting one item from table {self.table} with id {id}")
    self.cursor.execute(self.base_queries.get_one_query(id))

  def get_all(self):
    logging.debug(f"Getting all items from table {self.table}")
    self.cursor.execute(self.base_queries.get_all_query())

  def update_one(self, id):
    logging.debug(f"Updating one item from table {self.table} with id {id}")
    self.cursor.execute(self.base_queries.update_one_query(id))

  def remove_one(self, id):
    logging.debug(f"Removing one item from table {self.table} with id {id}")
    self.cursor.execute(self.base_queries.remove_one_query(id))

  def remove_all(self):
    logging.debug(f"Removing all items from table {self.table}")
    self.cursor.execute(self.base_queries.remove_all_query())