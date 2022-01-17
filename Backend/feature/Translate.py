from typing import Text
import speech_recognition as sr
from textblob import TextBlob
from gtts import gTTS
import os
from pygame import mixer
import time
import librosa
from TextToSpeech import TextToSpeech

class Translate:
    def __init__(self):
        pass

    def translate(self, fromLanguage='zh-TW', toLanguage='en'):
        while True:
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print("Say something!")
                    if r.energy_threshold<8000:
                        r.energy_threshold=8000
                    r.pause_threshold=1
                    audio=r.listen(source,timeout=10)

                sttTXT_org = r.recognize_google(audio, language = 'zh-TW')
                # cmd = r.recognize_google(audio, language='zh-TW')
                print(sttTXT_org)
                if '結束翻譯' in sttTXT_org:
                    TextToSpeech.text_to_voice('翻譯已結束','zh-TW')
                    break
                
                sttTXT_tblob = TextBlob(sttTXT_org)
                try:
                    blobTranslated = sttTXT_tblob.translate(to=toLanguage)
                except:
                    print('not translated')
                    continue
                print('Translated: ' + blobTranslated.raw)
                TextToSpeech.text_to_voice(blobTranslated.raw, toLanguage)
                
            except sr.UnknownValueError:
                mixer.init()
                mixer.music.load(f'{os.path.dirname(__file__)}/Audio/dontKnow.mp3')
                mixer.music.play()
                time.sleep(3)
                pass

            except sr.RequestError:
                mixer.init()
                mixer.music.load(f'{os.path.dirname(__file__)}/Audio/noInternet.mp3')
                mixer.music.play()
                time.sleep(2)
                break
            
            except sr.WaitTimeoutError:
                print('No voice')
                continue

if __name__=="__main__":
    Translate.translate() 