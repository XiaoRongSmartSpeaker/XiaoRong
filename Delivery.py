import wave
import pyaudio
import requests
import time
import struct
import math

# server的id

ServerPath = "https://2c9c-140-122-136-85.ngrok.io/"

# 假設搜尋結果長這樣
searchResultURL = 'https://www.google.com/search?q=%E5%BE%AE%E7%A9%8D%E5%88%86&oq=%E5%BE%AE%E7%A9%8D%E5%88%86&aqs=chrome..69i57j0i131i433i512j0i512l8.1211j0j7&sourceid=chrome&ie=UTF-8'
searchKeyWord = '微積分'
# 從DB拿userLINEID
userLINEID = 'Uc6e3d440bfe6da66232ce9005b34b375'


class Delivery:

    def deliver_to_cellphone(self, resultURL, keyWord, userId):
        # 把東西給server
        # userId如果沒有，就是空字串
        r = requests.post(
            ServerPath+"delivery", data={'data': resultURL + ' ' + keyWord + ' ' + userId})


# 要測過才能確定INPUT_DEVICE
INPUT_DEVICE = 9
WAVE_OUTPUT_FILENAME = "memorandum.m4a"

swidth = 2
SHORT_NORMALIZE = (1.0/32768.0)

# 回傳音量


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

    def deliver_memorandum(self, file_name, userId, timeLen):
        if userId == "":
            return 0
        Time = time.localtime()
        request_time = "語音備忘錄\n時間: " + str(Time.tm_mon) + "/" + str(Time.tm_mday) + \
            " " + str(Time.tm_hour) + ":" + str(Time.tm_min)
        """
        把東西給server
        userId如果沒有，就是空字串
        如果file不在當前目錄，就要再改
        """
        files = {WAVE_OUTPUT_FILENAME: (file_name, open(file_name, 'rb'))}
        values = [('time', request_time),
                  ('name', file_name), ('len', timeLen)]
        r = requests.post(
            ServerPath+"memorandum", data=values, files=files)

    def memorandum(self, file_name):
        CHUNK = 512
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 16000
        MAX_RECORD_SECONDS = 300
        TIMEOUT_LENGTH = 3  # 不說話多久停止錄音

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=2,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        # 告訴使用者錄音開始
        # print("开始錄音")

        frames = []
        frames_rms = []

        endTime = time.time() + MAX_RECORD_SECONDS
        lastTime = time.time()
        startTime = time.time()
        max_value = 4

        while True:
            if lastTime < endTime:

                input = stream.read(CHUNK)
                frames.append(input)

                rms_val = rms(input)
                frames_rms.append(rms_val)
                if rms_val > max_value:
                    lastTime = time.time()

                if time.time() - lastTime > TIMEOUT_LENGTH:
                    break

            else:
                break

        # 告訴使用者錄音結束
        # print("錄音結束")
        timeLen = time.time() - startTime

        while len(frames_rms) and frames_rms[-1] <= max_value/2:
            frames.pop()
            frames_rms.pop()
            timeLen -= 1/RATE

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(file_name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        # print("保存文件成功")
        # 傳給使用者，但我要怎麼拿到userId
        memorandum.deliver_memorandum(file_name, userLINEID, timeLen)
        # return 0


if __name__ == "__main__":
    delivery = Delivery()
    memorandum = Memorandum()
    memorandum.memorandum(WAVE_OUTPUT_FILENAME)
    """
    print("start")
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ",
                    p.get_device_info_by_host_api_device_index(0, i).get('name'))
        pa = pyaudio.PyAudio()
        for i in range(0, pa.get_device_count()-1):
            print("id:" + str(i))
            print(pa.get_device_info_by_index(i))

    # delivery.deliver_to_cellphone(searchResultURL, searchKeyWord, userLINEID)
    memorandum.deliver_memorandum(WAVE_OUTPUT_FILENAME, userLINEID, 4000)
    # memorandum.memorandum(WAVE_OUTPUT_FILENAME)
    # app.run()
# /usr/include/portaudio.h
"""
