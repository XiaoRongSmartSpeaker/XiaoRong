import os
import sys

import time  # for Development
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


playing = True  # for Development


class Volume:
    def __init__(self) -> None:
        self.systemVolume = 50
        self.musicVolume = 50
        return
    # alsa setting

    def set_amixer(self, mode):
        if mode == 'music':
            cmd = r"amixer -M set Master {}\%".format(self.musicVolume)
            returned_value = os.system(cmd)
            logger.debug("change musicVolume")
            logger.debug(returned_value)
        else:
            cmd = r"amixer -M set Master {}\%".format(self.systemVolume)
            returned_value = os.system(cmd)
            logger.debug("change systemVolume")
            logger.debug(returned_value)

        return

    # unspecified
    def get_volume(self) -> int:
        if playing:
            return self.get_music_volume()
        return self.get_system_volume()

    def set_volume(self, value=5):
        if value == None:
            value = 5
        if playing:
            return self.set_music_volume(value)
        return self.set_system_volume(value)

    def louder_volume(self, value=5):
        if value == None:
            value = 5
        if playing:
            return self.louder_music_volume(value)
        return self.louder_system_volume(value)

    def quieter_volume(self, value=5):
        if value == None:
            value = 5
        if playing:
            return self.quieter_music_volume(value)
        return self.quieter_system_volume(value)
    # system

    def get_system_volume(self) -> int:
        return self.systemVolume

    def set_system_volume(self, value=5):
        if value == None:
            value = 5
        if 10 <= value <= 100:
            self.systemVolume = value
            self.set_amixer('system')
        return True

    def louder_system_volume(self, value=5):
        if value == None:
            value = 5
        if 10 <= self.systemVolume + value <= 100:
            self.systemVolume += value
            self.set_amixer('system')

    def quieter_system_volume(self, value=5):
        if value == None:
            value = 5
        if 10 <= self.systemVolume - value <= 100:
            self.systemVolume -= value
            self.set_amixer('system')
    # music

    def get_music_volume(self):
        return self.musicVolume

    def set_music_volume(self, value=5):
        if value == None:
            value = 5
        if 0 <= value <= 100:
            self.musicVolume = value
            self.set_amixer('music')
        return True

    def louder_music_volume(self, value=5):
        if value == None:
            value = 5
        if 0 <= self.musicVolume + value <= 100:
            self.musicVolume += value
            self.set_amixer('music')

    def quieter_music_volume(self, value=5):
        if value == None:
            value = 5
        if 0 <= self.musicVolume - value <= 100:
            self.musicVolume -= value
            self.set_amixer('music')


#if __name__ == '__main__':
#    def get_all_volume():
#        print("System:", a.get_system_volume())
#        print("Music:", a.get_music_volume())
#    a = Volume()
#    a.set_music_volume(50)
#    get_all_volume()
#    time.sleep(10)
#    a.louder_music_volume()
#    get_all_volume()
#    time.sleep(10)
#    a.quieter_music_volume()
#    get_all_volume()
#    time.sleep(10)
#    a.louder_music_volume(10)
#    get_all_volume()
#    time.sleep(10)
#    a.louder_music_volume(30)
#    get_all_volume()
#    time.sleep(10)
#    a.quieter_music_volume(30)
#    get_all_volume()
#    time.sleep(10)
#    a.quieter_music_volume(10)
#    get_all_volume()

