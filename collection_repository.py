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
                jacket_url TEXT,
                cd_owned INTEGER NOT NULL DEFAULT 0,
                vinyl_owned INTEGER NOT NULL DEFAULT 0,
                memo TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
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
            jacket_url,
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
                jacket_url,
                cd_owned,
                vinyl_owned,
                memo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            musicbrainz_id,
            artist_name,
            release_name,
            label,
            release_date,
            country,
            format_text,
            jacket_url,
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
                jacket_url,
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
            result[7],  # jacket_url
            result[8],  # cd_owned
            result[9],  # vinyl_owned
            result[10]  # memo
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
                jacket_url,
                cd_owned,
                vinyl_owned,
                memo
            FROM collections
            ORDER BY created_at DESC, id DESC
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
                result[7],  # jacket_url
                result[8],  # cd_owned
                result[9],  # vinyl_owned
                result[10]  # memo
            ))

        return collections

    def get_collections_sorted_by_artist(self):
        """
        コレクションをアーティスト名の昇順で取得する。

        Returns:
            list:
                アーティスト名で並び替えたコレクション一覧。
        """

        # SQLを実行するためのカーソルを作成する
        cursor = self.conn.cursor()

        # アーティスト名の昇順でコレクションを取得する
        cursor.execute("""
            SELECT
                musicbrainz_id,
                artist_name,
                release_name,
                label,
                release_date,
                country,
                format,
                jacket_url,
                cd_owned,
                vinyl_owned,
                memo
            FROM collections
            ORDER BY artist_name COLLATE NOCASE ASC, id ASC
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
                result[7],  # jacket_url
                result[8],  # cd_owned
                result[9],  # vinyl_owned
                result[10]  # memo
            ))

        return collections

    def get_collections_by_cd_owned(self):
        """
        CDを所有しているコレクションだけを取得する。

        Returns:
            list:
                CDを所有しているコレクションの一覧。
        """

        # SQLを実行するためのカーソルを作成する
        cursor = self.conn.cursor()

        # CDを所有しているコレクションを取得する
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
            WHERE cd_owned = 1
            ORDER BY created_at DESC, id DESC
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

    def get_collections_by_vinyl_owned(self):
        """
        Vinylを所有しているコレクションだけを取得する。

        Returns:
            list:
                Vinylを所有しているコレクションの一覧。
        """

        # SQLを実行するためのカーソルを作成する
        cursor = self.conn.cursor()

        # Vinylを所有しているコレクションを取得する
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
            WHERE vinyl_owned = 1
            ORDER BY created_at DESC, id DESC
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

    def search_collections(self, keyword):
        """
        アーティスト名、作品名、メモから
        コレクションを検索する。

        Args:
            keyword (str):
                検索するキーワード。

        Returns:
            list:
                キーワードに一致するコレクションの一覧。
        """

        # SQLを実行するためのカーソルを作成する
        cursor = self.conn.cursor()

        # アーティスト名、作品名、メモを部分一致で検索する
        cursor.execute("""
            SELECT
                musicbrainz_id,
                artist_name,
                release_name,
                label,
                release_date,
                country,
                format,
                jacket_url,
                cd_owned,
                vinyl_owned,
                memo
            FROM collections
            WHERE artist_name LIKE ?
               OR release_name LIKE ?
               OR memo LIKE ?
            ORDER BY created_at DESC, id DESC
        """, (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        ))

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
                result[7],  # jacket_url
                result[8],  # cd_owned
                result[9],  # vinyl_owned
                result[10]  # memo
            ))

        return collections

    def search_collections_by_artist(self, keyword):
        """
        アーティスト名だけを対象に
        コレクションを検索する。

        Args:
            keyword (str):
                検索するアーティスト名。

        Returns:
            list:
                アーティスト名に一致するコレクションの一覧。
        """

        # SQLを実行するためのカーソルを作成する
        cursor = self.conn.cursor()

        # アーティスト名を部分一致で検索する
        cursor.execute("""
            SELECT
                musicbrainz_id,
                artist_name,
                release_name,
                label,
                release_date,
                country,
                format,
                jacket_url,
                cd_owned,
                vinyl_owned,
                memo
            FROM collections
            WHERE artist_name LIKE ?
            ORDER BY created_at DESC, id DESC
        """, (
            f"%{keyword}%",
        ))

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
                result[7],  # jacket_url
                result[8],  # cd_owned
                result[9],  # vinyl_owned
                result[10]  # memo
            ))

        return collections

    def search_collections_by_album(self, keyword):
        """
        アルバム名だけを対象に
        コレクションを検索する。

        Args:
            keyword (str):
                検索するアルバム名。

        Returns:
            list:
                アルバム名に一致するコレクションの一覧。
        """

        # SQLを実行するためのカーソルを作成する
        cursor = self.conn.cursor()

        # アルバム名を部分一致で検索する
        cursor.execute("""
            SELECT
                musicbrainz_id,
                artist_name,
                release_name,
                label,
                release_date,
                country,
                format,
                jacket_url,
                cd_owned,
                vinyl_owned,
                memo
            FROM collections
            WHERE release_name LIKE ?
            ORDER BY created_at DESC, id DESC
        """, (
            f"%{keyword}%",
        ))

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
                result[7],  # jacket_url
                result[8],  # cd_owned
                result[9],  # vinyl_owned
                result[10]  # memo
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

    def filter_collections(
            self,
            keyword="",
            cd_owned=None,
            vinyl_owned=None,
            search_target="キーワード"
    ):
        """
        検索対象、キーワード、CD/Vinyl所有状態を組み合わせて
        コレクションを絞り込む。

        Args:
            keyword (str):
                検索するキーワード。

            cd_owned (bool or None):
                CD所有状態。
                True = 所有、False = 未所有、None = 条件なし。

            vinyl_owned (bool or None):
                Vinyl所有状態。
                True = 所有、False = 未所有、None = 条件なし。

            search_target (str):
                検索対象。
                「アーティスト」「アルバム」「キーワード」のいずれか。

        Returns:
            list:
                条件に一致するコレクションの一覧。
        """

        # SQLの条件を入れるリスト
        conditions = []

        # SQLへ渡す値を入れるリスト
        parameters = []

        # ========================================
        # キーワード検索
        # ========================================

        # キーワードが指定されている場合
        if keyword:

            # アーティスト名だけを検索する
            if search_target == "アーティスト":
                conditions.append(
                    "artist_name LIKE ?"
                )

                parameters.append(
                    f"%{keyword}%"
                )

            # アルバム名だけを検索する
            elif search_target == "アルバム":
                conditions.append(
                    "release_name LIKE ?"
                )

                parameters.append(
                    f"%{keyword}%"
                )

            # アーティスト名・作品名・メモをまとめて検索する
            else:
                conditions.append(
                    "(artist_name LIKE ? OR release_name LIKE ? OR memo LIKE ?)"
                )

                parameters.append(f"%{keyword}%")
                parameters.append(f"%{keyword}%")
                parameters.append(f"%{keyword}%")

        # ========================================
        # 所有状態の絞り込み
        # ========================================

        # CD所有状態が指定されている場合
        if cd_owned is not None:
            conditions.append(
                "cd_owned = ?"
            )

            parameters.append(
                1 if cd_owned else 0
            )

        # Vinyl所有状態が指定されている場合
        if vinyl_owned is not None:
            conditions.append(
                "vinyl_owned = ?"
            )

            parameters.append(
                1 if vinyl_owned else 0
            )

        # ========================================
        # SQLを作成する
        # ========================================

        sql = """
            SELECT
                musicbrainz_id,
                artist_name,
                release_name,
                label,
                release_date,
                country,
                format,
                jacket_url,
                cd_owned,
                vinyl_owned,
                memo
            FROM collections
        """

        # 条件がある場合はWHERE句を追加する
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        # 登録日時の新しい順で並べる
        sql += " ORDER BY created_at DESC, id DESC"

        # ========================================
        # SQLを実行する
        # ========================================

        cursor = self.conn.cursor()

        cursor.execute(
            sql,
            parameters
        )

        # 検索結果を取得する
        results = cursor.fetchall()

        collections = []

        # ========================================
        # DBのデータをPython用に変換する
        # ========================================

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
                result[7],  # jacket_url
                result[8],  # cd_owned
                result[9],  # vinyl_owned
                result[10]  # memo
            ))

        return collections