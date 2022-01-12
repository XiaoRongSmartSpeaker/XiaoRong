from gtts import gTTS
from pygame import mixer
import time
import librosa
import os


class TextToSpeech:
    def text_to_voice(sentence):
        tts = gTTS(text=sentence, lang='zh-TW')
        tts.save(f'{os.path.dirname(__file__)}/Audio/temp.mp3')
        s = librosa.get_duration(filename=f'{os.path.dirname(__file__)}/Audio/temp.mp3')
        # print(s)
        mixer.init()
        mixer.music.load(f'{os.path.dirname(__file__)}/Audio/temp.mp3')
        mixer.music.play(1)
        time.sleep(s)
        os.system(f'rm {os.path.dirname(__file__)}/Audio/temp.mp3')
