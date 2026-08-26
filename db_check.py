import sqlite3


# データベースに接続
conn = sqlite3.connect("music_collection.db")

# カーソルを作成
cursor = conn.cursor()


# collectionsテーブルの構造を確認
cursor.execute("PRAGMA table_info(collections)")

columns = cursor.fetchall()

for column in columns:
    print(column)


# 接続を閉じる
conn.close()