import logging
from src.aux.utils import open_file
from src.exceptions.InvalidLanguage import InvalidLanguage


class ContextManagerService:
  def __init__(self, language):
    self.language = language
    self.context = None
    logging.debug(f"Instantiating ContextManagerService")
  
  def get_context(self):
    logging.info(f"Getting context file")

    if self.language == "en":
        #self.context = "chatbot_en.txt"
        self.context = "context_en.txt"
    elif self.language == "pt":
        #self.context = "chatbot_pt.txt"
        self.context = "context_pt.txt"
    else:
        raise InvalidLanguage(f"Invalid Context. We currently support en (english) and pt (brazililian portuguese), but got {self.language} language")

    return open_file(self.context)
