import time
import playsound
import sys
import os
scriptpath = "../"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))
from Threading import Job
class countdown():
	def __init__(self):
		self.totalSeconds = 0                               
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
		# print('Time\'s up!')
		audio_file = 'sound.mp3'
		playsound.playsound(audio_file, True) 
		return True
	def stop_countdown(self):
		pass
		 
if __name__ == "__main__":
	a = countdown()
	h, m, s = map(int,input("輸入到計時時間（格式：hh:mm:ss）").split(":"))
	if a.set_countdown(h, m, s) == False:
		print('error time!')
