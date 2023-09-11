import json
import calendar
from src.management.Functions import Functions

def open_file(filepath):
  with open(filepath, 'r', encoding='utf-8') as infile:
    return infile.read()


def get_voice_id(name):

    f = open("elevenlabs_voices.json")
    voices = json.load(f)["voices"]

    # next can be used when you create a list comprehension but always returns one value
    return next(v["voice_id"] for v in voices if v["name"] == name)

def get_month_name(n): return calendar.month_name[1:][int(n)-1]

def get_available_functions_from_json(f): return json.load(open(f))

def get_available_functions() -> list[Functions]: return Functions()._get()

def call_function(function_call):
   available_functions = get_available_functions()
   for af in available_functions:
    if af.name == function_call["name"]:
      function = af.value
      args = {a: function_call["arguments"].get(a) for a in af.args}
      function(**args)

