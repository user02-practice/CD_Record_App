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
                release_name TEXT NOT NULL
            )
        """)

        # テーブル作成を確定する
        self.conn.commit()

    def add_collection(
        self,
        musicbrainz_id,
        artist_name,
        release_name
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
        """

        # SQLを実行するためのカーソルを作成する
        cursor = self.conn.cursor()

        # コレクションをDBへ登録する
        cursor.execute("""
            INSERT INTO collections (
                musicbrainz_id,
                artist_name,
                release_name
            )
            VALUES (?, ?, ?)
        """, (
            musicbrainz_id,
            artist_name,
            release_name
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
                release_name
            FROM collections
            WHERE musicbrainz_id = ?
        """, (musicbrainz_id,))

        # 検索結果を1件取得する
        result = cursor.fetchone()

        # 取得した結果を返す
        return result

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