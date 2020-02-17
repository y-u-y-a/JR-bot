# メッセージの作成
def create_message(data):
    if data == False:
        return "駅名が存在しないよ！"
    else:
        if data["up"] == None:
            up_message = "上り：本日は終了です！"
        if data["down"] == None:
            down_message = "下り：本日は終了です！"
        if data["up"] != None and data["down"] != None:
            up_message = data["up"]["dest"] + "行き：" + data["up"]["hour"] + "時" + data["up"]["minute"] + "分"
            down_message = data["down"]["dest"] + "行き：" + data["down"]["hour"] + "時" + data["down"]["minute"] + "分"

        return up_message + "\n" + down_message + "\n" + "遅延情報：なし"
