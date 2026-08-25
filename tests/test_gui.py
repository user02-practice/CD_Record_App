import tkinter as tk
import pytest

from collection_repository import CollectionRepository
from gui import MainWindow


@pytest.fixture(scope="module")
def root():
    """
    GUIテスト全体で共有するTkinterのルートウィンドウ。
    """
    root = tk.Tk()
    root.withdraw()

    yield root

    root.destroy()
def test_collection_list_can_be_displayed(root):
    """
    Repositoryに登録したコレクションが
    GUIの一覧に表示されることを確認する。
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

    # ========================================
    # 実行：MainWindowを作成
    # ========================================

    window = MainWindow(
        root,
        repository
    )

    window.show_collections()

    # ========================================
    # 確認：GUIにコレクションが表示されている
    # ========================================

    items = window.collection_listbox.get(0, tk.END)

    assert len(items) == 1
    assert "Queen" in items[0]
    assert "A Night at the Opera" in items[0]


def test_collection_list_can_be_filtered_by_keyword(root):
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
    # 実行：MainWindowを作成
    # ========================================

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


def test_collection_list_can_be_filtered_by_cd_owned(root):
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
    # 実行：MainWindowを作成
    # ========================================

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


def test_collection_list_can_be_filtered_by_vinyl_owned(root):
    """
    GUIでVinyl所有を指定すると、
    Vinylを所有しているコレクションだけが表示されることを確認する。
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
    # 実行：MainWindowを作成
    # ========================================

    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # 実行：Vinyl所有で絞り込む
    # ========================================

    window.filter_collection_list(
        vinyl_owned=True
    )

    # ========================================
    # 確認：Vinyl所有の作品だけ表示される
    # ========================================

    items = window.collection_listbox.get(0, tk.END)

    assert len(items) == 1
    assert "The Beatles" in items[0]
    assert "Abbey Road" in items[0]


def test_collection_filter_can_select_vinyl_owned(root):
    """
    GUIでコレクションのフィルターとして
    「Vinyl所有」を選択できることを確認する。
    """

    # ========================================
    # 準備：Repositoryを作成
    # ========================================

    repository = CollectionRepository(":memory:")

    # ========================================
    # 実行：MainWindowを作成
    # ========================================

    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # 実行：「Vinyl所有」を選択する
    # ========================================

    window.collection_filter.set("Vinyl所有")

    # ========================================
    # 確認：「Vinyl所有」が選択されている
    # ========================================

    assert window.collection_filter.get() == "Vinyl所有"


def test_collection_list_can_be_filtered_by_keyword_and_cd_owned(root):
    """
    GUIでキーワードとCD所有を指定すると、
    両方の条件に一致するコレクションだけが表示されることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成
    # ========================================

    repository = CollectionRepository(":memory:")

    # Queen + CD所有
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

    # Queen + CD未所有
    repository.add_collection(
        musicbrainz_id="test-002",
        artist_name="Queen",
        release_name="News of the World",
        label="EMI",
        release_date="1977-10-28",
        country="GB",
        formats=["CD"],
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    # The Beatles + CD所有
    repository.add_collection(
        musicbrainz_id="test-003",
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
    # 実行：MainWindowを作成
    # ========================================

    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # 実行：
    # Queen かつ CD所有で絞り込む
    # ========================================

    window.filter_collection_list(
        keyword="Queen",
        cd_owned=True
    )

    # ========================================
    # 確認：
    # QueenかつCD所有の作品だけ表示される
    # ========================================

    items = window.collection_listbox.get(0, tk.END)

    assert len(items) == 1
    assert "Queen" in items[0]
    assert "A Night at the Opera" in items[0]


def test_collection_filter_controls_exist(root):
    """
    コレクション画面に検索欄と所有フィルターが
    用意されていることを確認する。
    """

    # ========================================
    # 準備：Repositoryを作成
    # ========================================

    repository = CollectionRepository(":memory:")

    # ========================================
    # 実行：MainWindowを作成
    # ========================================

    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # 確認：検索欄が存在する
    # ========================================

    assert hasattr(window, "collection_search_entry")

    # ========================================
    # 確認：所有フィルターが存在する
    # ========================================

    assert hasattr(window, "collection_filter")


def test_collection_filter_selection_updates_list(root):
    """
    GUIで「CD所有」を選択すると、
    CDを所有しているコレクションだけが表示されることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成
    # ========================================

    repository = CollectionRepository(":memory:")

    # CD所有
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

    # CD未所有
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
    # 実行：MainWindowを作成
    # ========================================

    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # 実行：「CD所有」を選択する
    # ========================================

    window.collection_filter.set("CD所有")

    window.on_collection_filter_changed()

    # ========================================
    # 確認：CD所有の作品だけ表示される
    # ========================================

    items = window.collection_listbox.get(0, tk.END)

    assert len(items) == 1
    assert "Queen" in items[0]
    assert "A Night at the Opera" in items[0]


def test_collection_filter_selection_updates_list_for_both_owned(root):
    """
    GUIで「CD・Vinyl両方所有」を選択すると、
    CDとVinylの両方を所有しているコレクションだけが表示されることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成
    # ========================================

    repository = CollectionRepository(":memory:")

    # CD・Vinyl両方所有
    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD", "Vinyl"],
        cd_owned=1,
        vinyl_owned=1,
        memo=""
    )

    # CDのみ所有
    repository.add_collection(
        musicbrainz_id="test-002",
        artist_name="The Beatles",
        release_name="Abbey Road",
        label="Apple Records",
        release_date="1969-09-26",
        country="GB",
        formats=["CD"],
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    # Vinylのみ所有
    repository.add_collection(
        musicbrainz_id="test-003",
        artist_name="Pink Floyd",
        release_name="The Dark Side of the Moon",
        label="Harvest",
        release_date="1973-03-01",
        country="GB",
        formats=["Vinyl"],
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    # ========================================
    # 実行：MainWindowを作成
    # ========================================

    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # 実行：「CD・Vinyl両方所有」を選択する
    # ========================================

    window.collection_filter.set("CD・Vinyl両方所有")

    window.on_collection_filter_changed()

    # ========================================
    # 確認：両方所有の作品だけ表示される
    # ========================================

    items = window.collection_listbox.get(0, tk.END)

    assert len(items) == 1
    assert "Queen" in items[0]
    assert "A Night at the Opera" in items[0]

def test_collection_filter_selection_updates_list_for_none_owned():
    """
    GUIで「どちらも未所有」を選択すると、
    CDとVinylのどちらも所有していないコレクションだけが表示されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD"],
        cd_owned=0,
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
        formats=["CD"],
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    repository.add_collection(
        musicbrainz_id="test-003",
        artist_name="Pink Floyd",
        release_name="The Dark Side of the Moon",
        label="Harvest",
        release_date="1973-03-01",
        country="GB",
        formats=["Vinyl"],
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    root = tk.Tk()

    window = MainWindow(
        root,
        repository
    )

    window.collection_filter.set("どちらも未所有")

    window.on_collection_filter_changed()

    items = window.collection_listbox.get(0, tk.END)

    assert len(items) == 1
    assert "Queen" in items[0]
    assert "A Night at the Opera" in items[0]

    root.destroy()