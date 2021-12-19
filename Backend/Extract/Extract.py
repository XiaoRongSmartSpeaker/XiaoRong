from pypinyin import pinyin, lazy_pinyin
import re
import time
import para_extract
import json

# 目前還不支援 明/後 天 時間

class Extract:

    def __init__(self) -> None:
        with open('./keyword.json', encoding="utf-8") as f :
            self.func_dict = json.load(f) 
        self.day_dict = {'一': 1, '1': 1 , '二': 2, '2': 2 , '三': 3, '3': 3 , '四': 4, '4': 4 , 
            '五': 5, '5': 5 , '六': 6, '6': 6 , '末': 6 ,'天': 7, '日': 7}
        return

    def text2func(self, input_str):
        key_found = 0
        keyword_index = -1
        smallest_index = 999999999
        keyword_str = 'UNKNOWN'
        classname = 'UNKNOWN'
        allfunc_list = []
        for func_name in list(self.func_dict):
            for keyword in list(self.func_dict[func_name]["keywords"]):
                allfunc_list.append(keyword)
        for keyword in allfunc_list:
            keyword_index = input_str.find(keyword)
            if (keyword_index!=-1):
                if(keyword_index < smallest_index):
                    smallest_index = keyword_index
                    keyword_str = keyword
        for func_name in list(self.func_dict):
            for keyword in list(self.func_dict[func_name]["keywords"]):
                if( keyword == keyword_str):
                    keyword_str = keyword
                    classname = self.func_dict[func_name]["class"]
                    return [classname, func_name, keyword]
        return [classname, func_name, 'None']


    def para_extract(self, input_str, func_key):
        class_name = func_key[0]
        function_name = func_key[1]
        location = input_str.find(func_key[2])
        target = input_str
        para = ()
        if(location != -1): # 有這個關鍵字
            target = input_str[location+len(func_key[2]):]
            target = target.lstrip()
        else:
            return('question', 'question_answering', tuple([input_str]))
        if( function_name == 'call'):#==================================================CALL=======================================V
            para = para_extract.target_call(target)
        elif( function_name == 'add_calender_week'):#==================================ADD_CALENDER_WEEK
            if(len(target) == 0):
                return (func_key[0], 'FAILED', ('TARGET NOT FOUND'))
            if(len(target) <= 1):
                return (func_key[0], 'FAILED', ('TARGET NOT FOUND'))
            if(target[0] in self.day_dict.keys()):
                para = para_extract.target_time(target[1:], 0)
                para = [self.day_dict[target[0]], para[0], para[1], para[2]]
            else:
                return ('FAILED', 'FAILED', tuple())
        elif( function_name == 'add_calender_day'):#====================================ADD_CALENDER_DAY
            if(len(target) == 0):
                return (func_key[0], 'FAILED', ('TARGET NOT FOUND'))
            para = para_extract.target_time(target, 0)
        elif( function_name == 'add_calender'):#========================================ADD_CALENDER
            if(len(target) == 0):
                return (func_key[0], 'FAILED', ('TARGET NOT FOUND'))
            para = para_extract.target_time(target, 0)
        elif( function_name == 'next_calender'):#=======================================NEXT_CALENDER
            para = ()
        elif( function_name == 'read_calender'):#=======================================READ_CALENDER
            para = para_extract.target_time(target, 0)
            para = [para[0][5:10]]
        elif( function_name == 'weather_forecast'):#====================================WEATHER_FORECAST
            para = para_extract.target_time(target, 1)
            place = para[-1]
            if(len(place)==0):
                place = 'HERE'
            elif(place[0] == '的'):
                place = place[1:]
            para = [para[0], place]
        elif( function_name == 'open_bluetooth'):#======================================OPEN_BLUETOOTH============================
            para = ()
        elif( function_name == 'close_bluetooth'):#=====================================CLOSE_BLUETOOTH===========================
            para = ()
        elif( function_name == 'play_music'):
            para = [target]
        elif( function_name == 'pause_music'):
            para = ()
        elif( function_name == 'continue_music'):
            para = ()
        elif( function_name == 'stop_music'):
            para = ()
        elif( function_name == 'now_playing'):
            para = ()
        elif( function_name == 'repeat_playing'):
            para = ()
        elif( function_name == 'louder_system_volume'):
            para = para_extract.target_volume(target)
        elif( function_name == 'quiter_system_volume'):
            para = para_extract.target_volume(target)
        elif( function_name == 'set_system_volume'):
            para = para_extract.target_volume(target)
        elif( function_name == 'louder_music_volume'):
            para = para_extract.target_volume(target)
        elif( function_name == 'quiter_music_volume'):
            para = para_extract.target_volume(target)
        elif( function_name == 'set_music_volume'):
            para = para_extract.target_volume(target)
        elif( function_name == 'louder_volume'):
            para = para_extract.target_volume(target)
        elif( function_name == 'quiter_volume'):
            para = para_extract.target_volume(target)
        elif( function_name == 'set_volume'):
            para = para_extract.target_volume(target)
        elif( function_name == 'translate'):
            para = para_extract.target_language(target)
        elif( function_name == 'question_answering'):
            para = [target]
        elif( function_name == 'set_timer'):
            para = para_extract.target_countdown(input_str)
        elif( function_name == 'set_alert'):
            para = para_extract.target_alert(target)
        else:
            para = [input_str]
            return{"name":'question', "func":'question_answering', "args":tuple(para)}
        return{"name":class_name, "func":function_name, "args":tuple(para)}        
            

    def main(self, input_str):
        print(input_str)
        which = self.text2func(input_str)
        ret = self.para_extract(input_str, which)
        return ret
    