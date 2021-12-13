import os
from linebot.models import *
from linebot.exceptions import (InvalidSignatureError)
from linebot import (LineBotApi, WebhookHandler)
from flask import Flask, request, abort
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
import time
import json
import random

VERIFICATION_PATH = "./Verification_code.json"


class Delivery:
    # 建構子

    # 設定驗證碼
    def setVerificationCode(self, event):
        code_list = []
        len = 8
        for i in range(10):  # 0-9數字
            code_list.append(str(i))
        for i in range(65, 91):  # 對應從“A”到“Z”的ASCII碼
            code_list.append(chr(i))
        for i in range(97, 123):  # 對應從“a”到“z”的ASCII碼
            code_list.append(chr(i))
        myslice = random.sample(code_list, len)  # 從list中隨機獲取6個元素，作為一個片斷返回
        verification_code = ''.join(myslice)  # list to string

        Time = time.time()
        fileName = VERIFICATION_PATH
        jsonString = {"verification": verification_code, "time": Time}
        #jsonString = json.loads(jsonString)

        file = open(fileName, "w")
        json.dump(jsonString, file)
        file.close()
        #replyMsg = {"type": 'text', "text": verification_code}
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=verification_code))

    # 檢查驗證碼
    def checkVerificationCode(self, event):
        with open(VERIFICATION_PATH) as f:
            code = json.load(f)
        if code['verification'] == event.message.text:  # 驗證碼正確
            today = time.time()
            if today - code['time'] <= 300:  # 時間內
                # 回傳LINEID
                print(event)
                #replyMsg = event.source
            else:
                replyMsg = "驗證碼已過期"
        else:  # 驗證碼錯誤
            replyMsg = "驗證碼錯誤"
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=replyMsg))
    # 透過LINE傳送

    def LINE_push_message(searchResultURL, userLINEID, searchKeyWord, channel_access_token):

        try:
            line_bot_api.push_message(
                userLINEID, TextSendMessage("搜尋關鍵字：" + searchKeyWord + "\n搜尋結果:" + searchResultURL))
        except LineBotApiError as e:
            pass
            # error handle

    #    def deliver_to_cellphone(resultURL, keyWord):


app = Flask(__name__)
line_bot_api = LineBotApi(
    'DDtWE84ugYYwdBxhJV8dd65JrEEeFoK0HzTmYk32FJYsZLeDEIschqNASNqRiILtGqhXbJbj/bW7A72l+7E3wxVmXDRlz4kgOZ/aV17mnW7PsCs3ZAe3hE50yM4yRMphRnm08lR0b+VOorUD6hUJngdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('384462bb9f27a9ab50f784441a4e45a2')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event.message.text)
    message = TextSendMessage(text=event.message.text)
    if event.message.text == "設定驗證碼":
        delivery.setVerificationCode(event)
    else:
        delivery.checkVerificationCode(event)
    #line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    delivery = Delivery()
    app.run()
