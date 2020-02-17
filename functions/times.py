import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
import pytz

# 取得した駅名からその駅の到着時刻を取得(岡山から下関間)
def get(station_name, next_or_last):

    # 駅名のチェック
    url = get_station_url(station_name)
    if url == False:
        return False

    # HTMLの解析開始
    time.sleep(1)
    res = requests.get(url)
    html = BeautifulSoup(res.content, "html.parser")

    # レスポンス
    if next_or_last == "next":
        return {
            "up": scrape(html, "weekday-0", next_or_last),
            "down": scrape(html, "weekday-1", next_or_last)
        }
    elif next_or_last == "last":
        return {
            "up": scrape(html, "weekday-0", next_or_last),
            "down": scrape(html, "weekday-1", next_or_last)
        }


def scrape(html, up_or_down, next_or_last):

    # 現在時刻の取得
    now_time = {
        "hour": datetime.datetime.now(pytz.timezone('Asia/Tokyo')).hour,
        "minute": datetime.datetime.now(pytz.timezone('Asia/Tokyo')).minute
    }
    # 0時は24時扱い
    if now_time["hour"] == 0:
        now_time["hour"] = 24
        # 1~4時の間は5時扱い
    if 1 <= now_time["hour"] <= 4:
        now_time["hour"] = 5
        now_time["minute"] = 0

    # 時刻のスクレイピング
    if next_or_last == "next":
        dl_tags  = html.find(id=up_or_down).select("dl")
        # 時刻ごとのレコード
        for dl_tag in dl_tags:
            hour = get_hour(dl_tag, now_time["hour"])
            if hour != None:
                min_dest = get_min_dest(dl_tag, now_time["minute"])
                if min_dest != None:
                    return {
                        "hour": hour,
                        "minute": min_dest["min"],
                        "dest": min_dest["dest"]
                    }
                else:
                    now_time["minute"] = 0
                    now_time["hour"] += 1
                    # 24時だった場合の回避
                    if now_time["hour"] == 25:
                        break

    elif next_or_last == "last":
        dl_tags = html.find(id=up_or_down).find(class_="diagram-frame")
        hour = dl_tags.select("dt")[-1].text
        min = dl_tags.select(".time")[-1].text
        dest = dl_tags.select(".ruby-dest")[-1].text
        return {
            "hour": str(hour),
            "minute": str(min),
            "dest": str(dest)
        }


def get_hour(dl_tag, hour):
    get_hour = int(dl_tag.find("dt").text)
    if get_hour == hour:
        return str(get_hour)


def get_min_dest(dl_tag, minute):
    # "時"のレコード内の"分"でループ
    for tag in dl_tag.select(".time-frame"):
        min  = tag.find(class_="time").text
        dest = tag.find(class_="ruby-dest").text
        # "分"を取得する条件
        if int(min) >= minute:
            return {
                "min": str(min),
                "dest": str(dest)
            }
            break


# NAVITIMEから駅の時刻表ページのURLを取得
def get_station_url(station_name):
    # 下関~岡山
    url = "https://www.navitime.co.jp/diagram/stationList?lineId=00000070&from=diagram.campany.top"
    res = requests.get(url)
    html = BeautifulSoup(res.content, "html.parser")
    station_links = html.find(class_="node-list").select("a")
    # 駅名の確認とURLの取得
    station_url = False
    for a in station_links:
        if station_name in a.text:
            station_url = "https:" + a["href"]
            break
    return station_url
