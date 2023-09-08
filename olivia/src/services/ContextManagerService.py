from src.aux.utils import open_file

class ContextManagerService:
  def __init__(self, language):
    self.language = language
    self.context = None
  
  def get_context(self):

    if self.language == "en":
        self.context = "chatbot_en.txt"
    elif self.language == "pt":
        self.context = "chatbot_pt.txt"
    else:
      # TODO: create custom exceptions
        raise ValueError(f"Invalid Context. We currently support en (english) and pt (brazililian portuguese), but got {LANGUAGE} language")

    return open_file(self.context)
