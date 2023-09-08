import openai

class ChatGPTService:
  def __init__(self, openai_api_key, context, temperature=0.9, frequency_penalty=0.2, presence_penalty=0):
    self.openai_api_key = openai_api_key
    self.context = context
    self.temperature = temperature
    self.frequency_penalty = frequency_penalty
    self.presence_penalty = presence_penalty
    self.conversation = []

  def speech_to_text(self, filename):
    with open(filename, "rb") as file:
      openai.api_key = self.openai_api_key
      result = openai.Audio.transcribe("whisper-1", file)
    transcription = result['text']
    return transcription

  def call_chatgpt(self, user_input):
    openai.api_key = self.openai_api_key

    self.conversation.append({"role": "user","content": user_input})

    messages_input = self.conversation.copy()

    prompt = [{"role": "system", "content": self.context}]
    messages_input.insert(0, prompt[0])

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        temperature=self.temperature,
        frequency_penalty=self.frequency_penalty,
        presence_penalty=self.presence_penalty,
        messages=messages_input)

    chat_response = completion['choices'][0]['message']['content']
    self.conversation.append({"role": "assistant", "content": chat_response})
    return chat_response


