import os
import sys
import types
import logging
import threading
from time import sleep
from gpiozero import Button, PWMLED

def str_to_class(field):
    try:
        identifier = getattr(sys.modules[__name__], field)
    except AttributeError:
        raise NameError("%s doesn't exist." % field) 
    # print(isinstance(identifier, Worker))
    if isinstance(identifier, ((type))):
        return identifier
    TypeError("%s is not a class." % field)

class Test():
    @classmethod
    def listen(cls, Worker): 
        if Worker.device.is_pressed:
            print("Pressed2" , Worker.device.pin)

class Worker(threading.Thread):
    def __init__(self, device, cls, func):
        threading.Thread.__init__(self)
        self.kill = False
        self.device = device
        self.cls = cls
        self.func = func
    
    def run(self):
        while not self.kill:
            try:
                #print(str_to_class(self.cls))
                todo = getattr(str_to_class(self.cls), self.func)
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
        
    def start(self):
        for item in self._sw:
            but, func = list(item.items())[0]
            self._sw_threads.append(Worker(but, func.split(',')[0],func.split(',')[1]))
            self._sw_threads[-1].daemon = True
            self._sw_threads[-1].start()
        for item in self._led:
            led, func = list(item.items())[0]
            self._led_threads.append(Worker(led, func.split(',')[0],func.split(',')[1]))
            self._led_threads[-1].daemon = True
            self._led_threads[-1].start()

    def modify_button_function(self, index, new_func):
        device = self._sw_threads[index].device
        self._sw_threads[index].kill=True
        self._sw_threads[index] = Worker(device, new_func.split(',')[0],new_func.split(',')[1])
        self._sw_threads[index].daemon = True
        self._sw_threads[index].start()

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
    BC = ButtonController({27:{'BUTTON':'Worker,listen'},24:{'BUTTON':'Worker,listen'},12:{'LED':'Worker,light'},16:{'LED':'Worker,light'},20:{'LED':'Worker,light'}})
    try:
        print("Starting Threads...")
        BC.start()
        print(BC._sw_threads)
        sleep(10)
        BC.modify_button_function(0,'Test,listen')
        print(BC._sw_threads)
        sleep(10)
        BC.modify_button_function(0,'Worker,listen')
        print(BC._sw_threads)
        BC.wait_until_finish()
    except:
        print("Shutting down...")
        BC.kill()

    BC.kill()
    print("Done!")