import pytz
from datetime import datetime
import sys
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

class WorldTime():
    def __init__(self):
        self.tzList = []
        self.threadHandler = None 
    def import_thread(self, thread):
		self.threadHandler = thread
		return
    def get_time_zone_list(self):
        if self.tzList == []:
            self.tzList = pytz.all_timezones
        return self.tzList
    def get_time_at_place(self, place):
        self.get_time_zone_list()
        # print(self.tzList)
        for tz in self.tzList:
            if place.casefold() in tz.casefold():
                tzId = pytz.timezone(tz)
                tzTime = datetime.now(tzId).strftime('%Y:%m:%d %H:%M:%S %Z %z')
                logger.debug(tzTime)
                self.threadHandler.add_thread({
                    'class': 'TextToSpeech',
                    'func': 'text_to_voice',
                    'args': place + '的現在時間是' + tzTime,
                    })
                return
        logger.debug('worldTime call QA')
        self.threadHandler.add_thread({
            'class': 'class QuestionAnswering',
            'func': 'class QuestionAnswering',
            'args': place + '時間',
            })  

tz = WorldTime()
tz.get_time_at_place('taipei')