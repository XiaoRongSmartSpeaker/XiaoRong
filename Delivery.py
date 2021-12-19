#import numpy as np
from linebot.models import *
import wave
#import sys
import pyaudio
import requests

# server的東東
ServerPath = "http://b298-2001-b400-e734-a52e-74ee-cb06-d9e5-ce53.ngrok.io/delivery"

# 看server那邊的json檔要放哪裡
# 假設搜尋結果長這樣
searchResultURL = 'https://www.google.com/search?q=%E5%BE%AE%E7%A9%8D%E5%88%86&oq=%E5%BE%AE%E7%A9%8D%E5%88%86&aqs=chrome..69i57j0i131i433i512j0i512l8.1211j0j7&sourceid=chrome&ie=UTF-8'
userLINEID = 'Uc6e3d440bfe6da66232ce9005b34b375'
searchKeyWord = '微積分'


class Delivery:

    def deliver_to_cellphone(self, resultURL, keyWord, userId):
        # 把東西給server
        # userId如果沒有，就是空字串
        r = requests.post(
            ServerPath, data={'data': resultURL + ' ' + keyWord + ' ' + userId})
    # fin


CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"


class Memorandum:

    def memorandum(self):
        print("memorandum")
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print("recording...")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("done")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


if __name__ == "__main__":
    delivery = Delivery()
    memorandum = Memorandum()
    print("start")
    delivery.deliver_to_cellphone(searchResultURL, searchKeyWord, userLINEID)
    # memorandum.memorandum()
    # app.run()
