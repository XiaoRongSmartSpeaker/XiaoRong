import os
import sys
import logging
import requests
import time
from gpiozero import Button, LED


class ResetGPIO:
    def __init__(self):
        self._sw_1 = Button(24)
        self._sw_2 = Button(25)
        self._led_r = LED(20)
        self._led_y = LED(16)
        self._led_g = LED(12)

    def light_y(self):
        self._led_y.source = self._sw_1

    def light_g(self):
        self._led_g.source = self._sw_1

    def light_r(self):
        self._led_r.source = self._sw_1

    def turn_off_LED(self):
        self._led_y.source = self._led_y
        self._led_g.source = self._led_g
        self._led_r.source = self._led_r

    def check_for_reset(self):
        start_time = time.time()
        
        while self._sw_1.is_pressed:
            button_time = time.time()
            held_time = button_time - start_time
            print(held_time)
            if held_time >= 5.0:
                self.light_y()
            if held_time >= 10.0:
                self.light_g()
            if held_time >= 15.0:
                self.light_r()
                time.sleep(3)
                self.turn_off_LED()
                return True
        self.turn_off_LED()
        return False

    def listen(self):
        while True:
            if self.check_for_reset():
                break
        return True

# set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fromatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(fromatter)
logger.addHandler(sh)

class FactoryReset:
    def __init__(self):
        self._default_config_path = os.environ.get('CONFIG_PATH')     # get factory default config file path
        self._config_path = os.environ.get('CONFIG_PATH')             # get current config file path
        self._speaker_name = os.environ.get('SPEAKER_NAME')           # get speaker_name for server API request

        self._server_url = ''
    
    def listen_reset_button(self):
        logger.debug("Begin to listen for gpio signal")
        # if button is pressed for 5 seconds, play factory reset warning
        # if button is pressed for 15 seconds, call factory_reset
        listener = ResetGPIO()
        if listener.listen():
            logger.debug("Begin factory reset")
            self.factory_reset()
    
    def _call_server_delete_speaker_data(self):
        payloads = {'speaker_name': self._speaker_name}
        try:
            response = requests.get(self._server_url, params=payloads, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logger.error(errh)
        except requests.exceptions.ConnectionError as errc:
            logger.error(errc)
        except requests.exceptions.Timeout as errt:
            logger.error(errt)
        except requests.exceptions.RequestException as err:
            logger.error(err)

    def _call_db_delete_user_data(self):
        # log request result
        pass

    def _terminate_other_process(self):
        # method 1: have main terminate all the other threads
        # method 2: kill all python process running on this machine
        pass

    def _restore_config(self):
        if not os.path.exists(self._default_config_path):
            logger.error("Default config file does not exist")
            return False
        
        if not os.path.exists(self._config_path):
            logger.error("Current config file does not exist")
            return False

        with open(self._default_config_path, 'r') as src_file, open(self._config_path, 'w') as dst_file:
            default_config_content = src_file.read()
            dst_file.wrtielines(default_config_content)
        
        logger.debug("Config file restored to factory default")
        return True

    def factory_reset(self):
        # delete user data
        # self._call_server_delete_speaker_data()
        # self._call_db_delete_user_data()

        # self._terminate_other_process()

        # self._restore_config()

        # log the results of previous steps

        logger.debug("Rebooting ...")
        # os.system('reboot')

# testing only
if __name__ == "__main__":
    thread = FactoryReset()
    thread.listen_reset_button()
