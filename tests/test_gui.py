import tkinter as tk

from collection_repository import CollectionRepository
from gui import MainWindow


def test_collection_list_can_be_displayed():
    """
    Repositoryに登録したコレクションが
    GUIの一覧に表示されることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成
    # ========================================

    repository = CollectionRepository(":memory:")

    # テスト用コレクションを登録
    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD"],
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    # ========================================
    # 準備：Tkinterの画面を作成
    # ========================================

    root = tk.Tk()

    # ========================================
    # 実行：MainWindowを作成
    # ========================================

    window = MainWindow(
        root,
        repository
    )

    # コレクション一覧を表示する
    window.show_collections()

    # ========================================
    # 確認：GUIにコレクションが表示されている
    # ========================================

    items = window.collection_listbox.get(0, tk.END)

    assert len(items) == 1
    assert "Queen" in items[0]
    assert "A Night at the Opera" in items[0]

    # ========================================
    # 後片付け
    # ========================================

    root.destroy()

def test_collection_list_can_be_filtered_by_keyword():
    """
    GUIでキーワード検索すると、
    一致するコレクションだけが表示されることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成
    # ========================================

    repository = CollectionRepository(":memory:")

    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD"],
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    repository.add_collection(
        musicbrainz_id="test-002",
        artist_name="The Beatles",
        release_name="Abbey Road",
        label="Apple Records",
        release_date="1969-09-26",
        country="GB",
        formats=["CD", "Vinyl"],
        cd_owned=1,
        vinyl_owned=1,
        memo=""
    )

    # ========================================
    # 準備：Tkinterの画面を作成
    # ========================================

    root = tk.Tk()

    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # 実行：Queenで検索
    # ========================================

    window.filter_collection_list("Queen")

    # ========================================
    # 確認：Queenだけ表示されている
    # ========================================

    items = window.collection_listbox.get(0, tk.END)

    assert len(items) == 1
    assert "Queen" in items[0]
    assert "A Night at the Opera" in items[0]

    # ========================================
    # 後片付け
    # ========================================

    root.destroy()

def test_collection_list_can_be_filtered_by_cd_owned():
    """
    GUIでCD所有を指定すると、
    CDを所有しているコレクションだけが表示されることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成
    # ========================================

    repository = CollectionRepository(":memory:")

    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD"],
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    repository.add_collection(
        musicbrainz_id="test-002",
        artist_name="The Beatles",
        release_name="Abbey Road",
        label="Apple Records",
        release_date="1969-09-26",
        country="GB",
        formats=["CD", "Vinyl"],
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    # ========================================
    # 準備：Tkinterの画面を作成
    # ========================================

    root = tk.Tk()

    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # 実行：CD所有で絞り込む
    # ========================================

    window.filter_collection_list(
        cd_owned=True
    )

    # ========================================
    # 確認：CD所有の作品だけ表示される
    # ========================================

    items = window.collection_listbox.get(0, tk.END)

    assert len(items) == 1
    assert "Queen" in items[0]
    assert "A Night at the Opera" in items[0]

    # ========================================
    # 後片付け
    # ========================================

    root.destroy()