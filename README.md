# 目次
- LINE Developerの登録・設定
- herokuの登録・設定

- プログラム作成
- herokuに環境変数を登録
- herokuにデプロイ


# ファイルの説明
## main.py
呼び出す処理を記述
## scrape.py
→ Yahoo!ニュースへのスクレイピング処理
## Pipfile
→ pipenvによる設定ファイル(仮想環境)
## Procfile
→ herokuで実行するコマンドを記述
## requirements.txt
→ 使用するライブラリ一覧を記述
→ herokuはこれを参考にライブラリをインストール
## runtime.txt

