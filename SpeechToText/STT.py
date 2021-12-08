import speech_recognition as sr
from pygame import mixer
import time
#import model.mic_vad_streaming as mvs
from pypinyin import pinyin,Style

class SpeechToText:
    def Voice_To_Text():
        cnt = 0
        cmd = False
        while True:
            # add thread
            r = sr.Recognizer()

            with sr.Microphone() as source:
                #r.adjust_for_ambient_noise(source, duration=1)
                print("Say something!")
                r.energy_threshold=9000
                r.pause_threshold=1
                audio=r.listen(source,timeout=10,phrase_time_limit=5)
            
            zh_text = ""
            try:
                zh_text = r.recognize_google(audio, language="zh-TW")
                print(zh_text)
                z = pinyin(zh_text, style=Style.BOPOMOFO)
                s=''
                for e in z:
                    s+=e[0]
                #print(s)
                if 'ㄋㄧˇㄏㄠˇㄒㄧㄠˇㄌㄨㄥˊ' in s or 'ㄋㄧˇㄏㄠˇㄒㄧㄠˇㄖㄨㄥˊ' in s or 'ㄋㄧˇㄏㄠˇㄒㄧㄠˇㄖㄡˊ' in s or 'ㄋㄧˇㄏㄠˇㄒㄧㄠˇㄌㄡˊ' in s or 'ㄋㄧˇㄏㄠˇㄒㄧㄠˇㄖㄣˊ' in s:
                    mixer.init()
                    mixer.music.load('./Audio/what.mp3')
                    mixer.music.play()
                    time.sleep(1)
                    cmd=True
                    continue
                elif not cmd:
                    continue
                else:
                    #等失衡跟我說怎麼傳
                    print('return',zh_text)
                    cmd=False

            except sr.RequestError:
                if cmd:
                    mixer.init()
                    mixer.music.load('./Audio/noInternet.mp3')
                    mixer.music.play()
                    time.sleep(2)

            except sr.UnknownValueError:
                if cmd:
                    mixer.init()
                    mixer.music.load('./Audio/dontKnow.mp3')
                    mixer.music.play()
                    time.sleep(3)
                    cnt+=1
                    if cnt==3:
                        cnt=0
                        cmd=False
                        continue
                    mixer.music.load('./Audio/again.mp3')
                    mixer.music.play()
                    time.sleep(2)
                else:
                    print('exceed 10s')

            except sr.WaitTimeoutError:
                print('No voice')
                continue

#SpeechToText.Voice_To_Text()