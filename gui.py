import tkinter as tk
import requests
from io import BytesIO
from tkinter import ttk, messagebox

from PIL import Image, ImageTk
from musicbrainz_api import MusicBrainzAPI
from collection_repository import CollectionRepository


class MainWindow:
    """
    アプリケーションのメイン画面を管理するクラス。
    """

    def __init__(self, root, repository=None):
        """
        メイン画面を初期化する。

        Args:
            root (tk.Tk):
                Tkinterのルートウィンドウ。
        """

        # メインウィンドウを保存する
        self.root = root

        # コレクションRepositoryを保存する
        self.repository = repository

        self.search_results = []

        # ウィンドウのタイトルを設定する
        self.root.title("CD・レコード検索・コレクション管理")

        # ウィンドウのサイズを設定する
        self.root.geometry("800x600")

        # 画面を作成する
        self._create_widgets()

    def _create_widgets(self):
        """
        メイン画面の部品を作成する。
        """

        # 画面全体をスクロールするためのCanvas
        canvas = tk.Canvas(self.root)
        canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        # 縦スクロールバー
        scrollbar = ttk.Scrollbar(
            self.root,
            orient=tk.VERTICAL,
            command=canvas.yview
        )
        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        # Canvasの中に実際の部品を置くフレーム
        main_frame = ttk.Frame(canvas)

        main_window = canvas.create_window(
            (0, 0),
            window=main_frame,
            anchor="nw"
        )

        # Canvasの幅に合わせてmain_frameの幅を広げる
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                main_window,
                width=event.width
            )
        )

        # 中身の大きさに合わせてスクロール範囲を更新する
        main_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # マウスホイールで画面全体をスクロールする
        def _on_mousewheel(event):
            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        canvas.bind_all(
            "<MouseWheel>",
            _on_mousewheel
        )
        # タイトルラベル
        title_label = ttk.Label(
            main_frame,
            text="CD・レコード検索・コレクション管理",
            font=("Meiryo", 18)
        )

        title_label.pack(pady=10)

        # 検索対象のラベル
        target_label = ttk.Label(
            main_frame,
            text="検索対象"
        )

        target_label.pack()

        # 検索対象の選択
        self.search_target = ttk.Combobox(
            main_frame,
            values=[
                "アーティスト",
                "アルバム",
                "トラック",
                "キーワード"
            ],
            state="readonly"
        )

        # 初期値を設定する
        self.search_target.current(0)

        # 検索対象を配置する
        self.search_target.pack(pady=5)

        # 検索入力欄
        self.search_entry = ttk.Entry(
            main_frame,
            width=50
        )

        self.search_entry.pack(pady=10)

        # 検索ボタン
        search_button = ttk.Button(
            main_frame,
            text="検索",
            command=self.search
        )

        search_button.pack()

        # 検索結果のラベル
        result_label = ttk.Label(
            main_frame,
            text="検索結果"
        )

        result_label.pack(pady=10)

        # 検索結果を表示するフレーム
        result_frame = tk.Frame(main_frame)
        result_frame.pack()

        # 検索結果を表示するリスト
        self.result_listbox = tk.Listbox(
            result_frame,
            width=70,
            height=8
        )

        # 縦スクロールバー
        result_scrollbar = tk.Scrollbar(
            result_frame,
            orient=tk.VERTICAL,
            command=self.result_listbox.yview
        )

        self.result_listbox.config(
            yscrollcommand=result_scrollbar.set
        )

        self.result_listbox.bind(
            "<<ListboxSelect>>",
            self.on_result_selected
        )

        self.result_listbox.pack(
            side=tk.LEFT
        )

        result_scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        # ジャケット画像
        self.jacket_image_label = tk.Label(
            main_frame,
            text="ジャケット画像"
        )

        self.jacket_image_label.pack()

        # 作品情報
        self.detail_label = tk.Label(
            main_frame,
            text="作品情報"
        )

        self.detail_label.pack()

        # コレクション登録ボタン
        self.collection_register_button = tk.Button(
            main_frame,
            text="コレクションに登録",
            command=self.register_selected_collection
        )

        self.collection_register_button.pack()

        # ========================================
        # コレクション検索
        # ========================================

        # コレクション検索ラベル
        collection_search_label = ttk.Label(
            main_frame,
            text="コレクション検索"
        )

        collection_search_label.pack(pady=5)

        # ========================================
        # コレクション検索対象
        # ========================================

        # コレクション検索の対象を選択する
        self.collection_search_target = ttk.Combobox(
            main_frame,
            values=[
                "アーティスト",
                "アルバム",
                "キーワード"
            ],
            state="readonly"
        )

        # 初期状態はキーワード検索
        self.collection_search_target.current(2)

        # 検索対象の選択欄を配置する
        self.collection_search_target.pack(pady=5)

        # コレクション検索入力欄
        self.collection_search_entry = ttk.Entry(
            main_frame,
            width=50
        )

        self.collection_search_entry.pack(pady=5)

        # ========================================
        # コレクション並び替え
        # ========================================

        self.collection_sort = ttk.Combobox(
            main_frame,
            values=[
                "登録日時の新しい順",
                "アーティスト名順",
                "アルバム名順"
            ],
            state="readonly"
        )

        # 初期状態は登録日時の新しい順
        self.collection_sort.current(0)

        # 並び替え選択欄を配置する
        self.collection_sort.pack(pady=5)

        # 並び替え方法が変更されたときの処理
        self.collection_sort.bind(
            "<<ComboboxSelected>>",
            self.on_collection_sort_changed
        )

        # コレクション所有フィルター
        self.collection_filter = ttk.Combobox(
            main_frame,
            values=[
                "すべて",
                "CD所有",
                "Vinyl所有",
                "CD・Vinyl両方所有",
                "どちらも未所有"
            ],
            state="readonly"
        )

        # 初期値は「すべて」
        self.collection_filter.current(0)

        # フィルターを配置する
        self.collection_filter.pack(pady=5)

        # フィルターが変更されたときの処理
        self.collection_filter.bind(
            "<<ComboboxSelected>>",
            self.on_collection_filter_changed
        )

        # コレクション一覧を表示するリスト
        self.collection_listbox = tk.Listbox(
            main_frame,
            width=70,
            height=10
        )

        self.collection_listbox.pack()

    def on_collection_sort_changed(self, event=None):
        """
        コレクションの並び替え方法が変更されたときの処理。
        """

        sort_value = self.collection_sort.get()

        # 現在の所有フィルターを取得する
        filter_value = self.collection_filter.get()

        cd_owned = None
        vinyl_owned = None

        if filter_value == "CD所有":
            cd_owned = True

        elif filter_value == "Vinyl所有":
            vinyl_owned = True

        elif filter_value == "CD・Vinyl両方所有":
            cd_owned = True
            vinyl_owned = True

        elif filter_value == "どちらも未所有":
            cd_owned = False
            vinyl_owned = False

        # 並び替え方法を決める
        if sort_value == "アーティスト名順":
            sort_by = "artist_name"

        elif sort_value == "アルバム名順":
            sort_by = "release_name"

        else:
            sort_by = None

        # 現在の検索条件を取得する
        keyword = self.collection_search_entry.get()
        search_target = self.collection_search_target.get()

        # 検索・所有フィルター・並び替えをまとめて適用する
        collections = self.repository.filter_collections(
            keyword=keyword,
            cd_owned=cd_owned,
            vinyl_owned=vinyl_owned,
            search_target=search_target,
            sort_by=sort_by
        )


        # 一覧をいったん空にする
        self.collection_listbox.delete(0, tk.END)

        # 並び替えたコレクションを表示する
        for collection in collections:
            artist_name = collection[1]
            release_name = collection[2]

            self.collection_listbox.insert(
                tk.END,
                f"{artist_name} - {release_name}"
            )

    def search(self):
        """
        検索ボタンが押されたときの処理。
        """

        # 検索対象を取得する
        search_target = self.search_target.get()

        # 検索文字を取得する
        keyword = self.search_entry.get()

        # 検索文字が空の場合
        if not keyword:
            return

        # MusicBrainz APIを使用する
        api = MusicBrainzAPI()

        try:
            # アーティスト検索
            if search_target == "アーティスト":
                result = api.search_artist(keyword)

                # 検索結果を取得する
                artists = result.get("artists", [])
                self.search_results = artists

                # 以前の検索結果を削除する
                self.result_listbox.delete(0, tk.END)

                # 検索結果を画面に表示する
                for artist in artists:
                    self.result_listbox.insert(
                        tk.END,
                        artist.get("name")
                    )
            # アルバム検索
            elif search_target == "アルバム":
                result = api.search_release_group(keyword)

                # 検索結果を取得する
                release_groups = result.get("release-groups", [])
                self.search_results = release_groups

                # 以前の検索結果を削除する
                self.result_listbox.delete(0, tk.END)

                # 検索結果を画面に表示する
                for release_group in release_groups:
                    artist_credit = release_group.get("artist-credit", [])

                    if artist_credit:
                        artist_name = artist_credit[0].get("name", "")
                    else:
                        artist_name = ""

                    release_name = release_group.get("title", "")

                    self.result_listbox.insert(
                        tk.END,
                        f"{artist_name} - {release_name}"
                    )

            # トラック検索
            elif search_target == "トラック":
                result = api.search_track(keyword)

                # 検索結果を取得する
                recordings = result.get("recordings", [])
                self.search_results = recordings

                # 以前の検索結果を削除する
                self.result_listbox.delete(0, tk.END)

                # 検索結果を画面に表示する
                for recording in recordings:
                    self.result_listbox.insert(
                        tk.END,
                        recording.get("title")
                    )

            # キーワード検索
            elif search_target == "キーワード":
                result = api.search_keyword(keyword)

                # 検索結果を取得する
                artists = result.get("artists", [])
                release_groups = result.get("release-groups", [])
                recordings = result.get("recordings", [])

                self.search_results = (
                    artists
                    + release_groups
                    + recordings
                )

                # 以前の検索結果を削除する
                self.result_listbox.delete(0, tk.END)

                # Artistの検索結果を表示する
                for artist in artists:
                    self.result_listbox.insert(
                        tk.END,
                        artist.get("name")
                    )

                # Albumの検索結果を表示する
                for release_group in release_groups:
                    artist_credit = release_group.get("artist-credit", [])

                    if artist_credit:
                        artist_name = artist_credit[0].get("name", "")
                    else:
                        artist_name = ""

                    release_name = release_group.get("title", "")

                    self.result_listbox.insert(
                        tk.END,
                        f"{artist_name} - {release_name}"
                    )

                # Trackの検索結果を表示する
                for recording in recordings:
                    self.result_listbox.insert(
                        tk.END,
                        recording.get("title")
                    )

        except requests.exceptions.RequestException:
            print("MusicBrainzへの接続に失敗しました。")

    def show_collections(self):
        """
        Repositoryからコレクションを取得し、
        GUIの一覧に表示する。
        """

        # コレクション一覧を取得する
        collections = self.repository.get_collections()

        # 以前の表示を削除する
        self.collection_listbox.delete(0, tk.END)

        # コレクションを1件ずつ表示する
        for collection in collections:

            # コレクション情報を取得する
            artist_name = collection[1]
            release_name = collection[2]

            # アーティスト名と作品名を表示する
            self.collection_listbox.insert(
                tk.END,
                f"{artist_name} - {release_name}"
            )

    def filter_collection_list(
            self,
            keyword="",
            cd_owned=None,
            vinyl_owned=None
    ):
        """
        キーワードと所有状態でコレクションを絞り込み、
        GUIの一覧に表示する。
        """

        # コレクション検索の対象を取得する
        search_target = self.collection_search_target.get()

        # 検索対象・キーワード・所有状態を使って
        # コレクションを絞り込む
        collections = self.repository.filter_collections(
            keyword=keyword,
            cd_owned=cd_owned,
            vinyl_owned=vinyl_owned,
            search_target=search_target
        )

        # 以前の表示を削除する
        self.collection_listbox.delete(0, tk.END)

        # 検索結果を1件ずつ表示する
        for collection in collections:
            # コレクション情報を取得する
            artist_name = collection[1]
            release_name = collection[2]

            # アーティスト名と作品名を表示する
            self.collection_listbox.insert(
                tk.END,
                f"{artist_name} - {release_name}"
            )

    def on_result_selected(self, event):
        """
        検索結果が選択されたときの処理。
        """

        api = MusicBrainzAPI()

        # 選択された項目の番号を取得する
        selection = self.result_listbox.curselection()

        # 何も選択されていない場合
        if not selection:
            return

        # 選択された番号を取得する
        index = selection[0]

        # 選択された検索結果を取得する
        result = self.search_results[index]

        # MusicBrainz IDを取得する
        musicbrainz_id = result.get("id")

        # アルバム検索以外の結果は
        # Release Groupの詳細取得を行わない
        if self.search_target.get() != "アルバム":
            return

        try:
            release_group = api.get_release_group(
                musicbrainz_id
            )

            releases_result = api.get_releases(
                musicbrainz_id
            )

        except requests.exceptions.RequestException:
            messagebox.showerror(
                "通信エラー",
                "MusicBrainzへの接続に失敗しました。"
            )
            return

        # Release一覧を取得する
        releases = releases_result.get("releases", [])

        # アーティスト名を取得する
        artist_credit = release_group.get("artist-credit", [])

        if artist_credit:
            artist_name = artist_credit[0].get("name", "")
        else:
            artist_name = ""

        # リリース日を取得する
        release_date = release_group.get("first-release-date", "")

        # ジャケット画像URLを取得する
        self.jacket_url = ""

        if releases:
            release_id = releases[0].get("id")

            self.jacket_url = api.get_cover_art_url(
                release_id
            )
            
        # ジャケット画像を表示する
        self.load_jacket_image(self.jacket_url)

        # フォーマットを取得する
        formats = []

        for release in releases:
            for media in release.get("media", []):
                format_name = media.get("format")

                if format_name and format_name not in formats:
                    formats.append(format_name)

        format_text = ", ".join(formats)

        # レーベルを取得する
        labels = []

        for release in releases:
            for label_info in release.get("label-info", []):
                label = label_info.get("label")

                if label:
                    label_name = label.get("name")

                    if label_name and label_name not in labels:
                        labels.append(label_name)

        label_text = ", ".join(labels)

        # 国を取得する
        countries = []

        for release in releases:
            country = release.get("country")

            if country and country not in countries:
                countries.append(country)

        country_text = ", ".join(countries)

        # 詳細欄に作品名、アーティスト名、リリース日、フォーマット、レーベル、国を表示する
        self.detail_label.config(
            text=(
                f"アーティスト：{artist_name}\n"
                f"作品名：{release_group.get('title')}\n"
                f"リリース日：{release_date}\n"
                f"フォーマット：{format_text}\n"
                f"レーベル：{label_text}\n"
                f"国：{country_text}"
            )
        )

    def register_selected_collection(self):
        """
        選択した作品をコレクションに登録する。
        """

        # 選択された検索結果を取得する
        selection = self.result_listbox.curselection()

        if not selection:
            return

        # 選択された検索結果を取得する
        index = selection[0]
        result = self.search_results[index]

        # MusicBrainz IDを取得する
        musicbrainz_id = result.get("id")

        # すでにコレクションに登録されているか確認する
        if self.repository.get_collection(musicbrainz_id) is not None:
            return

        # 詳細情報を取得する
        api = MusicBrainzAPI()

        try:
            release_group = api.get_release_group(
                musicbrainz_id
            )
        except requests.exceptions.RequestException:
            messagebox.showerror(
                "通信エラー",
                "MusicBrainzへの接続に失敗しました。\n"
                "しばらくしてからもう一度お試しください。"
            )
            return

        # アーティスト名を取得する
        artist_credit = release_group.get("artist-credit", [])

        if artist_credit:
            artist_name = artist_credit[0].get("name", "")
        else:
            artist_name = ""

        # 作品名を取得する
        release_name = release_group.get("title", "")

        # リリース日を取得する
        release_date = release_group.get(
            "first-release-date",
            ""
        )

        # ジャケット画像URLを取得する
        jacket_url = release_group.get(
            "jacket_url",
            ""
        )

        # フォーマットを取得する
        formats = []

        for release in release_group.get("releases", []):
            for media in release.get("media", []):
                format_name = media.get("format")

                if format_name and format_name not in formats:
                    formats.append(format_name)

        # レーベルを取得する
        labels = []

        for release in release_group.get("releases", []):
            for label_info in release.get("label-info", []):
                label = label_info.get("label")

                if label:
                    label_name = label.get("name")

                    if label_name and label_name not in labels:
                        labels.append(label_name)

        # 国を取得する
        countries = []

        for release in release_group.get("releases", []):
            country = release.get("country")

            if country and country not in countries:
                countries.append(country)

        # 登録画面へ渡す作品情報を保存する
        self.register_collection_data = {
            "musicbrainz_id": musicbrainz_id,
            "artist_name": artist_name,
            "release_name": release_name,
            "label": ", ".join(labels),
            "release_date": release_date,
            "country": ", ".join(countries),
            "formats": formats,
            "jacket_url": jacket_url
        }

        # コレクション登録画面を表示する
        self.show_collection_register()


    def on_collection_filter_changed(self, event=None):
        """
        コレクションの所有フィルターが変更されたときの処理。
        """

        filter_value = self.collection_filter.get()

        if filter_value == "CD所有":
            self.filter_collection_list(
                cd_owned=True
            )

        elif filter_value == "Vinyl所有":
            self.filter_collection_list(
                vinyl_owned=True
            )


        elif filter_value == "CD・Vinyl両方所有":

            self.filter_collection_list(

                cd_owned=True,

                vinyl_owned=True

            )


        elif filter_value == "どちらも未所有":

            self.filter_collection_list(

                cd_owned=False,

                vinyl_owned=False

            )


        else:

            self.filter_collection_list()

    def get_selected_search_result(self):
        """
        検索結果一覧で選択されている検索結果を取得する。

        Returns:
            dict or None:
                選択されている検索結果。
                選択されていない場合はNone。
        """

        # 検索結果一覧で選択されている項目を取得する
        selection = self.result_listbox.curselection()

        # 何も選択されていない場合
        if not selection:
            return None

        # 選択された一覧の番号を取得する
        index = selection[0]

        # 検索結果から選択された項目を返す
        return self.search_results[index]

    def get_selected_collection(self):
        """
        コレクション一覧で選択されている作品を取得する。

        Returns:
            tuple or None:
                選択されているコレクション。
                選択されていない場合はNone。
        """

        # コレクション一覧で選択されている項目を取得する
        selection = self.collection_listbox.curselection()

        # 何も選択されていない場合
        if not selection:
            return None

        # 選択された一覧の番号を取得する
        index = selection[0]

        # 現在の検索条件を取得する
        keyword = self.collection_search_entry.get()
        search_target = self.collection_search_target.get()

        # 現在の所有フィルターを取得する
        filter_value = self.collection_filter.get()

        cd_owned = None
        vinyl_owned = None

        if filter_value == "CD所有":
            cd_owned = True

        elif filter_value == "Vinyl所有":
            vinyl_owned = True

        elif filter_value == "CD・Vinyl両方所有":
            cd_owned = True
            vinyl_owned = True

        elif filter_value == "どちらも未所有":
            cd_owned = False
            vinyl_owned = False

        # 現在の並び替え方法を取得する
        sort_value = self.collection_sort.get()

        if sort_value == "アーティスト名順":
            sort_by = "artist_name"

        elif sort_value == "アルバム名順":
            sort_by = "release_name"

        else:
            sort_by = None

        # 画面に表示されている条件と同じ一覧を取得する
        collections = self.repository.filter_collections(
            keyword=keyword,
            cd_owned=cd_owned,
            vinyl_owned=vinyl_owned,
            search_target=search_target,
            sort_by=sort_by
        )

        # 選択されたコレクションを返す
        return collections[index]

    def show_collection_edit(self):
        """
        選択されているコレクションの編集画面を表示する。
        """

        # 選択されているコレクションを取得する
        collection = self.get_selected_collection()

        # コレクションが選択されていない場合
        if collection is None:
            return

        # ========================================
        # 編集用の値を作成する
        # ========================================

        self.cd_owned_var = tk.BooleanVar(
            value=bool(collection[8])
        )

        self.vinyl_owned_var = tk.BooleanVar(
            value=bool(collection[9])
        )

        # ========================================
        # CD所有チェックボックス
        # ========================================

        self.cd_owned_checkbutton = ttk.Checkbutton(
            self.root,
            text="CD所有",
            variable=self.cd_owned_var
        )

        self.cd_owned_checkbutton.pack()

        # ========================================
        # Vinyl所有チェックボックス
        # ========================================

        self.vinyl_owned_checkbutton = ttk.Checkbutton(
            self.root,
            text="Vinyl所有",
            variable=self.vinyl_owned_var
        )

        self.vinyl_owned_checkbutton.pack()

        # ========================================
        # メモ入力欄
        # ========================================

        self.memo_entry = ttk.Entry(
            self.root,
            width=50
        )

        self.memo_entry.pack()

        # 既存のメモを設定する
        self.memo_entry.insert(
            0,
            collection[10] or ""
        )

        # ========================================
        # 更新ボタン
        # ========================================

        self.update_button = ttk.Button(
            self.root,
            text="更新",
            command=self.update_collection
        )

        self.update_button.pack()

    def show_collection_register(self):
        """
        コレクションの登録画面を表示する。
        """

        # ========================================
        # 登録用の値を作成する
        # ========================================

        # 初期状態ではCDを所有していない
        self.cd_owned_var = tk.BooleanVar(
            value=False
        )

        # 初期状態ではVinylを所有していない
        self.vinyl_owned_var = tk.BooleanVar(
            value=False
        )

        # ========================================
        # CD所有チェックボックス
        # ========================================

        self.cd_owned_checkbutton = ttk.Checkbutton(
            self.root,
            text="CD所有",
            variable=self.cd_owned_var
        )

        self.cd_owned_checkbutton.pack()

        # ========================================
        # Vinyl所有チェックボックス
        # ========================================

        self.vinyl_owned_checkbutton = ttk.Checkbutton(
            self.root,
            text="Vinyl所有",
            variable=self.vinyl_owned_var
        )

        self.vinyl_owned_checkbutton.pack()

        # ========================================
        # メモ入力欄
        # ========================================

        self.memo_entry = ttk.Entry(
            self.root,
            width=50
        )

        self.memo_entry.pack()

        # ========================================
        # 登録ボタン
        # ========================================

        self.register_button = ttk.Button(
            self.root,
            text="登録",
            command=self.register_collection
        )

        self.register_button.pack()

    def register_collection(self):
        """
        登録画面で入力された内容を使って
        コレクションをDBへ登録する。
        """

        # 登録する作品情報を取得する
        data = self.register_collection_data

        # 登録画面で入力された所有状態を取得する
        cd_owned = int(self.cd_owned_var.get())
        vinyl_owned = int(self.vinyl_owned_var.get())

        # 登録画面で入力されたメモを取得する
        memo = self.memo_entry.get()

        # すでに登録されている作品か確認する
        if self.repository.get_collection(
                data["musicbrainz_id"]
        ) is not None:
            messagebox.showinfo(
                "登録済み",
                "この作品はすでにコレクションに登録されています。"
            )
            return

        # Repositoryへコレクションを登録する
        self.repository.add_collection(
            musicbrainz_id=data["musicbrainz_id"],
            artist_name=data["artist_name"],
            release_name=data["release_name"],
            label=data["label"],
            release_date=data["release_date"],
            country=data["country"],
            formats=data["formats"],
            jacket_url=data.get("jacket_url", ""),
            cd_owned=cd_owned,
            vinyl_owned=vinyl_owned,
            memo=memo
        )

    def show_selected_collection_detail(self):
        """
        選択されているコレクションの詳細を表示する。
        """

        # 選択されているコレクションを取得する
        collection = self.get_selected_collection()

        # コレクションが選択されていない場合
        if collection is None:
            return

        # コレクション情報を取得する
        artist_name = collection[1]
        release_name = collection[2]

        # ジャケット画像URLを取得する
        jacket_url = collection[7]

        # 保存されているジャケット画像URLを使って画像を表示する
        self.load_jacket_image(jacket_url)

        # コレクションの所有状態とメモを取得する
        cd_owned = collection[8]
        vinyl_owned = collection[9]
        memo = collection[10]

        # 所有状態を表示用の文字列に変換する
        cd_owned_text = "あり" if cd_owned else "なし"
        vinyl_owned_text = "あり" if vinyl_owned else "なし"

        # 詳細欄に作品情報を表示する
        self.detail_label.config(
            text=f"アーティスト：{artist_name}\n"
                 f"作品名：{release_name}\n"
                 f"CD所有：{cd_owned_text}\n"
                 f"Vinyl所有：{vinyl_owned_text}\n"
                 f"メモ：{memo or ''}"
        )

        # コレクション削除ボタン
        self.collection_delete_button = ttk.Button(
            self.root,
            text="コレクションから削除",
            command=self.delete_collection
        )

        self.collection_delete_button.pack()

    def delete_collection(self):
        """
        選択されているコレクションを削除する。
        """

        # 選択されているコレクションを取得する
        collection = self.get_selected_collection()

        # コレクションが選択されていない場合
        if collection is None:
            return

        # 削除確認ダイアログを表示する
        result = messagebox.askyesno(
            "削除確認",
            f"「{collection[2]}」を削除しますか？"
        )

        # キャンセルされた場合は削除しない
        if not result:
            return

        # Repositoryを使って削除する
        self.repository.delete_collection(
            musicbrainz_id=collection[0]
        )

        # コレクション一覧を更新する
        self.show_collections()


    def update_collection(self):
        """
        編集画面で入力された内容を使って
        コレクションを更新する。
        """

        # ========================================
        # 選択されているコレクションを取得する
        # ========================================

        collection = self.get_selected_collection()

        # コレクションが選択されていない場合
        if collection is None:
            return

        # ========================================
        # 編集画面から値を取得する
        # ========================================

        cd_owned = self.cd_owned_var.get()
        vinyl_owned = self.vinyl_owned_var.get()
        memo = self.memo_entry.get()

        # ========================================
        # Repositoryを使って更新する
        # ========================================

        self.repository.update_collection(
            musicbrainz_id=collection[0],
            cd_owned=cd_owned,
            vinyl_owned=vinyl_owned,
            memo=memo
        )

        # 詳細表示を更新する
        self.show_selected_collection_detail()

    def load_jacket_image(self, jacket_url):
        """
        ジャケット画像を取得して表示する。
        """

        # ジャケット画像URLがない場合
        if not jacket_url:
            self.jacket_image = None
            self.jacket_image_label.config(
                image="",
                text="画像なし"
            )
            return

        try:
            # ジャケット画像を取得する
            response = requests.get(
                jacket_url,
                timeout=10
            )

            # HTTPエラーがある場合は例外を発生させる
            response.raise_for_status()

            # 取得した画像データを開く
            image = Image.open(
                BytesIO(response.content)
            )

            # 表示サイズを調整する
            image.thumbnail((300, 300))

            # Tkinterで表示できる画像に変換する
            self.jacket_image = ImageTk.PhotoImage(image)

            # ジャケット画像を表示する
            self.jacket_image_label.config(
                image=self.jacket_image,
                text=""
            )

        except (requests.exceptions.RequestException, OSError):
            # 通信エラーや画像データの読み込みに失敗した場合は
            # 「画像なし」と表示する
            self.jacket_image = None
            self.jacket_image_label.config(
                image="",
                text="画像なし"
            )


def main():
    """
    アプリケーションを起動する。
    """

    # Tkinterのルートウィンドウを作成する
    root = tk.Tk()

    # コレクションRepositoryを作成する
    repository = CollectionRepository("collection.db")

    # メイン画面を作成する
    MainWindow(
        root,
        repository=repository
    )

    # Tkinterのイベントループを開始する
    root.mainloop()


if __name__ == "__main__":
    main()