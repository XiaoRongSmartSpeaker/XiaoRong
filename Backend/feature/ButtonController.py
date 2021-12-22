import os
import sys
import logging
from time import sleep
from gpiozero import Button, LED

class ButtonController():
    def __init__(self, pin_list):
        self._sw = []
        self._led = []
        for item in pin_list:
            for key, val in item.items():
                if key=='BUTTON':
                    self._sw.append(Button(val))
                if key=='LED':
                    self._led.append(LED(val))
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

    def check_for_press(self):
        flag = False
        pressed_list = []
        for but in self._sw:
            print("checking"+str(but))
            if but.is_pressed:
                print("pressing...")
                flag = True
                pressed_list.append(but)
                
        return flag, pressed_list

    def listen(self): 
        while True:
            for led in self._led:
                # print(led)
                led.on()
                sleep(1)
                led.off()
                sleep(1)
            check, pressed_list = self.check_for_press()
            if check:
                return pressed_list

if __name__=='__main__':
    check = True
    BC = ButtonController([{'BUTTON':24},{'BUTTON':25},{'LED':12},{'LED':16},{'LED':20}])
    pressed_list = BC.listen()
    print(pressed_list)