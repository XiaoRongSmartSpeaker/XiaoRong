from logging import Manager
import time
import multiprocessing
from playsound import playsound
import sys
import json

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


class Alarm():
	def __init__(self):
		self.alarmList = []
		self.audioFile = 'sound.mp3'  
		self.threadHandler = None  
		self.alarmListFile = 'AlarmList.json'
		self.isPlayingAudio = False  
		self.playingAudio = None  
		self.audioSec = 150              
		return
	def import_thread(self, thread):
		self.threadHandler = thread
		return

	def get_alarm_list(self):
		jsonContent = {}
		with open( "AlarmList.json", encoding="utf-8") as f:
			jsonContent = f.read()
		jsonContent = json.loads(jsonContent)
		# 取得 json "AlarmList" 欄位
		try:
			self.alarmList = jsonContent["AlarmList"]  
		except:
			self.alarmList = []
	def set_alarm(self, day: int, h: int, m: int):
		if not 1 <= day <= 7:
			logger.debug('Error day')
			return False
		elif not 0 <= h < 24:
			logger.debug('Error hour')
			return False
		elif not 0 <= m < 60:
			logger.debug('Error minute')
			return False
		self.alarmList.append({"day": day, "hour": h, "minute": m})
		self.save_alarm_list()
		return
	def save_alarm_list(self):
		with open(self.alarmListFile, mode="w", encoding="utf-8") as f:
			json.dump({"AlarmList":self.alarmList}, f, ensure_ascii=False)
		return None
	def start_alarm(self):
		while True:
			t = time.localtime()
			now = {"day": t.tm_wday + 1, "hour": t.tm_hour, "minute": t.tm_min}
			for setTime in self.alarmList:
				if now == setTime:
					logger.info('Alarm time')
					self.isPlayingAudio = True
					self.play_ring()
					while self.isPlayingAudio and self.audioSec:
						self.audioSec -= 1
						time.sleep(1)
					self.audioSec = 150
					self.isPlayingAudio = False
					logger.info('end of ring')
					self.playingAudio.terminate()
					break
			time.sleep(1)

	def play_ring(self):
		self.playingAudio = multiprocessing.Process(target=playsound, args=(self.audioFile,))
		self.playingAudio.start()
	def main(self):
		self.get_alarm_list()
		self.threadHandler.add_thread({
			'class': 'Alarm',
			'func': 'start_alarm',
		})
	def stop_ringing(self):
		self.isPlayingAudio = False
		return
if __name__ == "__main__":
	a = Alarm()
	day, h, m = map(int, input("輸入鬧鐘時間（格式：星期(1-7):hh:mm）").split(":"))
	a.main()
	if a.set_alarm(day, h, m) == False:
		print('error time!')
	time.sleep(30)
	a.stop_ringing()