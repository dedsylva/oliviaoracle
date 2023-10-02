import logging
import json
import calendar

def open_file(filepath):
  logging.debug(f"Opening {filepath}")

  with open(filepath, 'r', encoding='utf-8') as infile:
    return infile.read()

def get_voice_id(name):
  logging.debug(f"Getting Voice ID for {name}")

  f = open("elevenlabs_voices.json")
  voices = json.load(f)["voices"]

  # next can be used when you create a list comprehension but always returns one value
  return next(v["voice_id"] for v in voices if v["name"] == name)

def get_month_name(n): return calendar.month_name[1:][int(n)-1]

def get_available_functions_from_json(f): 
  logging.debug("Getting Available Functions from JSON File")
  return json.load(open(f))
