import re
# from datetime import datetime
import datetime
import cn2an
from pypinyin import pinyin

digit = {
    '一': 1,
    '兩': 2,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9}


def _trans(s):
    if s.isdigit():
        return(int(s))
    num = 0
    if s:
        idx_q, idx_b, idx_s = s.find('千'), s.find('百'), s.find('十')
        if idx_q != -1:
            num += digit[s[idx_q - 1:idx_q]] * 1000
        if idx_b != -1:
            num += digit[s[idx_b - 1:idx_b]] * 100
        if idx_s != -1:
            # 十前忽略一的处理
            num += digit.get(s[idx_s - 1:idx_s], 1) * 10
        if s[-1] in digit:
            num += digit[s[-1]]
    return num
# ==========================================================


def isPhoneNumber(str):
    return re.match(r'(\+|加)?\d(-\d)*', str)


# ================================================================================================================
day_dict = {'一': 1, '1': 1, '二': 2, '2': 2, '三': 3, '3': 3, '四': 4, '4': 4,
            '五': 5, '5': 5, '六': 6, '6': 6, '末': 6, '天': 7, '日': 7}


def target_call(input_str):
    if(len(input_str) == 0):
        return [0, None]
    else:
        if(isPhoneNumber(input_str)):
            input_str = input_str.replace("加", "+")
            return [0, input_str]
        else:
            return [1, pinyin(input_str, heteronym=True)]


def set_time(newtime):  # newtime=[year, month, hour, minute]
    a = datetime.datetime.now()
    time = [a.month, a.day, a.hour, a.minute]
    for i in range(4):
        if (newtime[i] != -1):
            time[i] = newtime[i]
    return (
        "%04d-%02d-%02d %02d:%02d" %
        (int(
            a.year), int(
            time[0]), int(
                time[1]), int(
                    time[2]), int(
                        time[3])))


def shift_time(day, hour, minute):
    return (
        datetime.datetime.now() +
        datetime.timedelta(
            days=day,
            hours=hour,
            minutes=minute)).strftime("%Y-%m-%d %H:%M")


def zh2cnnum(input_str):
    input_str = input_str.replace('兩', '二')
    input_str = input_str.replace('萬', '万')
    input_str = input_str.replace('億', '亿')
    return input_str


def target_time(input_str, mode):  # return the target time and the place to look later mode1 for time interval
    date = re.compile(
        r'((\d+)|(二|三|四|五|六|七|八|九)?十?(一|二|三|四|五|六|七|八|九)?)月((\d+)|(二|三|四|五|六|七|八|九)?十?(一|二|三|四|五|六|七|八|九)?)(日|號)')
    time = re.compile(
        r'((\d+)|(二|三|四|五|六|七|八|九)?十?(一|二|兩|三|四|五|六|七|八|九)?)(\.|點|時)(((\d+)|(二|三|四|五|六|七|八|九)?十?(一|二|三|四|五|六|七|八|九)?))?')
    later = re.compile(
        r'((今|明|後|大後)天)|(((\d+)|(二|三|四|五|六|七|八|九)?十?(一|二|三|四|五|六|七|八|九)?)(週|天|個?小時|分鐘)後)|下週(一|二|三|四|五|六|日|天)?')
    one_99 = re.compile(r'(\d+)|((二|三|四|五|六|七|八|九)?十?(一|二|兩|三|四|五|六|七|八|九)?)')
    target_obj = None
    # target_str = ''
    time_inter = 0
    time_str = 'NOW'
    month = int(-1)
    day = int(-1)
    hour = int(-1)
    minute = int(-1)
    endhour = int(-1)
    endminute = int(-1)
    time_inter = 0
    result = []
    if(later.search(input_str)):
        target_obj = later.search(input_str)
        target_str = target_obj.group()
        time_str = "1970-01-01 00:00"
        if (target_str == '明天'):
            time_str = shift_time(1, 0, 0)
        elif (target_str == '後天'):
            time_str = shift_time(2, 0, 0)
        elif (target_str == '大後天'):
            time_str = shift_time(3, 0, 0)
        elif (target_str == '今天'):
            time_str = shift_time(0, 0, 0)
        elif ('天後' in target_str):
            d = _trans(target_str[0:-2])
            time_str = shift_time(d, 0, 0)
            # time_str = 
            
        input_str = input_str[target_obj.end():]
        if(time.search(input_str)):
            ntarget_obj = time.search(input_str)
            ntarget_str = ntarget_obj.group()
            minute = 0
            if(ntarget_str.find('點')):
                hour = _trans(ntarget_str[:ntarget_str.index('點')])
                if('分' in ntarget_str):
                    minute = _trans(ntarget_str[ntarget_str.index(
                        '點') + 1:ntarget_str.index('分')])
            elif(ntarget_str.find('時')):
                hour = _trans(ntarget_str[:ntarget_str.index('時')])
                if('分' in ntarget_str):
                    minute = _trans(ntarget_str[ntarget_str.index(
                        '點') + 1:ntarget_str.index('分')])
            time_str = time_str[0:11] + ("%02d:%02d" % (hour, minute))
            result.append(time_str)
            input_str = input_str[ntarget_obj.end():]
        else:
            if(mode == 0):
                result.append(time_str[0:11] + '00:00')
            else:
                result.append(time_str[0:11] + '06:00')
        if(mode == 0 and input_str[0] == '到' and time.search(input_str)):
            if(time.search(input_str)):
                ntarget_obj = time.search(input_str)
                ntarget_str = ntarget_obj.group()
                minute = 0
                if(ntarget_str.find('點')):
                    hour = _trans(ntarget_str[:ntarget_str.index('點')])
                    if('分' in ntarget_str):
                        minute = _trans(ntarget_str[ntarget_str.index(
                            '點') + 1:ntarget_str.index('分')])
                elif(ntarget_str.find('時')):
                    hour = _trans(ntarget_str[:ntarget_str.index('時')])
                    if('分' in ntarget_str):
                        minute = _trans(ntarget_str[ntarget_str.index(
                            '點') + 1:ntarget_str.index('分')])
                result.append(time_str)
                time_str = time_str[0:11] + ("%02d:%02d" % (hour, minute))
                input_str = input_str[ntarget_obj.end():]
        elif(mode == 0):
            result.append(None)
        result.append(input_str)
        return result
        #######################################################################
    if(date.search(input_str)):
        target_obj = date.search(input_str)
        month = _trans(input_str[target_obj.start():input_str.index('月')])
        # print(target_obj.group())
        if('日' in target_obj.group()):
            day = _trans(input_str[input_str.index(
                '月') + 1:input_str.index('日')])
            # print(day)
        elif('號' in target_obj.group()):
            day = _trans(input_str[input_str.index(
                '月') + 1:input_str.index('號')])
            # print(day)
        input_str = input_str[target_obj.end():]
    if(time.search(input_str)):
        target_obj = time.search(input_str)
        target_str = target_obj.group()
        if('點' in target_obj.group() and target_obj.group()[:target_obj.group().index('點')].isnumeric()):
            hour = _trans(input_str[target_obj.start():input_str.index('點')])
            input_str = input_str[input_str.index('點') + 1:]
            if(one_99.search(input_str)):
                # print(one_99.search(input_str).group())
                minute = _trans(one_99.search(input_str).group())
                input_str = input_str[one_99.search(input_str).end():]
                if('分' in input_str):
                    input_str = input_str[1:]
                # minute = _trans(input_str[:input_str.index('分')])
                # input_str = input_str[input_str.index('分')+1:]
            else:
                minute = 0
            # print(hour)
        elif('時' in target_obj.group() and target_obj.group()[:target_obj.group().index('時')].isnumeric()):
            hour = _trans(input_str[target_obj.start():input_str.index('時')])
            input_str = input_str[input_str.index('時') + 1:]
            if('分' in target_str):
                minute = _trans(input_str[:input_str.index('分')])
                input_str = input_str[input_str.index('分') + 1:]
                # print(minute)
            else:
                minute = 0
            # print(hour)
        # print(day)
    if(target_obj):
        result.append(set_time([month, day, hour, minute]))
    else:
        result.append(shift_time(0, 0, 0))
    if(mode == 0 and ('到' or ' 到') in input_str):
        if(time.search(input_str)):
            time_inter = 1
            target_obj = time.search(input_str)
            # print("======TO======")
            if('點' in target_obj.group()):
                endhour = _trans(
                    input_str[target_obj.start():input_str.index('點')])
                input_str = input_str[input_str.index('點') + 1:]
                # print(endhour)
            elif('時' in target_obj.group()):
                endhour = _trans(
                    input_str[target_obj.start():input_str.index('時')])
                input_str = input_str[input_str.index('時') + 1:]
                # print(endhour)
            if(one_99.search(input_str)):
                # print(one_99.search(input_str).group())
                endminute = _trans(one_99.search(input_str).group())
                input_str = input_str[one_99.search(input_str).end():]
            else:
                endminute = 0
            result.append(set_time([month, day, endhour, endminute]))
        else:
            time_inter = 0
            result.append(None)
    else:
        time_inter = 0
        result.append(None)
    result.append(input_str.lstrip())
    return result


def target_countdown(full_input_str):
    input_str = cn2an.transform(zh2cnnum(full_input_str), "cn2an")
    hour, minute, second = None, None, None
    time = re.compile(r"(計時-?(\d+(小時))?-?(\d+(分鐘))?-?(\d+秒)?)")
    if(time.search(input_str)):
        input_str = time.search(input_str).group()[2:]
        if('小時' in input_str):
            hour = int(input_str[:input_str.index('小時')])
            input_str = input_str[input_str.index('小時') + 2:]
        if('分鐘' in input_str):
            minute = int(input_str[:input_str.index('分鐘')])
            input_str = input_str[input_str.index('分鐘') + 2:]
        if('秒' in input_str):
            second = int(input_str[:input_str.index('秒')])
            input_str = input_str[input_str.index('秒') + 1:]
        if(hour == None and minute == None and second == None):
            return [-1, -1, -1]
        else:
            return [hour, minute, second]
    else:
        return [-1, -1, -1]
# enter a full input str to get final result


def target_alarm(input_str):
    day = None
    hour = None
    minute = None
    day_re = re.compile(r'星期(一|二|三|四|五|六|七|日)')
    day_obj = day_re.match(input_str)
    later_re = re.compile(r'((明|後|大後)天)|((\d+)天後?)')
    later_obj = later_re.match(cn2an.transform(input_str, 'cn2an'))
    if(day_obj):
        day = day_dict[(day_obj.group(1))]
        input_str = input_str[day_obj.end():]
    elif(later_obj):
        day = datetime.datetime.today().weekday()
        if(later_obj.group(2)):
            later = later_obj.group(2)
            if(later == '明'):
                day += 1
            elif(later == '後'):
                day += 2
            elif(later == '大後'):
                day += 3
            else:
                day += 0
        elif(later_obj.group(4)):
            later = later_obj.group(4)
            day += int(later)
        else:
            day += 0
        day = day % 7 + 1
        input_str = input_str[later_obj.end():]
    input_str = input_str.replace('兩', '2')
    input_str = cn2an.transform(input_str, "cn2an")
    time = re.compile(r'((\d+)(點|時)(\d+)分)')
    time_obj = time.match(input_str)
    if(time_obj):
        hour = int(time_obj.group(2))
        minute = int(time_obj.group(4))
        input_str = input_str[time_obj.end():]
    return [day, hour, minute]


def target_volume(input_str):
    percent = re.compile(
        r'((\d+)|((一百)|(二|三|四|五|六|七|八|九)?((十?(一|二|兩|三|四|五|六|七|八|九))|十)))(趴|%)?')
    target_obj = percent.search(input_str)
    if('零' in input_str):
        target_num = 0
    elif('百' in input_str or '千' in input_str):
        target_num = 100
    elif(target_obj):
        target_str = target_obj.group()
        if('趴' in target_str):
            target_str = target_str.replace('趴', '')
        elif('%' in target_str):
            target_str = target_str.replace('%', '')
        target_num = _trans(target_str)
        if('百' in input_str or target_num > 100):
            target_num = 100
    else:
        return [None]
    if(input_str[0] == '負' or input_str[0] == '-'):
        target_num *= -1
    return [target_num]

def target_place(input_str):
    place = None
    place_re = re.compile(r'((.*)時間)|((.*)時區)')
    place_obj = place_re.search(input_str)
    if(place_obj):
        if('時間' in input_str):
            place = [place_obj.group(2)]
        elif('時區' in input_str):
            place = [place_obj.group(4)]
    else:
        return [input_str]
    return place


def target_language(inputSTR):
    language_dict = {"中文": "zh-TW", "英文": "en"}
    if('翻' in inputSTR):
        fromLanguage = inputSTR[:inputSTR.index('翻')]
        fromLanguage.lstrip()
        toLanguage = inputSTR[inputSTR.index('翻') + 1:]
        toLanguage.lstrip()
        if(len(fromLanguage) == 0 or len(toLanguage) == 0 or (fromLanguage not in language_dict) or (toLanguage not in language_dict)):
            return []
        else:
            return (language_dict[fromLanguage], language_dict[toLanguage])
    else:
        return []
