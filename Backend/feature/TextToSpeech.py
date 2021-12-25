from gtts import gTTS
from pygame import mixer
import time
import librosa
import os

class TextToSpeech:
    def text_to_voice(sentence):
        tts=gTTS(text=sentence, lang='zh-TW')
        tts.save('temp.mp3')
        s=librosa.get_duration(filename='./temp.mp3')
        #print(s)
        mixer.init()
        mixer.music.load('./temp.mp3')
        mixer.music.play(1)
        time.sleep(s)
        os.system('rm temp.mp3')
