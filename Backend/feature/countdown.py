from logging import Manager
import time
import playsound
import sys
import os
scriptpath = "../"
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

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))
from Threading import Job
class countdown():
	def __init__(self):
		self.totalSeconds = 0  
		self.audio_file = 'sound.mp3'                             
		return
		
	def set_countdown(self, h: int, m: int, s: int):
		if h < 0 or m < 0 or s < 0:
			return False
		totalSeconds = s + m * 60 + h * 3600
		if 0 <= totalSeconds <= 7200:
			self.totalSeconds = totalSeconds
			self.start_countdown()
			return True
		
		return False
	def start_countdown(self):
		while self.totalSeconds:
			m, s = divmod(self.totalSeconds, 60)
			h, m = divmod(m, 60)
			timeFormat = '{:02d}:{:02d}:{:02d}'.format(h, m, s)
			print(timeFormat)
			time.sleep(1)
			self.totalSeconds -= 1
		logger.debug('Time\'s up')
		playsound.playsound(self.audio_file, True) 
		time.sleep(150)
		logger.debug('end of ring')
		return True
	def stop_countdown(self):
		pass
		 
if __name__ == "__main__":
	a = countdown()
	h, m, s = map(int,input("輸入到計時時間（格式：hh:mm:ss）").split(":"))
	if a.set_countdown(h, m, s) == False:
		print('error time!')
