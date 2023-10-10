from .Response import Response

class FunctionErrorResponse(Response):
  def __init__(self, msg):
    super().__init__(msg)