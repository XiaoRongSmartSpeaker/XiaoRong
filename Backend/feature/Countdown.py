from logging import Manager
import time
from pygame import mixer
import sys
try:
    import logger
    logger = logger.get_logger(__name__)
except ModuleNotFoundError:
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


class Countdown():
    def __init__(self):
        self.totalSeconds = 0
        self.audioFile = 'feature/sound.mp3'
        self.threadHandler = None
        self.isCounting = False
        self.isPlayingAudio = False
        self.audioSec = 150
        return

    def import_thread(self, thread):
        self.threadHandler = thread
        return

    def set_timer(self, h: int, m: int, s: int):
        if h is None:
            h = 0
        if m is None:
            m = 0
        if s is None:
            s = 0
        if h < 0 or m < 0 or s < 0:
            return False
        totalSeconds = s + m * 60 + h * 3600
        if 0 <= totalSeconds <= 7200:
            self.totalSeconds = totalSeconds
            self.isCounting = True
            # sentence = '設定成功'.format(h, m, s)
            # self.threadHandler.add_thread({
            # 	'class': 'TextToSpeech',
            # 	'func': 'text_to_voice',
            # 	'args': (sentence,)
            # 	})
            # time.sleep(3)
            logger.debug('設定計時{}:{}:{}'.format(h, m, s))
            self.threadHandler.add_thread({
                'class': 'Countdown',
                'func': 'start_countdown',
            })
            return True
        return False

    def start_countdown(self):
        while self.totalSeconds and self.isCounting:
            # m, s = divmod(self.totalSeconds, 60)
            # h, m = divmod(m, 60)
            # timeFormat = '{:02d}:{:02d}:{:02d}'.format(h, m, s)
            # print(timeFormat)
            time.sleep(1)
            self.totalSeconds -= 1
        if self.isCounting:
            self.isPlayingAudio = True
            logger.debug('time up')
            # self.threadHandler.add_thread({
            # 	'class': 'TextToSpeech',
            # 	'func': 'text_to_voice',
            # 	'args': ('計時時間到',)
            # 	})
            mixer.init()
            mixer.music.load(self.audioFile)
            mixer.music.play(1)
            while self.isPlayingAudio and self.audioSec:
                self.audioSec -= 1
                time.sleep(1)
            logger.info('end of ring')
            self.audioSec = 150
            self.isPlayingAudio = False
            mixer.music.stop()
        else:
            logger.info('Cancel countdown')
            self.threadHandler.add_thread({
                'class': 'TextToSpeech',
                'func': 'text_to_voice',
                'args': ('取消倒計時',)
            })
        return True

    def stop_countdown(self):
        self.isCounting = False
        return

    def stop_ringing(self):
        # playsound(None)
        self.isPlayingAudio = False
        return
    # def play_ring(self):
    # 	# playsound(self.audioFile)

# if __name__ == "__main__":
#     a = Countdown()
#     h, m, s = map(int, input("輸入到計時時間（格式：hh:mm:ss）").split(":"))
#     if a.set_countdown(h, m, s) == False:
#         print('error time!')
