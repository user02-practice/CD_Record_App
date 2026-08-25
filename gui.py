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

        else:
            self.filter_collection_list()


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