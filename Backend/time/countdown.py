import time
import playsound
import os
class countdown:
	def __init__(self):
		True
	def setCountdown(self, h: int, m: int, s: int):
		totalSeconds = s + m * 60 + h * 3600
		if totalSeconds < 0 or totalSeconds > 7200:
			return False

		while totalSeconds:
			m, s = divmod(totalSeconds, 60)
			h, m = divmod(m, 60)
			timeFormat = '{:02d}:{:02d}:{:02d}'.format(h, m, s)
			print(timeFormat)
			time.sleep(1)
			totalSeconds -= 1
		# print('Time\'s up!')
		audio_file = 'sound.mp3'
		playsound.playsound(audio_file, True)                                      
		return True

if __name__ == "__main__":
    a = countdown()
    if a.setCountdown(0, 0, 1) == False:
    	print('error time!')
    
