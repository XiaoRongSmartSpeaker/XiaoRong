import os
import sys
import logging
import requests
import time
import configparser
from gpiozero import Button, LED
from dotenv import load_dotenv

# get gpio pin number from config file
config = configparser.ConfigParser()
config.read('config.ini')
BUTTON_RESET = int(config['GPIO']['BUTTON_RESET'])
LED_RED = int(config['GPIO']['LED_RED'])
LED_YELLOW = int(config['GPIO']['LED_YELLOW'])
LED_GREEN = int(config['GPIO']['LED_GREEN'])

# load .env in /feature
load_dotenv()

class ResetGPIO:
    def __init__(self):
        self._sw_1 = Button(BUTTON_RESET)
        self._sw_2 = Button(23)
        self._led_r = LED(LED_RED)
        self._led_y = LED(LED_YELLOW)
        self._led_g = LED(LED_GREEN)

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

class FactoryReset:
    def __init__(self):
        self._default_config_path = os.getenv('DEFAULT_CONFIG_FILE')     # get factory default config file path
        self._config_path = os.getenv('CONFIG_FILE')             # get current config file path
        # self._speaker_name = os.getenv('SPEAKER_NAME')           # get speaker_name for server API request
        # self._server_url = ''
    
    def listen_reset_button(self):
        logger.debug("Begin to listen for gpio signal")

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

    def _delete_device_user_data(self):
        pass

    def _terminate_other_process(self):
        # method 1: have main terminate all the other threads
        # method 2: kill all python process running on this machine
        pass

    def _restore_config(self):
        if not os.path.exists(self._default_config_path):
            logger.error("Default config file does not exist")
        
        if not os.path.exists(self._config_path):
            logger.error("Current config file does not exist")

        with open(self._default_config_path, 'r') as src_file, open(self._config_path, 'w') as dst_file:
            default_config_content = src_file.read()
            dst_file.write(default_config_content)
        
        logger.debug("Config file restored to factory default")

    def factory_reset(self):
        # delete user data
        # self._call_server_delete_speaker_data()
        # self._call_db_delete_user_data()

        # self._terminate_other_process()

        self._restore_config()

        logger.debug("Rebooting ...")
        # os.system('reboot')

# testing only
if __name__ == "__main__":
    thread = FactoryReset()
    thread.listen_reset_button()
