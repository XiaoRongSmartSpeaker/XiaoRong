import pytz
from datetime import datetime
     
class WorldTime():
    def __init__(self):
        self.tzList = []

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
                print(datetime.now(tzId).strftime('%Y:%m:%d %H:%M:%S %Z %z'))
                return
        print('not found')        

