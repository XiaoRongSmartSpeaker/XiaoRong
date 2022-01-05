import os
import sys
import logging
import requests
import configparser

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'feature', 'config.ini')
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'feature', 'default', 'default_config.ini')
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

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
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fhandle = logging.FileHandler('../log/smartspeaker.log')
    fhandle.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fhandle)

class FactoryReset:
    def __init__(self, main_instance):
        self._default_config_path = DEFAULT_CONFIG_PATH     # get factory default config file path
        self._config_path = CONFIG_PATH                     # get current config file path
        # self._speaker_name = os.getenv('SPEAKER_NAME')    # get speaker_name for server API request
        self._server_url = ''
        self._main_instance = main_instance
    
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

    def _delete_device_user_data(self):
        file_list = config.get('File Path', 'files_to_delete').split(',\n')
        for file in file_list:
            try:
                os.remove(file)
            except OSError as e:
                logger.error(e)
            else:
                logger.info("File successfully deleted: " + file)

    def _terminate_other_process(self):
        self._main_instance.close()     # main.close()

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
        # self._call_server_delete_speaker_data()
        self._terminate_other_process()

        # self._delete_device_user_data();

        # self._restore_config()

        logger.debug("Rebooting ...")
        # os.system('reboot')

# testing only
if __name__ == "__main__":
    thread = FactoryReset()
    thread.factory_reset()