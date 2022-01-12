from logging import INFO
import os
import sys
from time import sleep
import requests
import configparser
import shutil

import feature.TextToSpeech as TextToSpeech

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'feature', 'config.ini')
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'feature', 'default', 'default_config.ini')
config = configparser.ConfigParser(allow_no_value=True)
config.read(CONFIG_PATH)

# set up logger
try:
    import logger
    logger = logger.setup_applevel_logger(file_name='./log/smartspeaker.log')
except ModuleNotFoundError as e:
    print(e)
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class FactoryReset:
    def __init__(self, main_instance = None):
        # self.state = 0
        logger.debug("initializing")
        self._default_config_path = DEFAULT_CONFIG_PATH     # get factory default config file path
        self._config_path = CONFIG_PATH                     # get current config file path
        # self._speaker_name = os.getenv('SPEAKER_NAME')    # get speaker_name for server API request
        self._server_url = 'https://httpbin.org/delay/10'
        if main_instance:
            self._main_instance = main_instance
    
    def _call_server_delete_speaker_data(self):
        # payloads = {'speaker_name': self._speaker_name}
        my_headers = {'user-agent': 'smartspeaker'}
        try:
            # response = requests.get(self._server_url, params=payloads, timeout=10)
            response = requests.get(self._server_url, headers=my_headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logger.error(errh)
        except requests.exceptions.ConnectionError as errc:
            logger.error(errc)
        except requests.exceptions.Timeout as errt:
            logger.error(errt)
            config.set("Status", "serverPairRemoveCompleted", "False")
        except requests.exceptions.RequestException as err:
            logger.error(err)
        else:
            logger.info("Successfully sent request to delete speaker data")
            print(response.text)
            # print response
        
        with open(CONFIG_PATH, 'w') as configfile:
            config.write(configfile)

    def _delete_device_user_data(self):
        # delete specific files
        if config['File Path']['files_to_delete']:
            file_list = config.get('File Path', 'files_to_delete').split(',\n')
        else:
            file_list = []
        
        for file in file_list:
            try:
                os.remove(file)
            except OSError as e:
                logger.error('Failed to delete %s. Reason: %s' % (file, e))
            else:
                logger.info("File successfully deleted: " + file)

        # restore specific files
        if config['File Path']['files_to_restore']:
            file_pair_list = config.get('File Path', 'files_to_restore').split(',\n')
        else:
            file_pair_list = []
        
        for file_pair in file_pair_list:
            file, default_file = file_pair.split(" ", 1) + ['']
            try:
                os.path.exists(file)
                os.path.exists(default_file)
                with open(default_file, 'r') as src_file, open(file, 'w') as dst_file:
                    default_config_content = src_file.read()
                    dst_file.write(default_config_content)
            except OSError as e:
                logger.error('Failed to delete %s. Reason: %s' % (file, e))
            else:
                logger.debug("%s restored to default" % (file))
        
        # remove content in a folder
        if config['File Path']['folders_to_clean']:
            folder_list = config.get('File Path', 'folders_to_clean').split(',\n')
        else:
            folder_list = []
        
        for folder in folder_list:
            try:
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                            logger.debug("Successfully deleted file: " + file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                            logger.debug("Successfully deleted sub-folder: " + file_path)
                    except Exception as e:
                        logger.error('Failed to delete: %s. Reason: %s' % (file_path, e))
            except OSError as e:
                logger.error('Failed to clean %s. Reason: %s' % (folder, e))
            else:
                logger.debug("Successfully cleaned folder %s" % (folder))

    def _terminate_other_process(self):
        if hasattr(self._main_instance, "close") and callable(getattr(self._main_instance, "close")):
            logger.info("Closing all thread ...")
            self._main_instance.close()     # main.close()
        else:
            logger.error("Method to close all thread is not correctly implemented")
        pass

    def _restore_config(self):
        if not os.path.exists(self._default_config_path):
            logger.error("Default config file does not exist")
            return
        
        if not os.path.exists(self._config_path):
            logger.error("Current config file does not exist")
            return

        with open(self._default_config_path, 'r') as src_file, open(self._config_path, 'w') as dst_file:
            default_config_content = src_file.read()
            dst_file.write(default_config_content)
        
        logger.debug("Config file restored to factory default")

    def factory_reset(self):
        self._delete_device_user_data()

        self._call_server_delete_speaker_data()

        self._restore_config()

        # self._terminate_other_process()

        for i in range(3):
            logger.info("Rebooting in " + str(3 - i))
            sleep(1)

        # os.system('reboot')

    def factory_reset_notification(self):
        TextToSpeech.text_to_voice("音箱重置即將開始")
        TextToSpeech.text_to_voice("繼續按住按鈕十秒以執行重置")

# testing only
if __name__ == "__main__":
    ff = FactoryReset()
    # ff.factory_reset_notification()
    ff.factory_reset()