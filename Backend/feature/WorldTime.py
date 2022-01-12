import pytz
from datetime import datetime
import sys
import json
import os
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
    def import_thread(self, thread) -> None:
        self.threadHandler = thread
        return
    def get_time_zone_list(self) -> None:
        if self.tzList == []:
            with open( f'{os.path.dirname(__file__)}/timeZone.json', encoding="utf-8") as f:
                jsonContent = f.read()
            jsonContent = json.loads(jsonContent)
            # 取得 json "BODY" 欄位
            self.tzList = jsonContent["timezoneList"]
        return
    def get_time_at_place(self, place) -> None:
        self.get_time_zone_list()
        # print(self.tzList)
        for tz in self.tzList:
            if place.casefold() in tz["tzid"].casefold() or  place.casefold() in tz["cityNames"]:
                tzId = pytz.timezone(tz["tzid"])
                tzTime = datetime.now(tzId).strftime('%Y年%m月%d日 %H點%M分%S秒 %Z %z')
                sentence = place + '，現在時間是' + tzTime
                logger.debug(sentence)
                self.threadHandler.add_thread({
                    'class': 'TextToSpeech',
                    'func': 'text_to_voice',
                    'args': (sentence,)
                    })
                return
        logger.debug('worldTime call QA')
        self.threadHandler.add_thread({
            'class': 'QuestionAnswering',
            'func': 'google_search',
            'args': (place + '時間',)
            })  
        return

# if __name__ == '__main__':
#     tz = WorldTime()
#     while True:
#         place = input("輸入地區：")
#         tz.get_time_at_place(place)