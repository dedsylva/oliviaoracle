#! /usr/bin/python3

import sounddevice as sd
import soundfile as sf
import openai
import os
import requests
import re
from colorama import Fore, Style, init
from pydub import AudioSegment
from pydub.playback import play
from elevenlabs_voices import get_voice_id

init()

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def chatgpt(api_key, conversation, context, user_input, temperature=0.9, frequency_penalty=0.2, presence_penalty=0):
    openai.api_key = api_key
    conversation.append({"role": "user","content": user_input})
    messages_input = conversation.copy()
    prompt = [{"role": "system", "content": context}]
    messages_input.insert(0, prompt[0])
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messages_input)
    chat_response = completion['choices'][0]['message']['content']
    conversation.append({"role": "assistant", "content": chat_response})
    return chat_response

def text_to_speech(text, voice_id, api_key, MODEL):
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
    headers = {
        'Accept': 'audio/mpeg',
        'xi-api-key': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'text': text,
        'model_id': MODEL,
        'voice_settings': {
            'stability': 0.6,
            'similarity_boost': 0.85
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open('output.mp3', 'wb') as f:
            f.write(response.content)
        audio = AudioSegment.from_mp3('output.mp3')
        play(audio)
    else:
        print('Error:', response.text)

def print_colored(agent, text):
    agent_colors = {
        "Julie:": Fore.YELLOW,
    }
    color = agent_colors.get(agent, "")
    print(color + f"{agent}: {text}" + Style.RESET_ALL, end="")

def record(duration=5, fs=44100):
    print('Recording...')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    print('Recording complete.')
    filename = 'myrecording.wav'
    sf.write(filename, myrecording, fs)

    return filename

def speach_to_text(filename):
    with open(filename, "rb") as file:
        openai.api_key = OPENAI_API_KEY
        result = openai.Audio.transcribe("whisper-1", file)
    transcription = result['text']
    return transcription

def run(context):

    conversation = []  
    while True:
        # Record Speech
        #filename = record()

        # Translate to Text using Whisper
        #transcription = speach_to_text(filename)

        # Call ChatGPT
        #response = chatgpt(OPENAI_API_KEY, conversation, context, transcription)
        response = "Olá Tadeu! Estou bem, obrigada por perguntar. Como você tem se sentido ultimamente?"

        print_colored("Julie:", f"{response}\n\n")
        user_message_without_generate_image = re.sub(r'(Response:|Narration:|Image: generate_image:.*|)', '', response).strip()

        text_to_speech(user_message_without_generate_image, VOICE_ID, EL_API_KEY, MODEL)

if __name__ == "__main__":
    LANGUAGE = os.getenv("LANGUAGE", "en")
    MODEL = os.getenv("MODEL", "eleven_multilingual_v2")
    NAME = os.getenv("NAME", None) 
    VOICE_ID = "EXAVITQu4vr4xnSDxMaL" if NAME is None else get_voice_id(NAME)

    OPENAI_API_KEY = open_file('openaiapikey.txt')
    EL_API_KEY = open_file('elevenlabsapikey.txt')

    if LANGUAGE == "en":
        CONTEXT_FILE = "chatbot_en.txt"
    elif LANGUAGE == "pt":
        CONTEXT_FILE = "chatbot_pt.txt"
    else:
        raise ValueError(f"Invalid Context. We currently support en (english) and pt (brazililian portuguese), but got {LANGUAGE} language")


    context = open_file(CONTEXT_FILE)

    run(context)