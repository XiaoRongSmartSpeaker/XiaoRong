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
                    end_message = gTTS('翻譯已結束', lang='zh-TW')
                    end_message.save(f'{os.path.dirname(__file__)}/Audio/temp.mp3')
                    s=librosa.get_duration(filename=f'{os.path.dirname(__file__)}/Audio/temp.mp3')
                    mixer.init()
                    mixer.music.load(f'{os.path.dirname(__file__)}/Audio/temp.mp3')
                    mixer.music.play(1)
                    time.sleep(s)
                    os.system(f'rm {os.path.dirname(__file__)}/Audio/temp.mp3')
                    break
                
                sttTXT_tblob = TextBlob(sttTXT_org)
                try:
                    blobTranslated = sttTXT_tblob.translate(to=toLanguage)
                except:
                    print('not translated')
                    continue
                print('Translated: ' + blobTranslated.raw)

                tts = gTTS(blobTranslated.raw, lang=toLanguage)
                tts.save(f'{os.path.dirname(__file__)}/Audio/temp.mp3')
                
                s=librosa.get_duration(filename=f'{os.path.dirname(__file__)}/Audio/temp.mp3')
                mixer.init()
                mixer.music.load(f'{os.path.dirname(__file__)}/Audio/temp.mp3')
                mixer.music.play(1)
                time.sleep(s)
                os.system(f'rm {os.path.dirname(__file__)}/Audio/temp.mp3')
                
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