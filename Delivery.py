#import numpy as np
import wave
#import sys
import pyaudio
import requests
import time
import struct
import math

# server的東東
ServerPath = "http://b298-2001-b400-e734-a52e-74ee-cb06-d9e5-ce53.ngrok.io/delivery"

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


"""
CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3
"""
# 看裝置
INPUT_DEVICE = 9
WAVE_OUTPUT_FILENAME = "memorandum.wav"
# 计算当前音频声音
swidth = 2
SHORT_NORMALIZE = (1.0/32768.0)


def rms(frame):
    count = len(frame) / swidth
    format = "%dh" % (count)
    shorts = struct.unpack(format, frame)

    sum_squares = 0.0
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)
    return rms * 1000


class Memorandum:
    def memorandum(self, file_name):
        CHUNK = 512
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        MAX_RECORD_SECONDS = 300
        TIMEOUT_LENGTH = 2  # 音量小于一定时间后停止录音

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=2,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("开始录音...")

        frames = []

        endTime = time.time() + MAX_RECORD_SECONDS  # 超过此时间自动停止
        lastTime = time.time()

        while True:
            if lastTime < endTime:

                input = stream.read(CHUNK)
                frames.append(input)

                # 声音大小，小于音量后超过多少秒停止 / 超过多长时间停止
                rms_val = rms(input)  # 当前音量
                # print(rms_val)
                if rms_val > 1:  # 如果说话了（音量大于 1）就更新时间
                    lastTime = time.time()

                if time.time() - lastTime > TIMEOUT_LENGTH:     # 超过一定时间不说话，停止录音
                    break

            else:   # 超时停止
                break

        print("录音结束")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(file_name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print("保存文件成功")


if __name__ == "__main__":
    delivery = Delivery()
    memorandum = Memorandum()
    print("start")
    """
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
    """
    """
    pa = pyaudio.PyAudio()
    for i in range (0,pa.get_device_count()-1):
        print("id:" + str(i))
        print(pa.get_device_info_by_index(i))
    """

    #delivery.deliver_to_cellphone(searchResultURL, searchKeyWord, userLINEID)
    memorandum.memorandum(WAVE_OUTPUT_FILENAME)
    # app.run()
# /usr/include/portaudio.h
"""
pip install --global-option='build_ext' --global-option='-I/usr/include' --global-option='-L/usr/lib' pyaudio

pyaudio.pa.__file__
'/home/wago/.local/lib/python3.8/site-packages/_portaudio.cpython-38-x86_64-linux-gnu.so'

sudo find / -name "_portaudio.so"


"""
