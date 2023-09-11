import openai

class ChatGPTService:
  def __init__(self, openai_api_key, context, temperature=0.9, frequency_penalty=0.2, presence_penalty=0, functions=[]):
    self.openai_api_key = openai_api_key
    self.context = context
    self.temperature = temperature
    self.frequency_penalty = frequency_penalty
    self.presence_penalty = presence_penalty

    self.functions = functions
    self.function_called = False

    self.conversation = [{"role": "system","content": self.context}]

  def speech_to_text(self, filename):
    with open(filename, "rb") as file:
      openai.api_key = self.openai_api_key
      result = openai.Audio.transcribe("whisper-1", file)
    transcription = result['text']
    return transcription

  def call_chatgpt(self, user_input, function=None):
    if function is not None:
      self.functions.append(function)

    openai.api_key = self.openai_api_key

    self.conversation.append({"role": "user","content": user_input})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        temperature=self.temperature,
        frequency_penalty=self.frequency_penalty,
        presence_penalty=self.presence_penalty,
        messages=self.conversation,
        functions=self.function)

    chat_response = completion['choices'][0]['message']

    if chat_response.get("function_call"):
      self.conversation.append({"role": "assistant", "content": chat_response["content"], "function_call": chat_response["function_call"]})
      self.function_called = True
    else:
      self.conversation.append({"role": "assistant", "content": chat_response["content"]})
      self.function_called = False

    return chat_response["content"], chat_response["function_call"]
