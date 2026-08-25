import sqlite3


class CollectionRepository:
    """
    collectionsテーブルを操作するクラス。

    コレクションの登録や取得など、
    SQLiteデータベースに関する処理を担当する。
    """

    def __init__(self, database_path):
        """
        データベースの接続先を設定する。

        Args:
            database_path (str):
                SQLiteデータベースのファイルパス。
                ":memory:"を指定すると、
                テスト用のメモリ上のデータベースを使用する。
        """

        # 使用するデータベースのパスを保存する
        self.database_path = database_path

        # データベースに接続する
        self.conn = sqlite3.connect(self.database_path)

        # テーブルが存在しない場合は作成する
        self._create_table()

    def _create_table(self):
        """
        collectionsテーブルを作成する。

        すでにテーブルが存在する場合は何もしない。
        """

        # SQLを実行するためのカーソルを作成する
        cursor = self.conn.cursor()

        # collectionsテーブルを作成する
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collections (
                id INTEGER PRIMARY KEY,
                musicbrainz_id TEXT NOT NULL UNIQUE,
                artist_name TEXT NOT NULL,
                release_name TEXT NOT NULL,
                label TEXT,
                release_date TEXT,
                country TEXT,
                format TEXT,
                cd_owned INTEGER NOT NULL DEFAULT 0,
                vinyl_owned INTEGER NOT NULL DEFAULT 0,
                memo TEXT
            )
        """)

        # テーブル作成を確定する
        self.conn.commit()

    def add_collection(
        self,
        musicbrainz_id,
        artist_name,
        release_name,
        label,
        release_date,
        country,
        formats,
        cd_owned,
        vinyl_owned,
        memo
    ):
        """
        コレクションをDBへ登録する。

        Args:
            musicbrainz_id (str):
                MusicBrainzの作品ID。

            artist_name (str):
                アーティスト名。

            release_name (str):
                作品名。

            label (str):
                レーベル名。

            release_date (str):
                発売日。

            country (str):
                発売国。

            formats (list):
                CDやVinylなどのフォーマット一覧。

            cd_owned (int):
                CDを所有しているか。
                0 = 未所有、1 = 所有。

            vinyl_owned (int):
                Vinylを所有しているか。
                0 = 未所有、1 = 所有。

            memo(str):
            コレクションに関するメモ。
        """

        # SQLを実行するためのカーソルを作成する
        cursor = self.conn.cursor()

        # PythonのリストをSQLite保存用の文字列へ変換する
        format_text = ",".join(formats)

        # コレクションをDBへ登録する
        cursor.execute("""
            INSERT INTO collections (
                musicbrainz_id,
                artist_name,
                release_name,
                label,
                release_date,
                country,
                format,
                cd_owned,
                vinyl_owned,
                memo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            musicbrainz_id,
            artist_name,
            release_name,
            label,
            release_date,
            country,
            format_text,
            cd_owned,
            vinyl_owned,
            memo
        ))

        # DBへの変更を確定する
        self.conn.commit()

    def get_collection(self, musicbrainz_id):
        """
        MusicBrainz IDを使ってコレクションを1件取得する。

        Args:
            musicbrainz_id (str):
                取得したい作品のMusicBrainz ID。

        Returns:
            tuple:
                DBから取得した作品情報。
                見つからない場合はNone。
        """

        # SQLを実行するためのカーソルを作成する
        cursor = self.conn.cursor()

        # 指定されたMusicBrainz IDの作品を検索する
        cursor.execute("""
            SELECT
                musicbrainz_id,
                artist_name,
                release_name,
                label,
                release_date,
                country,
                format,
                cd_owned,
                vinyl_owned,
                memo
            FROM collections
            WHERE musicbrainz_id = ?
        """, (musicbrainz_id,))

        # 検索結果を1件取得する
        result = cursor.fetchone()

        # コレクションが存在しない場合
        if result is None:
            return None

        # DBから取得したformatをPythonのリストへ戻す
        formats = result[6].split(",") if result[6] else []

        # tupleを作り直して返す
        return (
            result[0],
            result[1],
            result[2],
            result[3],
            result[4],
            result[5],
            formats,
            result[7],
            result[8],
            result[9]

        )

    def get_collections(self):
        """
        登録されているコレクションをすべて取得する。

        Returns:
            list:
                コレクションの一覧。
                コレクションが存在しない場合は空のリスト。
        """

        # SQLを実行するためのカーソルを作成する
        cursor = self.conn.cursor()

        # コレクションをすべて取得する
        cursor.execute("""
            SELECT
                musicbrainz_id,
                artist_name,
                release_name,
                label,
                release_date,
                country,
                format,
                cd_owned,
                vinyl_owned,
                memo
            FROM collections
            ORDER BY id
        """)

        # 検索結果をすべて取得する
        results = cursor.fetchall()

        collections = []

        # DBから取得したデータをPythonで扱いやすい形に変換する
        for result in results:

            # formatを文字列からリストへ戻す
            formats = result[6].split(",") if result[6] else []

            collections.append((
                result[0],
                result[1],
                result[2],
                result[3],
                result[4],
                result[5],
                formats,
                result[7],
                result[8],
                result[9]
            ))

        return collections

    def update_collection(
        self,
        musicbrainz_id,
        cd_owned,
        vinyl_owned,
        memo
    ):
        """
        コレクションの所有状態とメモを更新する。

        Args:
            musicbrainz_id (str):
                更新する作品のMusicBrainz ID。

            cd_owned (int):
                CDを所有しているか。
                0 = 未所有、1 = 所有。

            vinyl_owned (int):
                Vinylを所有しているか。
                0 = 未所有、1 = 所有。

            memo (str):
                コレクションに関するメモ。
        """

        # コレクションを更新する
        self.conn.execute(
            """
            UPDATE collections
            SET
                cd_owned = ?,
                vinyl_owned = ?,
                memo = ?
            WHERE musicbrainz_id = ?
            """,
            (
                cd_owned,
                vinyl_owned,
                memo,
                musicbrainz_id
            )
        )

        # DBへの変更を確定する
        self.conn.commit()

    def delete_collection(self, musicbrainz_id):
        """指定したMusicBrainz IDのコレクションを削除する"""

        self.conn.execute(
            """
            DELETE FROM collections
            WHERE musicbrainz_id = ?
            """,
            (musicbrainz_id,)
        )

        self.conn.commit()