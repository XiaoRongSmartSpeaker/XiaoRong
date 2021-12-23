import speech_recognition as sr
from textblob import TextBlob
from gtts import gTTS
import os
from pygame import mixer
import time
import librosa

class Translate:
    def translate(fromLanguage='zh-TW', toLanguage='en'):
        while True:
            #是否按下按鈕

            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print("Say something!")
                    if r.energy_threshold<9000:
                        r.energy_threshold=9000
                    r.pause_threshold=1
                    audio=r.listen(source,timeout=10)

                sttTXT_org = r.recognize_google(audio, language = fromLanguage)
                print(sttTXT_org)

                sttTXT_tblob = TextBlob(sttTXT_org)
                blobTranslated = sttTXT_tblob.translate(to=toLanguage)
                print('Translated: ' + blobTranslated.raw)

                tts = gTTS(blobTranslated.raw, lang=toLanguage)
                tts.save('temp.mp3')
                
                s=librosa.get_duration(filename='./temp.mp3')
                mixer.init()
                mixer.music.load('./temp.mp3')
                mixer.music.play(1)
                time.sleep(s)
                os.system('rm temp.mp3')
                
            except sr.UnknownValueError:
                mixer.init()
                mixer.music.load('./Audio/dontKnow.mp3')
                mixer.music.play()
                time.sleep(3)
                pass

            except sr.RequestError:
                mixer.init()
                mixer.music.load('./Audio/noInternet.mp3')
                mixer.music.play()
                time.sleep(2)
            
            except sr.WaitTimeoutError:
                print('No voice')
                continue

#Translate.translate() 