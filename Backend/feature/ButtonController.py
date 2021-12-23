import os
import sys
import logging
import threading
from time import sleep
from gpiozero import Button, PWMLED

class Worker(threading.Thread):
    def __init__(self, device, func):
        threading.Thread.__init__(self)
        self.kill = False
        self.device = device
        self.func = func
    
    def run(self):
        while not self.kill:
            try:
                todo = getattr(Worker, self.func)
                todo(self)
            except:
                exit()
            
    def listen(self): 
        if self.device.is_pressed:
            print("Pressed" , self.device.pin)

    def light(self):
        self.device.value = 0.5  # half brightness
        sleep(1)
        self.device.value = 0  # off
        sleep(1)
        self.device.value = 0.5  # half brightness
        sleep(1)
        self.device.value = 1  # full brightness
        sleep(1)


class ButtonController():
    def __init__(self, pin_func_dict):
        self._sw = []
        self._led = []
        self._sw_threads = []
        self._led_threads = []
        for key, val in pin_func_dict.items():
            typ, func = list(val.items())[0]
            if typ=='BUTTON':
                self._sw.append({Button(key):func})
            if typ=='LED':
                self._led.append({PWMLED(key):func})
        # self._sw_1 = Button(24)
        # self._sw_2 = Button(25)
        # self._led_r = LED(20)
        # self._led_y = LED(16)
        # self._led_g = LED(12)

    # def light_y(self):
    #     self._led_y.source = self._sw_1

    # def light_g(self):
    #     self._led_g.source = self._sw_1

    # def light_r(self):
    #     self._led_r.source = self._sw_1

    # def turn_off_LED(self):
    #     self._led_y.source = self._led_y
    #     self._led_g.source = self._led_g
    #     self._led_r.source = self._led_r

    def start(self):
        for item in self._sw:
            but, func = list(item.items())[0]
            self._sw_threads.append(Worker(but, func))
            self._sw_threads[-1].daemon = True
            self._sw_threads[-1].start()
        for item in self._led:
            led, func = list(item.items())[0]
            self._led_threads.append(Worker(led, func))
            self._led_threads[-1].daemon = True
            self._led_threads[-1].start()

    def wait_until_finish(self):
        for thread in self._sw_threads:
            thread.join()
        for thread in self._led_threads:
            thread.join()

    def kill(self):
        index = 0
        for but in self._sw:
            self._sw_threads[index].kill=True
            index += 1
        index = 0
        for led in self._led:
            self._led_threads[index].kill=True
            index += 1
            

if __name__=='__main__':
    check = True
    BC = ButtonController({23:{'BUTTON':'listen'},24:{'BUTTON':'listen'},12:{'LED':'light'},16:{'LED':'light'},20:{'LED':'light'}})
    try:
        print("Starting Threads...")
        BC.start()
        BC.wait_until_finish()
    except:
        print("Shutting down...")
        BC.kill()

    BC.kill()
    print("Done!")