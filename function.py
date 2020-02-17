# メッセージの作成
def create_message(info, next_or_last):
    if info == False:
        return "駅名が存在しないよ！"
    else:
        if info["up"] == None:
            up_message = "上り：本日は終了です！"
        if info["down"] == None:
            down_message = "下り：本日は終了です！"
        if info["up"] != None and info["down"] != None:
            up_message = info["up"]["dest"] + "行き：" + info["up"]["hour"] + "時" + info["up"]["minute"] + "分"
            down_message = info["down"]["dest"] + "行き：" + info["down"]["hour"] + "時" + info["down"]["minute"] + "分"

        return next_or_last + "\n\n" + up_message + "\n" + down_message + "\n" + "遅延情報：なし"
