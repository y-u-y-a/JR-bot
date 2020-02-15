from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage

from flask import Flask, request, abort
import os
import scrape as sc
import function as func

# Flaskクラスのインスタンスを生成し、変数appに代入する
app = Flask(__name__)

# 環境変数の取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET       = os.environ["LINE_CHANNEL_SECRET"]
# Botのインスタンスの作成
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# webhookとはイベント発生時に指定したURLにPOSTリクエストする仕組みのこと
handler      = WebhookHandler(LINE_CHANNEL_SECRET)

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
# 駅名から列車到着時刻を取得する
def reply_message(event):  # "event"には、"MessageEvent"が入る
    get_text = event.message.text.replace("駅", "")

    if "終電" in get_text:
        station_name = get_text.replace("終電", "")
        if station_name == "":
            station_name = "あああ"
        info = sc.reply_last_time(station_name)
        next_or_last = "終電"
    else:
        info = sc.reply_next_time(station_name)
        next_or_last = "次の出発"
    # メッセージをビルド
    message = func.create_message(info, next_or_last)
    line_bot_api.reply_message(
        event.reply_token, # 送信相手とのトークン？
        TextSendMessage(
            text=message
        )
    )

# "__name__"はこのファイルが呼ばれたファイルの名前が入る(ここでは"main")
if __name__ == "__main__":
    # webサーバーの立ち上げ
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
