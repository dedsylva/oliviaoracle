import logging
import json
from src.management.Singleton import Singleton
from src.domain.common.Function import Function

class FunctionService(metaclass=Singleton):
  def __init__(self):
    self.functions = []

  def call_function(self,function_call):
    logging.info(f"Calling function {function_call['name']}")

    available_functions = self._get()
    for af in available_functions:
      if af["name"] == function_call["name"]:
        function = af["value"]

        args = [_dataclass(**json.loads(function_call["arguments"])) for _dataclass in af["args"]]

        logging.debug(f"Calling function {function_call['name']} with args {args}")
        try:
          return function(*args)
        except Exception as e:
          logging.error(f"Function {function_call['name']} with args {args} could not be executed properly")
          return None

      else:
        return None
        
  def _add(self, Function: Function):
    logging.debug(f"Adding function {Function.name} with args {Function.args}")
    args = [Function.args] if type(Function.args) != list else Function.args
    self.functions.append({"name": Function.name, 
                           "value": Function.value, 
                           "args": args})
  
  def _get(self):
    return self.functions