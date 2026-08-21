import sqlite3


# SQLiteデータベースに接続
conn = sqlite3.connect("music_collection.db")

# SQLを実行するためのカーソルを作成
cursor = conn.cursor()

# collectionsテーブルを作成
cursor.execute("""
    CREATE TABLE IF NOT EXISTS collections (
        id INTEGER PRIMARY KEY,
        musicbrainz_id TEXT NOT NULL UNIQUE,
        artist TEXT NOT NULL,
        album TEXT NOT NULL,
        release_date TEXT,
        format TEXT,
        label TEXT,
        country TEXT,
        jacket_url TEXT,
        cd_owned INTEGER DEFAULT 0 CHECK(cd_owned IN (0, 1)),
        vinyl_owned INTEGER DEFAULT 0 CHECK(vinyl_owned IN (0, 1)),
        memo TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
""")

# 変更を確定
conn.commit()

# データベースとの接続を終了
conn.close()