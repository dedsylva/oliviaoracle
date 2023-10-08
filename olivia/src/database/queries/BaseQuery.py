import logging

class BaseQuery:
  def __init__(self, table):
    self.table = table
    logging.debug(f"Instantiagin BaseQuery class for table {self.table}")

  def get_one_query(self, id): 
    return f"SELECT TOP 1 FROM {self.table} WHERE id = {id}"

  def get_all_query(self): 
    return f"SELECT * FROM {self.table}"
  
  def update_one_query(self, id, column, value):
    return f"UPDATE {self.table} SET {column} = {value} WHERE id = {id}"
  
  def remove_one_query(self, id):
    return f"DELETE FROM {self.table} WHERE id = {id}"

  def remove_all_query(self):
    return f"DELETE FROM {self.table}"