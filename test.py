from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import os

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
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    app.run()
