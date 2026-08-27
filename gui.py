import tkinter as tk
import requests
from tkinter import ttk, messagebox

from musicbrainz_api import MusicBrainzAPI


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

        # タイトルラベル
        title_label = ttk.Label(
            self.root,
            text="CD・レコード検索・コレクション管理",
            font=("Meiryo", 18)
        )

        title_label.pack(pady=20)

        # 検索対象のラベル
        target_label = ttk.Label(
            self.root,
            text="検索対象"
        )

        target_label.pack()

        # 検索対象の選択
        self.search_target = ttk.Combobox(
            self.root,
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
            self.root,
            width=50
        )

        self.search_entry.pack(pady=10)

        # 検索ボタン
        search_button = ttk.Button(
            self.root,
            text="検索",
            command=self.search
        )

        search_button.pack()

        # 検索結果のラベル
        result_label = ttk.Label(
            self.root,
            text="検索結果"
        )

        result_label.pack(pady=20)

        # 検索結果を表示するリスト
        self.result_listbox = tk.Listbox(
            self.root,
            width=70,
            height=20
        )

        self.result_listbox.bind(
            "<<ListboxSelect>>",
            self.on_result_selected
        )

        self.result_listbox.pack()

        # 作品情報
        self.detail_label = tk.Label(
            self.root,
            text="作品情報"
        )

        self.detail_label.pack()

        # ========================================
        # コレクション検索
        # ========================================

        # コレクション検索ラベル
        collection_search_label = ttk.Label(
            self.root,
            text="コレクション検索"
        )

        collection_search_label.pack(pady=5)

        # コレクション検索入力欄
        self.collection_search_entry = ttk.Entry(
            self.root,
            width=50
        )

        self.collection_search_entry.pack(pady=5)

        # コレクション所有フィルター
        self.collection_filter = ttk.Combobox(
            self.root,
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
            self.root,
            width=70,
            height=10
        )

        self.collection_listbox.pack()

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
                    self.result_listbox.insert(
                        tk.END,
                        release_group.get("title")
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

        # キーワードと所有状態を使ってコレクションを検索する
        collections = self.repository.filter_collections(
            keyword=keyword,
            cd_owned=cd_owned,
            vinyl_owned=vinyl_owned
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

        # 検索結果から選択されたアーティストを取得する
        artist = self.search_results[index]

        # MusicBrainz IDを取得する
        musicbrainz_id = artist.get("id")

        # 確認のためコンソールに表示する
        print(musicbrainz_id)
        print(artist.get("name"))

        try:
            release_groups = api.search_release_group(
                artist.get("name")
            )

        except requests.exceptions.RequestException:
            messagebox.showerror(
                "通信エラー",
                "MusicBrainzへの接続に失敗しました。"
            )
            return

        print(release_groups)
        print(release_groups.get("release-groups", []))

        release_group_list = release_groups.get(
            "release-groups",
            []
        )

        if release_group_list:
            release_group = release_group_list[0]

            print(release_group.get("title"))

            self.detail_label.config(
                text=f"作品名：{release_group.get('title')}"
            )

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

        # Repositoryからコレクション一覧を取得する
        collections = self.repository.get_collections()

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
            value=bool(collection[7])
        )

        self.vinyl_owned_var = tk.BooleanVar(
            value=bool(collection[8])
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
            collection[9] or ""
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

        # Repositoryへコレクションを登録する
        self.repository.add_collection(
            musicbrainz_id=data["musicbrainz_id"],
            artist_name=data["artist_name"],
            release_name=data["release_name"],
            label=data["label"],
            release_date=data["release_date"],
            country=data["country"],
            formats=data["formats"],
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
        cd_owned = collection[7]
        vinyl_owned = collection[8]
        memo = collection[9]

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


def main():
    """
    アプリケーションを起動する。
    """

    # Tkinterのルートウィンドウを作成する
    root = tk.Tk()

    # メイン画面を作成する
    MainWindow(root)

    # Tkinterのイベントループを開始する
    root.mainloop()


if __name__ == "__main__":
    main()