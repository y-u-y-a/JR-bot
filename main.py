from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage

from flask import Flask, request, abort
import os
import scrape
import function as func

# Flaskクラスのインスタンスを生成し、変数appに代入する
app = Flask(__name__)

# 環境変数の取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET       = os.environ["LINE_CHANNEL_SECRET"]
# Botのインスタンスの作成
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# webhookとはイベント発生時に指定したURLにPOSTリクエストする仕組みのこと
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Flaskクラスで用意してあるrouteというメソッドをデコレートしている
@app.route("/callback", methods=['POST'])
# webhookからのリクエスト検証を行う
def callback():
    # リクエストヘッダーから署名検証のための値を取得する
    signature = request.headers['X-Line-Signature']
    # リクエストボディを取得する
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # 署名検証で例外ならばエラーを出す
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# WebhookHandlerクラスで用意してあるaddというメソッドをデコレートしている
@handler.add(MessageEvent, message=TextMessage)

def reply_message(MessageEvent):
    station_name = MessageEvent.message.text.replace("駅", "")

    if "終電" in station_name:
        station_name = station_name.replace("終電", "")

        get_data = scrape.reply_last_time(station_name)
        pre_message = "最終"

    else:
        get_data = scrape.reply_next_time(station_name)
        pre_message = "次の出発"

    # メッセージをビルド
    message = func.create_message(get_data)

    line_bot_api.reply_message(
        MessageEvent.reply_token, [
            TextSendMessage(text=pre_message),
            TextSendMessage(text=message)
        ]
    )

# "__name__"はこのファイルが呼ばれたファイルの名前が入る(ここでは"main")
if __name__ == "__main__":
    # webサーバーの立ち上げ
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
