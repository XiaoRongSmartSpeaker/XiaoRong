import time
import playsound
import os
class countdown:
	def __init__(self):
		self.totoalSeconds = 0
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

	def setCountdown(self, h: int, m: int, s: int):
		if h <= 0 or m <= 0 or s <= 0:
			return False
		totalSeconds = s + m * 60 + h * 3600
		if 0 <= totalSeconds <= 7200:
			self.totalSeconds = totalSeconds
			return True
		return False
	def stopCountdown(self):
		pass
		 
if __name__ == "__main__":
    a = countdown()
    if a.setCountdown(0, 0, 1) == False:
    	print('error time!')
    
