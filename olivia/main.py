#! /usr/bin/python3

import os
from colorama import Fore, Style, init
from src.services.ContextManagerService import ContextManagerService
from src.services.RecordService import RecordService
from src.services.ChatGPTService import ChatGPTService
from src.services.ElevenLabsService import ElevenLabsService
from src.entities.google.GoogleManager import GoogleManager
from src.aux.utils import get_voice_id, open_file, get_available_functions_from_json, call_function, get_available_functions 

init()

def print_colored(agent, text):
    agent_colors = {
        "Julie:": Fore.YELLOW,
    }
    color = agent_colors.get(agent, "")
    print(color + f"{agent}: {text}" + Style.RESET_ALL, end="")

def run():
  # Record Speech
  filename = record_service.record()

  # Translate to Text using Whisper
  transcription = chatgpt_service.speech_to_text(filename)

  # Call ChatGPT
  response, function_call = chatgpt_service.call_chatgpt(user_input=transcription)

  if chatgpt_service.function_called:
    call_function(function_call)

  # TODO: replace print with log
  print_colored("Julie:", f"{response}\n\n")

  eleven_labs_service.text_to_speech(text=response)

if __name__ == "__main__":
    LANGUAGE = os.getenv("LANGUAGE", "en")
    MODEL = os.getenv("MODEL", "eleven_multilingual_v2")
    NAME = os.getenv("NAME", None) 
    VOICE_ID = "EXAVITQu4vr4xnSDxMaL" if NAME is None else get_voice_id(NAME)
    FUNCTIONS = get_available_functions_from_json("src/aux/json/functions.json")

    OPENAI_API_KEY = open_file('openaiapikey.txt')
    EL_API_KEY = open_file('elevenlabsapikey.txt')

    # TODO: create another file that handles stantiating those classes
    # TODO: make those classes singleton
    context_manager_service = ContextManagerService(LANGUAGE)
    record_service = RecordService(duration=5, fs=44100, channels=2)

    context = context_manager_service.get_context()

    chatgpt_service = ChatGPTService(openai_api_key=OPENAI_API_KEY, context=context, functions=FUNCTIONS)
    eleven_labs_service = ElevenLabsService(voice_id=VOICE_ID, api_key=EL_API_KEY, model=MODEL)
    google_manager = GoogleManager()

    while True:
      run()