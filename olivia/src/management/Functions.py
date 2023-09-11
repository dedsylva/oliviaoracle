from src.domain.Function import Function
from src.management.Singleton import Singleton

class Functions(metaclass=Singleton):

  def __init__(self):
    self.functions = []

  def _add(self, name, value, args):
    args = [args] if type(args) == str else args
    self.functions.append(Function(name, value, args))
  
  def _get(self):
    return self.functions