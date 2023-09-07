import re
import requests
from pydub import AudioSegment
from pydub.playback import play

class ElevenLabsService:
  def __init__(self, voice_id, api_key, model):
    self.voice_id = voice_id
    self.api_key = api_key
    self.model = model

  def text_to_speech(self, text):
    text = re.sub(r'(Response:|Narration:|Image: generate_image:.*|)', '', text).strip()
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}'
    headers = {
        'Accept': 'audio/mpeg',
        'xi-api-key': self.api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'text': text,
        'model_id': self.model,
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

