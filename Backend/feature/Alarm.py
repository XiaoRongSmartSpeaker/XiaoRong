from logging import Manager
import time

import playsound
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
		return
	def import_thread(self, thread):
		self.threadHandler = thread
		return

	def get_alarm_list():
		with open( "AlarmList.json", encoding="utf-8") as f:
			jsonContent = f.read()
		jsonContent = json.loads(jsonContent)
		# 取得 json "BODY" 欄位
		AlarmList = jsonContent["AlarmList"]  
	# TODO
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
		
		return
	# TODO
	def main(self):
		pass
		
if __name__ == "__main__":
    a = Alarm()
    day, h, m = map(int, input("輸入鬧鐘時間（格式：星期(1-7):hh:mm）").split(":"))
    if a.set_alarm(day, h, m) == False:
        print('error time!')
