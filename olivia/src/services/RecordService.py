import logging
import sounddevice as sd
import soundfile as sf

class RecordService:
  def __init__(self, duration=5, fs=44100, channels=2):
    self.duration = duration
    self.fs = fs
    self.channels = channels

    logging.debug(f"Instantiating RecordService")

  def record(self):
      logging.info('Recording...')
      print('Recording...')

      myrecording = sd.rec(int(self.duration * self.fs), samplerate=self.fs, channels=self.channels)
      sd.wait()

      logging.info('Recording complete.')
      print('Recording complete.')

      filename = 'myrecording.wav'
      sf.write(filename, myrecording, self.fs)

      return filename

