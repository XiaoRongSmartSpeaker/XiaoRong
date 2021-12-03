from pypinyin import pinyin, lazy_pinyin
import re
import time
import time_extract
import volume_extract
import language_extract
import json

# 目前還不支援 明/後 天 時間
with open('./keyword.json', encoding="utf-8") as f :
    func_dict = json.load(f) 

day_dict = {'一': 1, '1': 1 , '二': 2, '2': 2 , '三': 3, '3': 3 , '四': 4, '4': 4 , 
            '五': 5, '5': 5 , '六': 6, '6': 6 , '末': 6 ,'天': 7, '日': 7}

def isPhoneNumber(str):
    return re.match(r'\d(-\d)*', str)

def text2func(input_str):
    key_found = 0
    keyword_index = -1
    smallest_index = 999999999
    keyword_str = 'UNKNOWN'
    classname = 'UNKNOWN'
    allfunc_list = []
    for func_name in list(func_dict):
        for keyword in list(func_dict[func_name]["keywords"]):
            allfunc_list.append(keyword)
    for keyword in allfunc_list:
        keyword_index = input_str.find(keyword)
        if (keyword_index!=-1):
            if(keyword_index < smallest_index):
                smallest_index = keyword_index
                keyword_str = keyword
    for func_name in list(func_dict):
        for keyword in list(func_dict[func_name]["keywords"]):
            if( keyword == keyword_str):
                keyword_str = keyword
                classname = func_dict[func_name]["class"]
                return [classname, func_name, keyword]
    return [classname, func_name, 'None']


def para_extract(input_str, func_key):
    class_name = func_key[0]
    function_name = func_key[1]
    location = input_str.find(func_key[2])
    if(location != -1): # 有這個關鍵字
        target = input_str[location+len(func_key[2]):]
        target = target.lstrip()
    else:
        return('question', 'question_answering', (input_str))
    if( function_name == 'call'):#==================================================CALL=======================================V
        if(len(target) == 0):
            return ('FAILED', 'FAILED', tuple())
        if(isPhoneNumber(target)):
            return (func_key[0], 'call', (0, target))
        target_pinyin = lazy_pinyin(target)
        return (func_key[0], 'call', (1, target_pinyin))
    elif( function_name == 'add_calender_week'):#==================================ADD_CALENDER_WEEK
        if(len(target) == 0):
            return (func_key[0], 'FAILED', ('TARGET NOT FOUND'))
        if(len(target) <= 1):
            return (func_key[0], 'FAILED', ('TARGET NOT FOUND'))
        if(target[0] in day_dict.keys()):
            para = time_extract.target_time(target[1:], 0)
            return (class_name, 'add_calender_week', (day_dict[target[0]], para[0], para[1], para[2]))
        else:
            return ('FAILED', 'FAILED', tuple())
    elif( function_name == 'add_calender_day'):#====================================ADD_CALENDER_DAY
        if(len(target) == 0):
            return (func_key[0], 'FAILED', ('TARGET NOT FOUND'))
        para = time_extract.target_time(target, 0)
        return (class_name, 'add_calender_day', (tuple(para)))
    elif( function_name == 'add_calender'):#========================================ADD_CALENDER
        if(len(target) == 0):
            return (func_key[0], 'FAILED', ('TARGET NOT FOUND'))
        para = time_extract.target_time(target, 0)
        return(class_name, function_name, tuple(para))
    elif( function_name == 'next_calender'):#=======================================NEXT_CALENDER
        return(class_name, function_name, (None))
    elif( function_name == 'read_calender'):#=======================================READ_CALENDER
        para = time_extract.target_time(target, 0)
        return(class_name, function_name, tuple([para[0][5:10]]))
    elif( function_name == 'weather_forecast'):#====================================WEATHER_FORECAST
        para = time_extract.target_time(target, 1)
        place = para[-1]
        if(len(place)==0):
            place = 'HERE'
        elif(place[0] == '的'):
            place = place[1:]
        return(class_name, function_name, tuple([para[0],place] ))
    elif( function_name == 'open_bluetooth'):#======================================OPEN_BLUETOOTH============================
        return(class_name, function_name,())
    elif( function_name == 'close_bluetooth'):#=====================================CLOSE_BLUETOOTH===========================
        return(class_name, function_name,())
    elif( function_name == 'play_music'):
        return(class_name, function_name, tuple([target]))
    elif( function_name == 'pause_music'):
        return(class_name, function_name, tuple())
    elif( function_name == 'continue_music'):
        return(class_name, function_name, tuple())
    elif( function_name == 'stop_music'):
        return(class_name, function_name, tuple())
    elif( function_name == 'now_playing'):
        return(class_name, function_name, tuple())
    elif( function_name == 'repeat_playing'):
        return(class_name, function_name, tuple())
    elif( function_name == 'louder_system_volume'):
        para = volume_extract.target_volume(target)
        return(class_name, function_name,tuple(para))
    elif( function_name == 'quiter_system_volume'):
        para = volume_extract.target_volume(target)
        return(class_name, function_name,tuple(para))
    elif( function_name == 'set_system_volume'):
        para = volume_extract.target_volume(target)
        return(class_name, function_name, tuple(para))
    elif( function_name == 'louder_music_volume'):
        para = volume_extract.target_volume(target)
        return(class_name, function_name,tuple(para))
    elif( function_name == 'quiter_music_volume'):
        para = volume_extract.target_volume(target)
        return(class_name, function_name,tuple(para))
    elif( function_name == 'set_music_volume'):
        para = volume_extract.target_volume(target)
        return(class_name, function_name, tuple(para))
    elif( function_name == 'louder_volume'):
        para = volume_extract.target_volume(target)
        return(class_name, function_name,tuple(para))
    elif( function_name == 'quiter_volume'):
        para = volume_extract.target_volume(target)
        return(class_name, function_name,tuple(para))
    elif( function_name == 'set_volume'):
        para = volume_extract.target_volume(target)
        return(class_name, function_name, tuple(para))
    elif( function_name == 'translate'):
        para = language_extract.target_language(target)
        return(class_name, function_name, tuple(para))
    elif( function_name == 'question_answering'):
        para = target
        return(class_name, function_name, tuple([para]))
    else:
        return ('question', 'question_answering', tuple([input_str]))
        

def main(input_str):
    print(input_str)
    which = text2func(input_str)
    ret = para_extract(input_str, which)
    return ret

print(main('幫我打給小絨'))
print(' ')
print(main('打給0800-000-123'))
print(' ')
print(main('幫我打給'))
print(' ')
print(main('查看下一個行程'))
print(' ')
print(main('查看行事曆十二月三日'))
print(' ')
print(main('新增行事曆12月3號12點到13點家庭聚餐'))
print(' ')
print(main('新增行事曆每週二兩點兩分家庭聚餐'))
print(' ')
print(main('新增行事曆每天18點健身'))
print(' ')
# print(main('新增提醒 12月3號 12點 家庭聚餐'))
# print(' ')
print(main('查看下一個行程'))
print(' ')
print(main('天氣查詢'))
print(' ')
print(main('天氣查詢12月3日'))
print(' ')
print(main('天氣查詢台北'))
print(' ')
print(main('天氣查詢12月五日八點十三的台北'))
print(' ')
print(main('開啟藍芽'))
print(' ')
print(main('關閉藍芽'))
print(' ')
print(main('播放鄧紫棋的光年之外'))
print(' ')
print(main('暫停播放'))
print(' ')
print(main('停止音樂'))
print(' ')
print(main('現在在播的是什麼'))
print(' ')
print(main('幫我一直播放'))
print(' ')
print(main('系統音量調大聲'))
print(' ')
print(main('系統音量調小聲10趴'))
print(' ')
print(main('系統音量調成兩百'))
print(' ')
print(main('音樂音量調大聲負10'))
print(' ')
print(main('音樂音量調小聲18'))
print(' ')
print(main('音樂音量調成500'))
print(' ')
print(main('音量調大聲-18'))
print(' ')
print(main('音量調小聲0'))
print(' ')
print(main('音量調成'))
print(' ')
print(main('啟動即時翻譯'))
print(' ')
print(main('啟動即時翻譯中文翻法文'))
print(' ')
