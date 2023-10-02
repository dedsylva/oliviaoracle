#! /usr/bin/python3

import os
import logging
from src.services.ContextManagerService import ContextManagerService
from src.services.RecordService import RecordService
from src.services.ChatGPTService import ChatGPTService
from src.services.ElevenLabsService import ElevenLabsService
from src.services.FunctionService import FunctionService
from src.services.AuthenticationService import AuthenticationService
from src.entities.google.GoogleManager import GoogleManager
from src.aux.utils import get_voice_id, open_file, get_available_functions_from_json
from src.management.LogHandler import LogHandler

def run():
  if PROMPT is not None:
    print("\nInput:")
    transcription = input()

  else:
    # Record Speech
    filename = record_service.record()
    #filename = 'myrecording.wav'

    # Translate to Text using Whisper
    transcription = chatgpt_service.speech_to_text(filename)

  # Call ChatGPT
  response, function_call = chatgpt_service.call_chatgpt(user_input=transcription)

  while chatgpt_service.function_called:
    # TODO: call a validation with all the arguments 
    # - for example: I'm about to create the following event:
    # - are you sure?

    # TODO: put default values for most arguments so that the functions are executed properly

    function_result = function_service.call_function(function_call)
    logging.debug(f"Function Result: {function_result}")

    if function_result is None:
       logging.error(f"Function {function_call['name']} wasn't called correctly")
       exit(-1)
    else:
      response, function_call = chatgpt_service.callback_chatgpt_with_function_results(function_call["name"], function_result)

  eleven_labs_service.text_to_speech(text=response)

if __name__ == "__main__":

  LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
  if LOG_LEVEL not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']: LOG_LEVEL = 'INFO'
  LogHandler(LOG_LEVEL)

  PROMPT = os.getenv("PROMPT", None)
  LANGUAGE = os.getenv("LANGUAGE", "en")
  MODEL = os.getenv("MODEL", "eleven_multilingual_v2")
  NAME = os.getenv("NAME", None)
  VOICE_ID = "EXAVITQu4vr4xnSDxMaL" if NAME is None else get_voice_id(NAME)
  FUNCTIONS = get_available_functions_from_json("src/aux/json/functions.json")

  OPENAI_API_KEY = open_file('openaiapikey.txt')
  EL_API_KEY = open_file('elevenlabsapikey.txt')

  logging.info(f"Starting Olivia Oracle with Language {LANGUAGE} and Model {MODEL}")

  # TODO: create another file that handles instantiating those classes
  authentication_service = AuthenticationService()
  context_manager_service = ContextManagerService(LANGUAGE)
  context = context_manager_service.get_context()

  record_service = RecordService(duration=7, fs=44100, channels=2)
  function_service = FunctionService()
  google_manager = GoogleManager(function_service, authentication_service)

  chatgpt_service = ChatGPTService(openai_api_key=OPENAI_API_KEY, context=context, functions=FUNCTIONS)
  eleven_labs_service = ElevenLabsService(voice_id=VOICE_ID, api_key=EL_API_KEY, model=MODEL)

  while True:
    run()