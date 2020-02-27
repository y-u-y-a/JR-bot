from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate,URIAction
)
import os
from flask import Flask, request, abort
from functions import times, message

# Flaskクラスのインスタンスを生成
app = Flask(__name__)

# 環境変数の取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
# Botのインスタンスの作成
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Flaskクラスで用意してあるrouteというメソッドをデコレートして実行
@app.route("/callback", methods=['POST'])
# webhookからのリクエスト検証を行う
def callback():
    # リクエストヘッダーから署名検証のための値を取得する
    signature = request.headers['X-Line-Signature']
    # リクエストボディを取得する
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # 署名検証で例外処理
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# WebhookHandlerクラスで用意してあるaddというメソッドをデコレートして実行
@handler.add(MessageEvent, message=TextMessage)
def reply_message(MessageEvent):

    station_name = MessageEvent.message.text.replace("駅", "")
    # 時刻取得
    next_time = times.get(station_name, "next")
    last_time = times.get(station_name, "last")
    # messageビルド
    message_last = message.build(next_time, "次の出発")
    message_next = message.build(last_time, "最終")
    # テキスト送信
    line_bot_api.reply_message(
        MessageEvent.reply_token, [
            # テキストmessage
            TextSendMessage(text=message_last),
            TextSendMessage(text=message_next),
            # ボタンmessage
            # TemplateSendMessage(
            #     alt_text="JR-times",
            #     template=ButtonsTemplate(
            #         title="全ての時刻表を表示する",
            #         text="外部ページにアクセスします",
            #         thumbnail_image_url="./images/JR.jpeg",
            #         image_size="cover",
            #         actions=[
            #             URIAction(
            #                 uri="https://qiita.com/shimayu22/items/c599a94dfa39c6466dfa",
            #                 label="移動する"
            #             )
            #         ]
            #     )
            # )
        ]
    )

# "__name__"はこのファイルが呼ばれたファイルの名前が入る(ここでは"main")
if __name__ == "__main__":
    # webサーバーの立ち上げ
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
