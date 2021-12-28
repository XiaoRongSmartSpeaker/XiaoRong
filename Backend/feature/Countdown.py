from logging import Manager
import time
import playsound
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
		self.audioFile = 'sound.mp3'  
		self.threadHandler = None  
		self.isCounting = False                         
		return
	def import_thread(self, thread):
		self.threadHandler = thread
		return
	def set_countdown(self, h: int, m: int, s: int):
		if h < 0 or m < 0 or s < 0:
			return False
		totalSeconds = s + m * 60 + h * 3600
		if 0 <= totalSeconds <= 7200:
			self.totalSeconds = totalSeconds
			self.isCounting = True
			self.threadHandler.add_thread({
                'class': 'Countdown',
                'func': 'start_countdown',
            })
			return True
		return False
	def start_countdown(self):
		while self.totalSeconds and self.isCounting:
			m, s = divmod(self.totalSeconds, 60)
			h, m = divmod(m, 60)
			timeFormat = '{:02d}:{:02d}:{:02d}'.format(h, m, s)
			print(timeFormat)
			time.sleep(1)
			self.totalSeconds -= 1
		if self.isCounting:
			logger.debug('Time\'s up')
			playsound.playsound(self.audio_file, True) 
			time.sleep(150)
			logger.debug('end of ring')
		else:
			logger.debug('Cancel countdown')
		return True
	def stop_countdown(self):
		self.isCounting = False
		return
	def stop_ringing(self):
		playsound.playsound(None, True)
		return
		
if __name__ == "__main__":
    a = Countdown()
    h, m, s = map(int, input("輸入到計時時間（格式：hh:mm:ss）").split(":"))
    if a.set_countdown(h, m, s) == False:
        print('error time!')
