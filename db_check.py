import sqlite3


# SQLiteデータベースに接続
conn = sqlite3.connect("music_collection.db")

# SQLを実行するためのカーソルを作成
cursor = conn.cursor()


# テストデータを登録
cursor.execute("""
    INSERT INTO collections (
        musicbrainz_id,
        artist,
        album
    )
    VALUES (?, ?, ?)
""", (
    "test-001",
    "Queen",
    "A Night at the Opera"
))


# 変更を確定
conn.commit()


# collectionsテーブルのデータを取得
cursor.execute("SELECT * FROM collections")

rows = cursor.fetchall()


# 取得したデータを表示
for row in rows:
    print(row)


# データベースを閉じる
conn.close()