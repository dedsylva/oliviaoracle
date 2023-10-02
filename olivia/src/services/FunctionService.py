import logging
import json
from src.management.Singleton import Singleton
from src.domain.common.Function import Function

class FunctionService(metaclass=Singleton):
  def __init__(self):
    self.functions = []

  # TODO: validate if function has the right arguments to instantiate dataclass, otherwise we need to ask for user the rest of the inputs
  def validate_function(self, function_call): pass

  def call_function(self,function_call):
    logging.info(f"Calling function {function_call['name']}")

    available_functions = self._get()
    for af in available_functions:
      if af["name"] == function_call["name"]:
        logging.info(f"Starting to look for arguments of function {af['name']}")
        function = af["value"]

        try:
          args = [_dataclass(**json.loads(function_call["arguments"])) for _dataclass in af["args"]]
        except Exception as e:
          logging.error(f"Invalid parameters for function {function_call['name']} and one of dataclasses {af['args']}")
          logging.error(f"Exception: \n{e}")

        logging.debug(f"Calling function {function_call['name']} with args {args}")
        try:
          return function(*args)
        except Exception as e:
          logging.error(f"Function {function_call['name']} with args {args} could not be executed properly")
          logging.error(f"Exception: \n{e}")
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