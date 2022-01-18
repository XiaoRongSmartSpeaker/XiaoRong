import os
import sys
import types
import logging
import threading
from time import sleep
from gpiozero import Button, PWMLED
import Volume
import MusicStreaming


class Test():
    def __init__(self):
        self.state = 0
        pass

    def listen(self, *args):
        print("Pressed2")

    def light_control_on(self, LC):
        ind = 0
        print("blinking...")
        for led in LC._leds:
            LC.blink(ind)
            ind += 1

    def light_control_off(self, LC):
        ind = 0
        print("turning off...")
        for led in LC._leds:
            LC.off(ind)
            ind += 1

    def reset(self, args):
        device = args[0], LC = args[1]
        if device.is_pressed:
            print("setting timer...")
            t1 = threading.Timer(5.0, self.change_state, [LC])
            t2 = threading.Timer(10.0, self.change_state, [LC])
            t3 = threading.Timer(15.0, self.change_state, [LC])
            t1.start()
            t2.start()
            t3.start()
            device.when_released = lambda: self.cancel([t1, t2, t3], LC)

    def cancel(self, ts, LC):
        print("canceling...")
        self.state = 0
        for t in ts:
            t.cancel()
        for i in range(3):
            LC.off(i)

    def change_state(self, LC):
        print("changing...")
        if self.state == 0:
            LC.light(0)
            self.state = 1
        elif self.state == 1:
            LC.light(1)
            self.state = 2
        elif self.state == 2:
            LC.light(2)
            # reset here


class Worker(threading.Thread):
    def __init__(self, device, cls, func, args=None):
        threading.Thread.__init__(self)
        self.kill = False
        self.device = device
        self.cls = cls
        self.func = func
        if func == 'reset':
            self.args = [device] + args
        else:
            self.args = args

    def run(self):
        while not self.kill:
            try:
                todo = getattr(self.cls, self.func)
                if self.args is not None:
                    self.device.when_pressed = lambda: todo(self.args)
                else:
                    self.device.when_pressed = lambda: todo()
            except AttributeError:
                print("Attribute Error... Cannot find function from class")
                exit()

    def listen(self):
        print("Pressed", self.device.pin)

    def change_func(self):
        if self.device.is_pressed:
            BC.modify_button_function(0, 'Test,listen')
        else:
            BC.modify_button_function(0, 'Worker,listen')

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
    def __init__(self):
        self._sw = []
        self._led = []
        self._sw_threads = []
        self._led_threads = []
        self.LC = LEDController([23, 24, 25])

    def start(self, pin_func_dict):
        for key, val in pin_func_dict.items():
            typ, func = list(val.items())[0]
            if typ == 'BUTTON':
                self._sw.append({Button(key, hold_time=5): func})
            # if typ=='LED':
            #     self._led.append({PWMLED(key):func})
        for item in self._sw:
            but, func = list(item.items())[0]
            if func[1] == 'reset':
                self._sw_threads.append(
                    Worker(but, func[0], func[1], func[2] + [self.LC]))
            else:
                self._sw_threads.append(Worker(but, func[0], func[1]))
            self._sw_threads[-1].daemon = True
            self._sw_threads[-1].start()
        # for item in self._led:
        #     led, func = list(item.items())[0]
        #     self._led_threads.append(Worker(led, func[0],func[1]))
        #     self._led_threads[-1].daemon = True
        #     self._led_threads[-1].start()

    def modify_button_function(self, index, new_func):
        device = self._sw_threads[index].device
        self._sw_threads[index].kill = True
        if new_func[1] == 'reset':
            self._sw_threads[index] = (
                Worker(device, new_func[0], new_func[1], new_func[2] + [self.LC]))
        else:
            self._sw_threads[index] = Worker(device, new_func[0], new_func[1])
        self._sw_threads[index].daemon = True
        self._sw_threads[index].start()

    def wait_until_finish(self):
        for thread in self._sw_threads:
            thread.join()
        # for thread in self._led_threads:
        #     thread.join()

    def kill(self):
        index = 0
        for but in self._sw:
            self._sw_threads[index].kill = True
            index += 1
        index = 0
        for led in self._led:
            self._led_threads[index].kill = True
            index += 1


class LEDController():
    def __init__(self, pin_dict):
        self._leds = []
        for led in pin_dict:
            self._leds.append(PWMLED(led))
            self._leds[-1].off()

    def light(self, id):
        self._leds[id].value = 1

    def off(self, id):
        self._leds[id].value = 0
        self._leds[id].off()

    def blink(self, id):
        self._leds[id].blink(on_time=0.5, off_time=0.5)


if __name__ == '__main__':
    check = True
    T = Test()
    # ff = FactoryReset(T)
    # LC = LEDController([23,24,25])
    vv = Volume.Volume()
    BC = ButtonController()
    # BC = ButtonController({27:{'BUTTON':'Worker,listen'},24:{'BUTTON':'Worker,listen'},12:{'LED':'Worker,light'},16:{'LED':'Worker,light'},20:{'LED':'Worker,light'}})
    try:
        print("Starting Threads...")
        BC.start({13: {'BUTTON': [vv, 'louder_volume']}, 14: {'BUTTON': [
                 vv, 'louder_volume']}, 15: {'BUTTON': [vv, 'quieter_volume']}})
        print(BC._sw_threads)
        BC.wait_until_finish()
    except BaseException:
        print("Shutting down...")
        BC.kill()

    BC.kill()
    print("Done!")
