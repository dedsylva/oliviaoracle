# OliviaOracle - A Simple Assistant

<p align="center">
  <img width="80%" height="80%" src="assets/logo.jpeg">
</p>


## How to Use

### Setups
* Install dependencies
    * pip3 install -r requirements.txt
* Paste Open AI API key into file openaiapikey.txt
* Paste Eleven Labs API key into file elevenlabsapikey.txt

### Debugging

```bash
# for not using voice, but typing
cd olivia
PROMPT=1 ./main.py

# for changing log_level (default is info)
cd olivia
LOG_LEVEL=DEBUG ./main.py
```

### Running
```bash
# for default settings (english language)
cd olivia
./main.py 

# for portuguese language
cd olivia
LANGUAGE=pt ./main.py 
```

### Ubuntu Requirements
 - ffmpeg


### Docker
 - Soon


### Technical Details

Speech To Text
 - [Whisper](https://openai.com/research/whisper)

Text to Speech
 - [Elevenlabs](https://elevenlabs.io/)


ElevenLabs Docs
 - https://api.elevenlabs.io/docs

OpenAI Docs
 - https://platform.openai.com/docs/api-reference 


## Features

- English and Portuguese Language 
  - if you want to add more languages, all you need to do is to add it in the ContextManagerService and add a context_lg.txt with the context story for your personal assistant (see context_en.txt for an example).

- Integration with Google Calendar
  - You can <b>add</b> new events or <b>check</b> events on your google calendar. When creating a new event please ask for the assistant which data it needs to create the event.
  - Example prompt for creating an event: 
    - Hi! please create the following event on my calendar! summary: test, location: home, description: test, start and time: october 3 2023 at 12, end date and time: october 3 2023 at 13

## Inspiration
This project began as inspiration of [this project](https://github.com/AllAboutAI-YT/talk-to-chatgpt) which has a demo on [this youtube video](https://www.youtube.com/watch?v=bZhgoYrHC3w&ab_channel=AllAboutAI)
