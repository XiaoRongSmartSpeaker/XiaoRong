import requests
import json
import urllib.request
import datetime
import os
from dotenv import load_dotenv
import threading
import logger
logger = logger.get_logger(__name__)


class Weather:

    def __init__(self):
        load_dotenv()
        self.__weather_api_key = os.getenv('WEATHER_API_KEY')
        self.thread = None

    def import_thread(self, thread):
        self.thread = thread

    def weather_forecast(self, time, place):

        print(type(time))
        logger.info(f"[weather_forcast] 收到 {time} {place}")
        listTaiwan = [
            '新竹縣',
            '金門縣',
            '苗栗縣',
            '新北市',
            '宜蘭縣',
            '雲林縣',
            '臺南市',
            '高雄市',
            '彰化縣',
            '臺北市',
            '南投縣',
            '澎湖縣',
            '基隆市',
            '桃園市',
            '花蓮縣',
            '連江縣',
            '臺東縣',
            '嘉義市',
            '嘉義縣',
            '屏東縣',
            '臺中市',
            '新竹市']

        listWorld = [
            '東京',
            '大阪',
            '首爾',
            '曼谷',
            '雅加達',
            '吉隆坡',
            '新加坡',
            '馬尼拉',
            '胡志明市',
            '河內',
            '海參威',
            '伯力',
            '關島',
            '檀香山',
            '威靈頓',
            '奧克蘭',
            '雪梨機場',
            '伯斯',
            '布里斯班',
            '瀋陽',
            '青島',
            '北京',
            '南京',
            '開封',
            '蘭州',
            '武漢',
            '重慶',
            '昆明',
            '上海',
            '南昌',
            '杭州',
            '廣州',
            '福州',
            '香港',
            '海口',
            '西安',
            '墨爾本',
            '雪梨',
            '洛杉磯',
            '拉斯維加斯',
            '舊金山',
            '西雅圖',
            '紐約',
            '華盛頓',
            '芝加哥',
            '邁阿密',
            '多倫多',
            '溫哥華',
            '蒙特婁',
            '墨西哥城',
            '里約',
            '聖地牙哥',
            '利瑪',
            '布宜諾斯艾利斯',
            '奧斯陸',
            '馬德里',
            '哥本哈根',
            '赫爾辛基',
            '法蘭克福',
            '柏林',
            '日內瓦',
            '布魯塞爾',
            '倫敦',
            '巴黎',
            '維也納',
            '羅馬',
            '威尼斯',
            '布達佩斯',
            '雅典',
            '華沙',
            '布拉格',
            '阿姆斯特丹',
            '斯德哥爾摩',
            '里斯本',
            '開羅',
            '約翰尼斯堡',
            '加德滿都',
            '新德里',
            '伊斯坦布爾',
            '莫斯科']

        listTaiwanEnglish = [
            'Hsinchu County',
            'Kinmen County',
            'Miaoli County',
            'New Taipei City',
            'Yilan County',
            'Yunlin County',
            'Tainan City',
            'Kaohsiung City',
            'Changhua County',
            'Taipei City',
            'Nantou County',
            'Penghu County',
            'Keelung City',
            'Taoyuan City',
            'Hualien County',
            'Lienchiang County',
            'Taitung County',
            'Chiayi City',
            'Chiayi County',
            'Pingtung County',
            'Taichung City',
            'Hsinchu City']

        url_Taiwan = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization={self.__weather_api_key}'

        url_World = f'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-007?Authorization={self.__weather_api_key}&downloadType=WEB&format=JSON'

        if place == "HERE":
            place = self.find_place()

        if place == '馬祖':
            place = '連江縣'

        r = requests.get(url_Taiwan)
        if place in listTaiwan:
            index = listTaiwan.index(place)
            r = requests.get(url_Taiwan)
            j = json.loads(r.text)
            data = j["records"]["locations"][0]["location"][index]
            # print(data)
            timeStart = data["weatherElement"][10]['time'][0]["startTime"]
            timeEnd = data["weatherElement"][10]['time'][0]["endTime"]
            if time < timeStart:
                message = "時間已過期，無法查詢"
                logger.info(f"[weather] 時間已過期，無法查詢 {time} < {timeStart}")

                self.thread.add_thread({
                    'class': 'TextToSpeech',
                    'func': 'text_to_voice',
                    'args': (message,),
                })

                return

            elif time < timeEnd:
                description = data["weatherElement"][10]['time'][0]["elementValue"][0]["value"]
            else:
                for i in range(1, 14):
                    timeEnd = data["weatherElement"][10]['time'][i]["endTime"]
                    if time < timeEnd:
                        description = data["weatherElement"][10]['time'][i]["elementValue"][0]["value"]
                        break
                    if i == 13:
                        timeEnd = data["weatherElement"][10]['time'][i]["endTime"]
                        if time > timeEnd:
                            message = "時間超過一週，無法查詢"

                            self.thread.add_thread({
                                'class': 'TextToSpeech',
                                'func': 'text_to_voice',
                                'args': (message,),
                            })

                            return

            self.thread.add_thread({
                'class': 'TextToSpeech',
                'func': 'text_to_voice',
                'args': (description,),
            })

            return

        elif place in listWorld:
            index = listWorld.index(place)
            r = requests.get(url_World)
            j = json.loads(r.text)
            data = j['cwbopendata']["dataset"]["location"][index]
            # print(data)
            time = time.split(' ')
            timeStart = data["weatherElement"][0]['time'][0]["startTime"]
            timeEnd = data["weatherElement"][0]['time'][0]["endTime"]
            timeStart = timeStart.split('T')
            timeEnd = timeEnd.split('T')

            if time[0] < timeStart[0]:
                message = "時間已過期，無法查詢"

                self.thread.add_thread({
                    'class': 'TextToSpeech',
                    'func': 'text_to_voice',
                    'args': (message,),
                })

                return

            elif time[0] == timeStart[0]:
                Wx = data["weatherElement"][0]['time'][0]["elementValue"][0]["value"]
                Tmax = data["weatherElement"][1]['time'][0]["elementValue"]["value"]
                Tmin = data["weatherElement"][2]['time'][0]["elementValue"]["value"]
                description = Wx + '。' + '溫度攝氏' + Tmax + '至' + Tmin + '度。'
            else:
                for i in range(1, 7):
                    timeStart = data["weatherElement"][0]['time'][i]["startTime"]
                    timeStart = timeStart.split('T')
                    if time[0] == timeStart[0]:
                        Wx = data["weatherElement"][0]['time'][i]["elementValue"][0]["value"]
                        Tmax = data["weatherElement"][1]['time'][i]["elementValue"]["value"]
                        Tmin = data["weatherElement"][2]['time'][i]["elementValue"]["value"]
                        description = Wx + '。' + '溫度攝氏' + Tmax + '至' + Tmin + '度。'
                        break
                    if i == 6:
                        timeStart = data["weatherElement"][0]['time'][i]["startTime"]
                        timeStart = timeStart.split('T')
                        if time[0] > timeStart[0]:
                            message = "時間超過一週，無法查詢"

                            self.thread.add_thread({
                                'class': 'TextToSpeech',
                                'func': 'text_to_voice',
                                'args': (message,),
                            })

                            return

            self.thread.add_thread({
                'class': 'TextToSpeech',
                'func': 'text_to_voice',
                'args': (description,),
            })

            return

        elif place == '':
            tmp = self.find_place()
            if tmp in listTaiwanEnglish:
                index = listTaiwanEnglish.index(tmp)
                place = listTaiwan[index]

                r = requests.get(url_Taiwan)
                j = json.loads(r.text)
                data = j["records"]["locations"][0]["location"][index]
                # print(data)
                timeStart = data["weatherElement"][10]['time'][0]["startTime"]
                timeEnd = data["weatherElement"][10]['time'][0]["endTime"]
                if time < timeStart:
                    message = "時間已過期，無法查詢"
                    self.thread.add_thread({
                        'class': 'TextToSpeech',
                        'func': 'text_to_voice',
                        'args': (message,),
                    })

                    return

                elif time < timeEnd:
                    description = data["weatherElement"][10]['time'][0]["elementValue"][0]["value"]
                else:
                    for i in range(1, 14):
                        timeEnd = data["weatherElement"][10]['time'][i]["endTime"]
                        if time < timeEnd:
                            description = data["weatherElement"][10]['time'][i]["elementValue"][0]["value"]
                            break
                        if i == 13:
                            timeEnd = data["weatherElement"][10]['time'][i]["endTime"]
                            if time > timeEnd:
                                message = "時間超過一週，無法查詢"

                                self.thread.add_thread({
                                    'class': 'TextToSpeech',
                                    'func': 'text_to_voice',
                                    'args': (message,),
                                })

                                return

                self.thread.add_thread({
                    'class': 'TextToSpeech',
                    'func': 'text_to_voice',
                    'args': (description,),
                })

                return

            else:
                message = "查無此地點"
                self.thread.add_thread({
                    'class': 'TextToSpeech',
                    'func': 'text_to_voice',
                    'args': (message,),
                })

                return
        else:
            message = "查無此地點"
            self.thread.add_thread({
                'class': 'TextToSpeech',
                'func': 'text_to_voice',
                'args': (message,),
            })

            return

    def find_place(self):
        with urllib.request.urlopen("https://geolocation-db.com/json") as url:
            data = json.loads(url.read().decode())
            if data['country_name'] == "Taiwan":
                # 如果在台灣 且 state 為 null 的話 回傳臺北市
                if data['state'] is None:
                    return '臺北市'
                else:
                    return data['state']


if __name__ == "__main__":
    time = "2022-01-15 12:00"
    place = "臺北市"
    weather = Weather()
    situation = weather.weather_forecast(time, place)
    print(situation)
