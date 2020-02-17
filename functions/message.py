
def build(time, next_or_last):
    if time == False:
        return "駅名が存在しないよ！"
    else:
        if time["up"] == None:
            up_message = "上り：本日は終了です！"
        if time["down"] == None:
            down_message = "下り：本日は終了です！"
        if time["up"] != None and time["down"] != None:
            up_message = time["up"]["dest"] + "行き：" + time["up"]["hour"] + "時" + time["up"]["minute"] + "分"
            down_message = time["down"]["dest"] + "行き：" + time["down"]["hour"] + "時" + time["down"]["minute"] + "分"

        return next_or_last + "\n\n" + up_message + "\n" + down_message + "\n" + "遅延情報：なし"
