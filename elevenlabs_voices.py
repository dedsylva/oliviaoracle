import json

def get_voice_id(name):

    f = open("elevenlabs_voices.json")
    voices = json.load(f)["voices"]

    # next can be used when you create a list comprehension but always returns one value
    return next(v["voice_id"] for v in voices if v["name"] == name)