import tkinter as tk
import pytest
import requests

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
        "test-001",
        "Queen",
        "A Night at the Opera",
        "EMI",
        "1975-11-21",
        "GB",
        ["CD"],
        None,  # jacket_url
        1,
        0,
        ""
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
        jacket_url=None,
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
        jacket_url=None,
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
        jacket_url=None,
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
        jacket_url=None,
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
        jacket_url=None,
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
        jacket_url=None,
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
        jacket_url=None,
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
        jacket_url=None,
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
        jacket_url=None,
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
        jacket_url=None,
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
        jacket_url=None,
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
        jacket_url=None,
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
        jacket_url=None,
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
        jacket_url=None,
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


def test_collection_filter_selection_updates_list_for_none_owned(root):
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
        jacket_url=None,
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
        jacket_url=None,
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
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

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


def test_collection_can_be_selected_from_list():
    """
    GUIのコレクション一覧から作品を選択すると、
    選択したコレクションの情報を取得できることを確認する。
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
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo="名盤"
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
    # コレクション一覧を表示する
    # ========================================

    window.show_collections()

    # ========================================
    # 実行：一覧の1件目を選択する
    # ========================================

    window.collection_listbox.selection_set(0)

    collection = window.get_selected_collection()

    # ========================================
    # 確認：選択した作品が取得できる
    # ========================================

    assert collection is not None
    assert collection[0] == "test-001"
    assert collection[1] == "Queen"
    assert collection[2] == "A Night at the Opera"
    assert collection[3] == "EMI"
    assert collection[4] == "1975-11-21"
    assert collection[5] == "GB"
    assert collection[6] == ["CD"]
    assert collection[7] is None  # jacket_url
    assert collection[8] == 1  # cd_owned
    assert collection[9] == 0  # vinyl_owned
    assert collection[10] == "名盤"  # memo

    # ========================================
    # 後片付け
    # ========================================

    root.destroy()


def test_selected_collection_name_is_displayed_in_detail():
    """
    コレクション一覧から作品を選択すると、
    選択した作品名が詳細欄に表示されることを確認する。
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
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo="名盤"
    )

    root = tk.Tk()

    window = MainWindow(
        root,
        repository
    )

    window.show_collections()

    window.collection_listbox.selection_set(0)

    window.show_selected_collection_detail()

    detail_text = window.detail_label.cget("text")

    assert "A Night at the Opera" in detail_text

    root.destroy()


def test_collection_edit_controls_exist():
    """
    コレクションの編集画面を開くと、
    CD所有、Vinyl所有、メモの編集部品が存在することを確認する。
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
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo="名盤"
    )

    root = tk.Tk()

    window = MainWindow(
        root,
        repository
    )

    window.show_collections()

    window.collection_listbox.selection_set(0)

    window.show_collection_edit()

    assert hasattr(window, "cd_owned_var")
    assert hasattr(window, "vinyl_owned_var")
    assert hasattr(window, "memo_entry")

    root.destroy()


def test_collection_edit_controls_show_current_values():
    """
    コレクションの編集画面を開くと、
    現在のCD所有、Vinyl所有、メモが
    編集部品に正しく設定されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo="名盤"
    )

    root = tk.Tk()

    window = MainWindow(
        root,
        repository
    )

    window.show_collections()

    window.collection_listbox.selection_set(0)

    window.show_collection_edit()

    assert window.cd_owned_var.get() is True
    assert window.vinyl_owned_var.get() is False
    assert window.memo_entry.get() == "名盤"

    root.destroy()


def test_collection_can_be_updated_from_edit_screen():
    """
    編集画面でCD所有、Vinyl所有、メモを変更して更新すると、
    コレクションが正しく更新されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo="名盤"
    )

    root = tk.Tk()

    window = MainWindow(
        root,
        repository
    )

    window.show_collections()

    window.collection_listbox.selection_set(0)

    window.show_collection_edit()

    window.cd_owned_var.set(False)
    window.vinyl_owned_var.set(True)

    window.memo_entry.delete(0, tk.END)
    window.memo_entry.insert(0, "買い直したい")

    window.update_collection()

    collection = repository.get_collection("test-001")

    assert collection[7] is None  # jacket_url
    assert collection[8] == 0  # cd_owned
    assert collection[9] == 1  # vinyl_owned
    assert collection[10] == "買い直したい"  # memo

    root.destroy()


def test_collection_edit_screen_has_update_button():
    """
    コレクション編集画面に更新ボタンが存在することを確認する。
    """

    repository = CollectionRepository(":memory:")

    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo="名盤"
    )

    root = tk.Tk()

    window = MainWindow(
        root,
        repository
    )

    window.show_collections()

    window.collection_listbox.selection_set(0)

    window.show_collection_edit()

    assert hasattr(window, "update_button")

    root.destroy()


def test_updated_collection_is_reflected_in_detail():
    """
    コレクションを更新したあと、
    詳細表示に更新後の所有状態とメモが反映されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo="名盤"
    )

    root = tk.Tk()

    window = MainWindow(
        root,
        repository
    )

    window.show_collections()

    window.collection_listbox.selection_set(0)

    window.show_collection_edit()

    window.cd_owned_var.set(False)
    window.vinyl_owned_var.set(True)

    window.memo_entry.delete(0, tk.END)
    window.memo_entry.insert(0, "買い直したい")

    window.update_collection()

    window.show_selected_collection_detail()

    detail_text = window.detail_label.cget("text")

    assert "アーティスト：Queen" in detail_text
    assert "作品名：A Night at the Opera" in detail_text
    assert "CD所有：なし" in detail_text
    assert "Vinyl所有：あり" in detail_text
    assert "メモ：買い直したい" in detail_text

    root.destroy()


def test_update_collection_refreshes_detail():
    """
    コレクションを更新すると、
    詳細表示も自動的に更新されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo="名盤"
    )

    root = tk.Tk()

    window = MainWindow(
        root,
        repository
    )

    window.show_collections()

    window.collection_listbox.selection_set(0)

    window.show_collection_edit()

    window.cd_owned_var.set(False)
    window.vinyl_owned_var.set(True)

    window.memo_entry.delete(0, tk.END)
    window.memo_entry.insert(0, "買い直したい")

    window.update_collection()

    detail_text = window.detail_label.cget("text")

    assert "アーティスト：Queen" in detail_text
    assert "作品名：A Night at the Opera" in detail_text
    assert "CD所有：なし" in detail_text
    assert "Vinyl所有：あり" in detail_text
    assert "メモ：買い直したい" in detail_text

    root.destroy()


def test_collection_register_controls_exist():
    """
    コレクションの登録画面を開くと、
    CD所有、Vinyl所有、メモの入力部品が存在することを確認する。
    """

    repository = CollectionRepository(":memory:")

    root = tk.Tk()

    window = MainWindow(
        root,
        repository
    )

    window.show_collection_register()

    assert hasattr(window, "cd_owned_var")
    assert hasattr(window, "vinyl_owned_var")
    assert hasattr(window, "memo_entry")

    root.destroy()


def test_collection_can_be_registered_from_register_screen():
    """
    登録画面で入力した所有状態とメモを使って、
    コレクションをDBへ登録できることを確認する。
    """

    repository = CollectionRepository(":memory:")

    root = tk.Tk()

    window = MainWindow(
        root,
        repository
    )

    window.register_collection_data = {
        "musicbrainz_id": "test-001",
        "artist_name": "Queen",
        "release_name": "A Night at the Opera",
        "label": "EMI",
        "release_date": "1975-11-21",
        "country": "GB",
        "formats": ["CD", "Vinyl"]
    }

    window.show_collection_register()

    window.cd_owned_var.set(True)
    window.vinyl_owned_var.set(False)

    window.memo_entry.insert(
        0,
        "名盤"
    )

    window.register_collection()

    collection = repository.get_collection("test-001")

    assert collection is not None
    assert collection[0] == "test-001"
    assert collection[1] == "Queen"
    assert collection[2] == "A Night at the Opera"
    assert collection[7] == ""  # jacket_url
    assert collection[8] == 1  # cd_owned
    assert collection[9] == 0  # vinyl_owned
    assert collection[10] == "名盤"  # memo

    root.destroy()


def test_registered_collection_is_reflected_in_list(root):
    """
    コレクションを登録すると、
    登録した作品が一覧に表示されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    window = MainWindow(
        root,
        repository
    )

    window.register_collection_data = {
        "musicbrainz_id": "test-001",
        "artist_name": "Queen",
        "release_name": "A Night at the Opera",
        "label": "EMI",
        "release_date": "1975-11-21",
        "country": "GB",
        "formats": ["CD", "Vinyl"]
    }

    window.show_collection_register()

    window.cd_owned_var.set(True)
    window.vinyl_owned_var.set(False)

    window.memo_entry.insert(
        0,
        "名盤"
    )

    window.register_collection()

    window.show_collections()

    items = window.collection_listbox.get(0, tk.END)

    assert len(items) == 1
    assert "Queen" in items[0]
    assert "A Night at the Opera" in items[0]


def test_collection_register_screen_has_register_button():
    """
    コレクション登録画面に登録ボタンが存在することを確認する。
    """

    repository = CollectionRepository(":memory:")

    root = tk.Tk()

    window = MainWindow(
        root,
        repository
    )

    window.register_collection_data = {
        "musicbrainz_id": "test-001",
        "artist_name": "Queen",
        "release_name": "A Night at the Opera",
        "label": "EMI",
        "release_date": "1975-11-21",
        "country": "GB",
        "formats": ["CD", "Vinyl"]
    }

    window.show_collection_register()

    assert hasattr(window, "register_button")

    root.destroy()


def test_album_search_results_can_be_displayed(root, monkeypatch):
    """
    アルバム検索を実行すると、
    検索結果がGUIの一覧に表示されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("アルバム")

    window.search_entry.insert(
        0,
        "A Night at the Opera"
    )

    window.search()

    items = window.result_listbox.get(0, tk.END)

    assert len(items) == 1
    assert "A Night at the Opera" in items[0]


def test_track_search_results_can_be_displayed(root, monkeypatch):
    """
    トラック検索を実行すると、
    検索結果がGUIの一覧に表示されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_track(self, track_name):
            return {
                "recordings": [
                    {
                        "id": "recording-001",
                        "title": "Bohemian Rhapsody"
                    }
                ]
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("トラック")

    window.search_entry.insert(
        0,
        "Bohemian Rhapsody"
    )

    window.search()

    items = window.result_listbox.get(0, tk.END)

    assert len(items) == 1
    assert "Bohemian Rhapsody" in items[0]


def test_keyword_search_results_can_be_displayed(root, monkeypatch):
    """
    キーワード検索を実行すると、
    Artist、Album、Trackの検索結果がGUIの一覧に表示されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_keyword(self, keyword):
            return {
                "artists": [
                    {
                        "id": "artist-001",
                        "name": "Queen"
                    }
                ],
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ],
                "recordings": [
                    {
                        "id": "recording-001",
                        "title": "Bohemian Rhapsody"
                    }
                ]
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("キーワード")

    window.search_entry.insert(
        0,
        "Queen"
    )

    window.search()

    items = window.result_listbox.get(0, tk.END)

    assert len(items) == 3
    assert "Queen" in items[0]
    assert "A Night at the Opera" in items[1]
    assert "Bohemian Rhapsody" in items[2]


def test_selected_album_search_result_can_be_retrieved(root, monkeypatch):
    """
    アルバム検索結果から作品を選択すると、
    選択した検索結果を取得できることを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("アルバム")

    window.search_entry.insert(
        0,
        "A Night at the Opera"
    )

    window.search()

    window.result_listbox.selection_set(0)

    result = window.get_selected_search_result()

    assert result is not None
    assert result["id"] == "release-group-001"
    assert result["title"] == "A Night at the Opera"


def test_selected_album_search_result_is_displayed_in_detail(root, monkeypatch):
    """
    アルバム検索結果から作品を選択すると、
    選択した作品の詳細情報が表示されることを確認する。
    """

    # ========================================
    # 準備：Repositoryを作成
    # ========================================

    repository = CollectionRepository(":memory:")

    # ========================================
    # MusicBrainz APIの検索結果を用意する
    # ========================================

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

        def get_release_group(self, musicbrainz_id):
            assert musicbrainz_id == "release-group-001"

            return {
                "id": "release-group-001",
                "title": "A Night at the Opera",
                "artist-credit": [
                    {
                        "name": "Queen"
                    }
                ]
            }

        def get_releases(self, musicbrainz_id):
            return {
                "releases": []
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    # ========================================
    # MainWindowを作成
    # ========================================

    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # アルバム検索を設定
    # ========================================

    window.search_target.set("アルバム")

    window.search_entry.insert(
        0,
        "A Night at the Opera"
    )

    # ========================================
    # 検索を実行
    # ========================================

    window.search()

    # ========================================
    # 1件目を選択する
    # ========================================

    window.result_listbox.selection_set(0)

    # ========================================
    # 選択された検索結果を詳細表示する
    # ========================================

    window.on_result_selected(None)

    # ========================================
    # 確認：作品名とアーティスト名が表示される
    # ========================================

    detail_text = window.detail_label.cget("text")

    assert "A Night at the Opera" in detail_text
    assert "Queen" in detail_text




def test_selected_album_search_result_displays_release_date(root, monkeypatch):
    """
    アルバム検索結果から作品を選択すると、
    詳細欄にリリース日が表示されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

        def get_releases(self, musicbrainz_id):
            return {
                "releases": []
            }

        def get_release_group(self, musicbrainz_id):
            assert musicbrainz_id == "release-group-001"

            return {
                "id": "release-group-001",
                "title": "A Night at the Opera",
                "first-release-date": "1975-11-21",
                "artist-credit": [
                    {
                        "name": "Queen"
                    }
                ]
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("アルバム")

    window.search_entry.insert(
        0,
        "A Night at the Opera"
    )

    window.search()

    window.result_listbox.selection_set(0)
    window.on_result_selected(None)

    detail_text = window.detail_label.cget("text")

    assert "1975-11-21" in detail_text


def test_selected_album_search_result_displays_format(root, monkeypatch):
    """
    アルバム検索結果から作品を選択すると、
    詳細欄にフォーマットが表示されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

        def get_release_group(self, musicbrainz_id):
            assert musicbrainz_id == "release-group-001"

            return {
                "id": "release-group-001",
                "title": "A Night at the Opera",
                "first-release-date": "1975-11-21",
                "artist-credit": [
                    {
                        "name": "Queen"
                    }
                ]
            }

        def get_releases(self, musicbrainz_id):
            return {
                "releases": [
                    {
                        "title": "A Night at the Opera",
                        "media": [
                            {
                                "format": "CD"
                            },
                            {
                                "format": "Vinyl"
                            }
                        ]
                    }
                ]
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("アルバム")

    window.search_entry.insert(
        0,
        "A Night at the Opera"
    )

    window.search()

    window.result_listbox.selection_set(0)
    window.on_result_selected(None)

    detail_text = window.detail_label.cget("text")

    assert "CD" in detail_text
    assert "Vinyl" in detail_text


def test_selected_album_search_result_displays_label(root, monkeypatch):
    """
    アルバム検索結果から作品を選択すると、
    詳細欄にレーベルが表示されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

        def get_releases(self, musicbrainz_id):
            return {
                "releases": [
                    {
                        "title": "A Night at the Opera",
                        "media": [
                            {
                                "format": "CD"
                            },
                            {
                                "format": "Vinyl"
                            }
                        ],
                        "label-info": [
                            {
                                "label": {
                                    "name": "EMI"
                                }
                            }
                        ]
                    }
                ]
            }

        def get_release_group(self, musicbrainz_id):
            assert musicbrainz_id == "release-group-001"

            return {
                "id": "release-group-001",
                "title": "A Night at the Opera",
                "first-release-date": "1975-11-21",
                "artist-credit": [
                    {
                        "name": "Queen"
                    }
                ],
                "releases": [
                    {
                        "title": "A Night at the Opera",
                        "media": [
                            {
                                "format": "CD"
                            },
                            {
                                "format": "Vinyl"
                            }
                        ],
                        "label-info": [
                            {
                                "label": {
                                    "name": "EMI"
                                }
                            }
                        ]
                    }
                ]
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("アルバム")

    window.search_entry.insert(
        0,
        "A Night at the Opera"
    )

    window.search()

    window.result_listbox.selection_set(0)
    window.on_result_selected(None)

    detail_text = window.detail_label.cget("text")

    assert "EMI" in detail_text


def test_selected_album_search_result_displays_country(root, monkeypatch):
    """
    アルバム検索結果から作品を選択すると、
    詳細欄に国が表示されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

        def get_releases(self, musicbrainz_id):
            return {
                "releases": [
                    {
                        "title": "A Night at the Opera",
                        "country": "GB",
                        "media": [
                            {
                                "format": "CD"
                            },
                            {
                                "format": "Vinyl"
                            }
                        ],
                        "label-info": [
                            {
                                "label": {
                                    "name": "EMI"
                                }
                            }
                        ]
                    }
                ]
            }

        def get_release_group(self, musicbrainz_id):
            assert musicbrainz_id == "release-group-001"

            return {
                "id": "release-group-001",
                "title": "A Night at the Opera",
                "first-release-date": "1975-11-21",
                "artist-credit": [
                    {
                        "name": "Queen"
                    }
                ],
                "releases": [
                    {
                        "title": "A Night at the Opera",
                        "country": "GB",
                        "media": [
                            {
                                "format": "CD"
                            },
                            {
                                "format": "Vinyl"
                            }
                        ],
                        "label-info": [
                            {
                                "label": {
                                    "name": "EMI"
                                }
                            }
                        ]
                    }
                ]
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("アルバム")

    window.search_entry.insert(
        0,
        "A Night at the Opera"
    )

    window.search()

    window.result_listbox.selection_set(0)
    window.on_result_selected(None)

    detail_text = window.detail_label.cget("text")

    assert "GB" in detail_text


def test_selected_album_search_result_displays_jacket_url(root, monkeypatch):
    """
    アルバム検索結果から作品を選択すると、
    詳細欄にジャケット画像URLが表示されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

        def get_releases(self, musicbrainz_id):
            return {
                "releases": []
            }

        def get_release_group(self, musicbrainz_id):
            return {
                "id": "release-group-001",
                "title": "A Night at the Opera",
                "first-release-date": "1975-11-21",
                "artist-credit": [
                    {
                        "name": "Queen"
                    }
                ],
                "releases": [
                    {
                        "country": "GB",
                        "media": [
                            {
                                "format": "CD"
                            }
                        ],
                        "label-info": [
                            {
                                "label": {
                                    "name": "EMI"
                                }
                            }
                        ]
                    }
                ],
                "jacket_url": "https://example.com/jacket.jpg"
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("アルバム")
    window.search_entry.insert(0, "A Night at the Opera")

    window.search()

    window.result_listbox.selection_set(0)

    monkeypatch.setattr(
        window,
        "load_jacket_image",
        lambda jacket_url: None
    )

    window.on_result_selected(None)

    assert window.jacket_url == "https://example.com/jacket.jpg"


def test_selected_album_search_result_displays_jacket_image(root, monkeypatch):
    """
    アルバム検索結果から作品を選択すると、
    ジャケット画像表示用のウィジェットが存在することを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

        def get_release_group(self, musicbrainz_id):
            return {
                "id": "release-group-001",
                "title": "A Night at the Opera",
                "first-release-date": "1975-11-21",
                "artist-credit": [
                    {
                        "name": "Queen"
                    }
                ],
                "jacket_url": "https://example.com/jacket.jpg"
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    assert hasattr(window, "jacket_image_label")


def test_selected_album_search_result_has_collection_register_button(
        root,
        monkeypatch
):
    """
    アルバム検索結果を選択すると、
    コレクション登録ボタンが詳細画面に存在することを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

        def get_releases(self, musicbrainz_id):
            return {
                "releases": []
            }

        def get_release_group(self, musicbrainz_id):
            return {
                "id": "release-group-001",
                "title": "A Night at the Opera",
                "artist-credit": [
                    {
                        "name": "Queen"
                    }
                ],
                "jacket_url": ""
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("アルバム")
    window.search_entry.insert(
        0,
        "A Night at the Opera"
    )

    window.search()

    window.result_listbox.selection_set(0)
    window.on_result_selected(None)

    assert hasattr(
        window,
        "collection_register_button"
    )


def test_collection_register_button_calls_register_method(
        root,
        monkeypatch
):
    """
    コレクション登録ボタンを押すと、
    コレクション登録処理が呼ばれることを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

        def get_release_group(self, musicbrainz_id):
            return {
                "id": "release-group-001",
                "title": "A Night at the Opera",
                "artist-credit": [
                    {
                        "name": "Queen"
                    }
                ],
                "jacket_url": ""
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("アルバム")
    window.search_entry.insert(
        0,
        "A Night at the Opera"
    )


def test_collection_register_button_has_register_command(
        root,
        monkeypatch
):
    """
    コレクション登録ボタンに、
    コレクション登録処理が設定されていることを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

        def get_release_group(self, musicbrainz_id):
            return {
                "id": "release-group-001",
                "title": "A Night at the Opera",
                "artist-credit": [
                    {
                        "name": "Queen"
                    }
                ],
                "jacket_url": ""
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    command = window.collection_register_button.cget("command")

    assert command

def test_collection_register_button_registers_selected_album(
    root,
    monkeypatch
):
    """
    コレクション登録ボタンを押すと、
    選択したアルバムがRepositoryに登録されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

        def get_releases(self, musicbrainz_id):
            return {
                "releases": []
            }

        def get_release_group(self, musicbrainz_id):
            return {
                "id": "release-group-001",
                "title": "A Night at the Opera",
                "artist-credit": [
                    {
                        "name": "Queen"
                    }
                ],
                "first-release-date": "1975-11-21",
                "jacket_url": ""
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("アルバム")
    window.search_entry.insert(
        0,
        "A Night at the Opera"
    )

    window.search()

    window.result_listbox.selection_set(0)
    window.on_result_selected(None)

    window.collection_register_button.invoke()

    window.register_button.invoke()

    collection = repository.get_collection(
        "release-group-001"
    )

    assert collection is not None
    assert collection[1] == "Queen"
    assert collection[2] == "A Night at the Opera"

def test_collection_register_button_does_not_duplicate_collection(
        root,
        monkeypatch
):
    """
    同じ作品をコレクションに2回登録しても、
    二重登録されないことを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

        def get_releases(self, musicbrainz_id):
            return {
                "releases": []
            }

        def get_release_group(self, musicbrainz_id):
            return {
                "id": "release-group-001",
                "title": "A Night at the Opera",
                "artist-credit": [
                    {
                        "name": "Queen"
                    }
                ],
                "releases": [
                    {
                        "country": "GB",
                        "media": [
                            {
                                "format": "CD"
                            }
                        ],
                        "label-info": [
                            {
                                "label": {
                                    "name": "EMI"
                                }
                            }
                        ]
                    }
                ],
                "jacket_url": ""
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("アルバム")
    window.search_entry.insert(
        0,
        "A Night at the Opera"
    )

    window.search()

    window.result_listbox.selection_set(0)
    window.on_result_selected(None)

    window.collection_register_button.invoke()
    window.register_button.invoke()

    window.collection_register_button.invoke()
    window.register_button.invoke()

    collections = repository.get_collections()

    assert len(collections) == 1

def test_collection_register_button_opens_register_screen(
        root,
        monkeypatch
):
    """
    詳細画面のコレクション登録ボタンを押すと、
    コレクション登録画面が表示されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera"
                    }
                ]
            }

        def get_releases(self, musicbrainz_id):
            return {
                "releases": []
            }

        def get_release_group(self, musicbrainz_id):
            return {
                "id": "release-group-001",
                "title": "A Night at the Opera",
                "artist-credit": [
                    {
                        "name": "Queen"
                    }
                ],
                "releases": [],
                "jacket_url": ""
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("アルバム")
    window.search_entry.insert(
        0,
        "A Night at the Opera"
    )

    window.search()

    window.result_listbox.selection_set(0)
    window.on_result_selected(None)

    window.collection_register_button.invoke()

    assert hasattr(
        window,
        "register_collection_data"
    )

def test_collection_detail_has_delete_button(root):
    """
    コレクション詳細画面に削除ボタンが存在することを確認する
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
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    window = MainWindow(root, repository)

    window.show_collections()

    window.collection_listbox.selection_set(0)
    window.show_selected_collection_detail()

    assert hasattr(window, "collection_delete_button")

def test_collection_delete_button_calls_delete_method(root, monkeypatch):
    """
    コレクション削除ボタンを押すと、
    Repositoryのdelete_collection()が呼ばれることを確認する
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
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    window = MainWindow(root, repository)

    window.show_collections()
    window.collection_listbox.selection_set(0)
    window.show_selected_collection_detail()

    monkeypatch.setattr(
        "gui.messagebox.askyesno",
        lambda title, message: True
    )

    deleted_id = []

    def fake_delete_collection(musicbrainz_id):
        deleted_id.append(musicbrainz_id)

    monkeypatch.setattr(
        repository,
        "delete_collection",
        fake_delete_collection
    )

    window.collection_delete_button.invoke()

    assert deleted_id == ["test-001"]

def test_collection_delete_button_removes_collection(root,monkeypatch):
    """
    コレクション削除ボタンを押すと、
    コレクションがRepositoryから削除されることを確認する
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
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    window = MainWindow(root, repository)

    window.show_collections()
    window.collection_listbox.selection_set(0)
    window.show_selected_collection_detail()

    monkeypatch.setattr(
        "gui.messagebox.askyesno",
        lambda title, message: True
    )

    window.collection_delete_button.invoke()

    assert repository.get_collection("test-001") is None

def test_collection_delete_button_refreshes_list(root,monkeypatch):
    """
    コレクション削除後に、
    コレクション一覧が更新されることを確認する
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
        jacket_url=None,
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
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=1,
        memo=""
    )

    window = MainWindow(root, repository)

    window.show_collections()

    # Queenを選択する
    # コレクションは登録日時の新しい順に表示されるため、
    # 先に登録したQueenは1番目になる
    window.collection_listbox.selection_set(1)
    window.show_selected_collection_detail()

    monkeypatch.setattr(
        "gui.messagebox.askyesno",
        lambda title, message: True
    )

    # Queenを削除する
    window.collection_delete_button.invoke()

    # 一覧を再取得する
    items = window.collection_listbox.get(0, tk.END)

    assert len(items) == 1
    assert "Abbey Road" in items[0]

def test_collection_delete_button_asks_for_confirmation(
        root,
        monkeypatch
):
    """
    コレクション削除ボタンを押すと、
    削除確認ダイアログが表示されることを確認する。
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
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    window = MainWindow(root, repository)

    window.show_collections()
    window.collection_listbox.selection_set(0)
    window.show_selected_collection_detail()

    dialog_called = []

    def fake_askyesno(title, message):
        dialog_called.append((title, message))
        return False

    monkeypatch.setattr(
        "gui.messagebox.askyesno",
        fake_askyesno
    )

    window.collection_delete_button.invoke()

    assert len(dialog_called) == 1

def test_collection_delete_is_cancelled_when_confirmation_is_no(
        root,
        monkeypatch
):
    """
    削除確認ダイアログで「いいえ」を選択すると、
    コレクションが削除されないことを確認する。
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
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    window = MainWindow(root, repository)

    window.show_collections()
    window.collection_listbox.selection_set(0)
    window.show_selected_collection_detail()

    monkeypatch.setattr(
        "gui.messagebox.askyesno",
        lambda title, message: False
    )

    window.collection_delete_button.invoke()

    assert repository.get_collection("test-001") is not None

def test_collection_delete_is_executed_when_confirmation_is_yes(
        root,
        monkeypatch
):
    """
    削除確認ダイアログで「はい」を選択すると、
    コレクションが削除されることを確認する。
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
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    window = MainWindow(root, repository)

    window.show_collections()
    window.collection_listbox.selection_set(0)
    window.show_selected_collection_detail()

    monkeypatch.setattr(
        "gui.messagebox.askyesno",
        lambda title, message: True
    )

    window.collection_delete_button.invoke()

    assert repository.get_collection("test-001") is None
def test_selected_collection_detail_displays_jacket_image(root, monkeypatch):
    """
    コレクション詳細画面を表示したとき、
    保存されているジャケット画像URLが
    ジャケット画像表示処理へ渡されることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成する
    # ========================================

    repository = CollectionRepository(":memory:")

    # ジャケット画像URLを含むコレクションを登録する
    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD"],
        jacket_url="https://example.com/jacket.jpg",
        cd_owned=1,
        vinyl_owned=0,
        memo="名盤"
    )

    # メイン画面を作成する
    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # ジャケット画像の通信処理を置き換える
    # ========================================

    # 実際の画像取得は行わず、
    # load_jacket_image() に渡されたURLだけを記録する
    loaded_urls = []

    monkeypatch.setattr(
        window,
        "load_jacket_image",
        lambda jacket_url: loaded_urls.append(jacket_url)
    )

    # ========================================
    # 実行：コレクション詳細を表示する
    # ========================================

    window.show_collections()

    # 一覧の1件目を選択する
    window.collection_listbox.selection_set(0)

    # 選択したコレクションの詳細を表示する
    window.show_selected_collection_detail()

    # ========================================
    # 確認：保存されたジャケットURLが使用される
    # ========================================

    assert loaded_urls == [
        "https://example.com/jacket.jpg"
    ]

def test_load_jacket_image_shows_no_image_when_request_fails(root, monkeypatch):
    """
    ジャケット画像の取得に失敗した場合でも、
    アプリがエラーで終了せず「画像なし」と表示されることを確認する。
    """

    # ========================================
    # 準備：MainWindowを作成する
    # ========================================

    window = MainWindow(
        root,
        CollectionRepository(":memory:")
    )

    # ========================================
    # 通信エラーを発生させる
    # ========================================

    def raise_request_error(*args, **kwargs):
        raise requests.exceptions.RequestException()

    monkeypatch.setattr(
        "gui.requests.get",
        raise_request_error
    )

    # ========================================
    # 実行：ジャケット画像を読み込む
    # ========================================

    window.load_jacket_image(
        "https://example.com/jacket.jpg"
    )

    # ========================================
    # 確認：画像なし表示になる
    # ========================================

    assert window.jacket_image is None
    assert window.jacket_image_label.cget("text") == "画像なし"

def test_load_jacket_image_shows_no_image_when_image_data_is_invalid(root, monkeypatch):
    """
    ジャケット画像の通信には成功しても、
    取得したデータが画像として読み込めない場合は
    「画像なし」と表示されることを確認する。
    """

    # ========================================
    # 準備：MainWindowを作成する
    # ========================================

    window = MainWindow(
        root,
        CollectionRepository(":memory:")
    )

    # ========================================
    # 壊れた画像データを返すレスポンスを用意する
    # ========================================

    class FakeResponse:
        content = b"not-image-data"

        def raise_for_status(self):
            pass

    monkeypatch.setattr(
        "gui.requests.get",
        lambda *args, **kwargs: FakeResponse()
    )

    # ========================================
    # 実行：ジャケット画像を読み込む
    # ========================================

    window.load_jacket_image(
        "https://example.com/jacket.jpg"
    )

    # ========================================
    # 確認：画像なし表示になる
    # ========================================

    assert window.jacket_image is None
    assert window.jacket_image_label.cget("text") == "画像なし"

def test_collection_list_can_be_sorted_by_artist_name(root):
    """
    コレクション画面で「アーティスト名順」を選択したとき、
    アーティスト名の昇順で一覧表示されることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成する
    # ========================================

    repository = CollectionRepository(":memory:")

    # Queenを登録する
    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    # The Beatlesを登録する
    repository.add_collection(
        musicbrainz_id="test-002",
        artist_name="The Beatles",
        release_name="Abbey Road",
        label="Apple Records",
        release_date="1969-09-26",
        country="GB",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=1,
        memo=""
    )

    # ABBAを登録する
    repository.add_collection(
        musicbrainz_id="test-003",
        artist_name="ABBA",
        release_name="Arrival",
        label="Polar",
        release_date="1976-10-11",
        country="SE",
        formats=["Vinyl"],
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    # メイン画面を作成する
    window = MainWindow(
        root,
        repository
    )

    # コレクション一覧を表示する
    window.show_collections()

    # ========================================
    # 実行：アーティスト名順を選択する
    # ========================================

    window.collection_sort.set(
        "アーティスト名順"
    )

    window.on_collection_sort_changed()

    # ========================================
    # 確認：アーティスト名の昇順で表示される
    # ========================================

    items = window.collection_listbox.get(
        0,
        tk.END
    )

    assert len(items) == 3

    assert "ABBA" in items[0]
    assert "Queen" in items[1]
    assert "The Beatles" in items[2]

def test_collection_list_can_be_sorted_by_album_name(root):
    """
    コレクション画面で「アルバム名順」を選択したとき、
    アルバム名の昇順で一覧表示されることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成する
    # ========================================

    repository = CollectionRepository(":memory:")

    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="News of the World",
        label="EMI",
        release_date="1977-10-28",
        country="GB",
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    repository.add_collection(
        musicbrainz_id="test-002",
        artist_name="The Beatles",
        release_name="Abbey Road",
        label="Apple",
        release_date="1969-09-26",
        country="GB",
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    repository.add_collection(
        musicbrainz_id="test-003",
        artist_name="ABBA",
        release_name="Arrival",
        label="Polar",
        release_date="1976-10-11",
        country="SE",
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    # ========================================
    # GUIを作成する
    # ========================================

    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # 実行：アルバム名順を選択する
    # ========================================

    window.collection_sort.set(
        "アルバム名順"
    )

    window.on_collection_sort_changed()

    # ========================================
    # 確認：アルバム名の昇順で表示される
    # ========================================

    items = window.collection_listbox.get(
        0,
        tk.END
    )

    assert len(items) == 3

    assert "Abbey Road" in items[0]
    assert "Arrival" in items[1]
    assert "News of the World" in items[2]


def test_collection_list_can_be_sorted_by_newest(root):
    """
    コレクション画面で「登録日時の新しい順」を選択したとき、
    新しく登録した作品から順に一覧表示されることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成する
    # ========================================

    repository = CollectionRepository(":memory:")

    # Queenを先に登録する
    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    # The Beatlesを後から登録する
    repository.add_collection(
        musicbrainz_id="test-002",
        artist_name="The Beatles",
        release_name="Abbey Road",
        label="Apple Records",
        release_date="1969-09-26",
        country="GB",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=1,
        memo=""
    )

    # メイン画面を作成する
    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # 実行：登録日時の新しい順を選択する
    # ========================================

    window.collection_sort.set(
        "登録日時の新しい順"
    )

    window.on_collection_sort_changed()

    # ========================================
    # 確認：後から登録した作品が先に表示される
    # ========================================

    items = window.collection_listbox.get(
        0,
        tk.END
    )

    assert len(items) == 2

    assert "The Beatles" in items[0]
    assert "Queen" in items[1]

def test_collection_list_can_be_searched_by_memo(root):
    """
    コレクション検索欄にメモのキーワードを入力すると、
    メモに一致する作品が一覧表示されることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成する
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
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo="お気に入りのアルバム"
    )

    repository.add_collection(
        musicbrainz_id="test-002",
        artist_name="The Beatles",
        release_name="Abbey Road",
        label="Apple Records",
        release_date="1969-09-26",
        country="GB",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=1,
        memo="中古で購入"
    )

    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # 実行：メモのキーワードで検索する
    # ========================================

    window.collection_search_entry.insert(
        0,
        "お気に入り"
    )

    window.filter_collection_list(
        keyword=window.collection_search_entry.get()
    )

    # ========================================
    # 確認：メモが一致する作品だけ表示される
    # ========================================

    items = window.collection_listbox.get(
        0,
        tk.END
    )

    assert len(items) == 1
    assert "Queen" in items[0]
    assert "A Night at the Opera" in items[0]

def test_collection_search_target_artist_searches_artist_only(root):
    """
    コレクション検索対象を「アーティスト」にした場合、
    アーティスト名だけを対象に検索できることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成する
    # ========================================

    repository = CollectionRepository(":memory:")

    # アーティスト名にQueenを含む作品
    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    # アルバム名にはQueenを含むが、
    # アーティスト名には含まない作品
    repository.add_collection(
        musicbrainz_id="test-002",
        artist_name="Various Artists",
        release_name="Queen Tribute",
        label=None,
        release_date=None,
        country=None,
        formats=["CD"],
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=0,
        memo=""
    )

    # メイン画面を作成する
    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # 実行：検索対象をアーティストにする
    # ========================================

    window.collection_search_target.set(
        "アーティスト"
    )

    window.filter_collection_list(
        keyword="Queen"
    )

    # ========================================
    # 確認：アーティスト名が一致する作品だけ表示される
    # ========================================

    items = window.collection_listbox.get(
        0,
        tk.END
    )

    assert len(items) == 1
    assert "Queen - A Night at the Opera" in items[0]

def test_collection_search_target_album_searches_album_only(root):
    """
    コレクション検索対象を「アルバム」にした場合、
    アルバム名だけを対象に検索できることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成する
    # ========================================

    repository = CollectionRepository(":memory:")

    # アルバム名にQueenを含む作品
    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Various Artists",
        release_name="Queen Tribute",
        label=None,
        release_date=None,
        country=None,
        formats=["CD"],
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=0,
        memo=""
    )

    # アーティスト名にはQueenを含むが、
    # アルバム名には含まない作品
    repository.add_collection(
        musicbrainz_id="test-002",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    # メイン画面を作成する
    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # 実行：検索対象をアルバムにする
    # ========================================

    window.collection_search_target.set(
        "アルバム"
    )

    window.filter_collection_list(
        keyword="Queen"
    )

    # ========================================
    # 確認：アルバム名が一致する作品だけ表示される
    # ========================================

    items = window.collection_listbox.get(
        0,
        tk.END
    )

    assert len(items) == 1
    assert "Various Artists - Queen Tribute" in items[0]

def test_collection_search_target_artist_can_be_combined_with_cd_filter(root):
    """
    コレクション検索対象を「アーティスト」にした状態で、
    CD所有フィルターも同時に適用できることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成する
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
        jacket_url=None,
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
        formats=["Vinyl"],
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    # Queenではない + CD所有
    repository.add_collection(
        musicbrainz_id="test-003",
        artist_name="The Beatles",
        release_name="Abbey Road",
        label="Apple Records",
        release_date="1969-09-26",
        country="GB",
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    window = MainWindow(
        root,
        repository
    )

    # ========================================
    # 実行：Queen + CD所有で絞り込む
    # ========================================

    window.collection_search_target.set(
        "アーティスト"
    )

    window.filter_collection_list(
        keyword="Queen",
        cd_owned=True
    )

    # ========================================
    # 確認：QueenかつCD所有の作品だけ表示される
    # ========================================

    items = window.collection_listbox.get(
        0,
        tk.END
    )

    assert len(items) == 1
    assert "Queen - A Night at the Opera" in items[0]

def test_collection_search_target_album_can_be_combined_with_vinyl_filter(root):
    """
    コレクション検索対象を「アルバム」にした状態で、
    Vinyl所有フィルターも同時に適用できることを確認する。
    """

    repository = CollectionRepository(":memory:")

    # Abbey Road + Vinyl所有
    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="The Beatles",
        release_name="Abbey Road",
        label="Apple Records",
        release_date="1969-09-26",
        country="GB",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=1,
        memo=""
    )

    # Abbey Road + Vinyl未所有
    repository.add_collection(
        musicbrainz_id="test-002",
        artist_name="Various Artists",
        release_name="Abbey Road Tribute",
        label=None,
        release_date=None,
        country=None,
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    # Abbey Roadではない + Vinyl所有
    repository.add_collection(
        musicbrainz_id="test-003",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["Vinyl"],
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    window = MainWindow(
        root,
        repository
    )

    # 検索対象をアルバムにする
    window.collection_search_target.set(
        "アルバム"
    )

    # Abbey Road + Vinyl所有で絞り込む
    window.filter_collection_list(
        keyword="Abbey Road",
        vinyl_owned=True
    )

    items = window.collection_listbox.get(
        0,
        tk.END
    )

    assert len(items) == 1
    assert "The Beatles - Abbey Road" in items[0]

def test_collection_list_can_be_filtered_by_cd_owned_and_sorted_by_artist(root):
    """
    CD所有で絞り込んだ状態で、
    アーティスト名の昇順に並び替えられることを確認する。
    """

    repository = CollectionRepository(":memory:")

    # CD所有：Queen
    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    # CD所有：ABBA
    repository.add_collection(
        musicbrainz_id="test-002",
        artist_name="ABBA",
        release_name="Arrival",
        label="Polar",
        release_date="1976-10-11",
        country="SE",
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    # CD未所有：The Beatles
    repository.add_collection(
        musicbrainz_id="test-003",
        artist_name="The Beatles",
        release_name="Abbey Road",
        label="Apple Records",
        release_date="1969-09-26",
        country="GB",
        formats=["Vinyl"],
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    window = MainWindow(
        root,
        repository
    )

    # CD所有で絞り込む
    window.collection_filter.set("CD所有")
    window.on_collection_filter_changed()

    # アーティスト名順に並び替える
    window.collection_sort.set("アーティスト名順")
    window.on_collection_sort_changed()

    items = window.collection_listbox.get(
        0,
        tk.END
    )

    assert len(items) == 2
    assert "ABBA" in items[0]
    assert "Queen" in items[1]

def test_collection_list_can_be_searched_filtered_and_sorted(root):
    """
    アーティスト検索とCD所有フィルターを使った状態で、
    アーティスト名順に並び替えられることを確認する。
    """

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
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    # Queen + CD所有
    repository.add_collection(
        musicbrainz_id="test-002",
        artist_name="Queen II",
        release_name="Queen II",
        label="EMI",
        release_date="1974-03-08",
        country="GB",
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    # Queen + CD未所有
    repository.add_collection(
        musicbrainz_id="test-003",
        artist_name="Queen Live",
        release_name="Live Album",
        label="EMI",
        release_date="1980-01-01",
        country="GB",
        formats=["Vinyl"],
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    # Queenではない + CD所有
    repository.add_collection(
        musicbrainz_id="test-004",
        artist_name="ABBA",
        release_name="Arrival",
        label="Polar",
        release_date="1976-10-11",
        country="SE",
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    window = MainWindow(
        root,
        repository
    )

    window.collection_search_target.set("アーティスト")
    window.collection_search_entry.insert(0, "Queen")
    window.collection_filter.set("CD所有")

    window.filter_collection_list(
        keyword="Queen",
        cd_owned=True
    )

    window.collection_sort.set("アーティスト名順")
    window.on_collection_sort_changed()

    items = window.collection_listbox.get(
        0,
        tk.END
    )

    assert len(items) == 2
    assert "Queen - A Night at the Opera" in items[0]
    assert "Queen II - Queen II" in items[1]

def test_selected_collection_matches_sorted_list(root):
    """
    並び替え後に選択した作品と、
    実際に取得されるコレクションが一致することを確認する。
    """

    repository = CollectionRepository(":memory:")

    # 先にABBAを登録
    repository.add_collection(
        musicbrainz_id="test-001",
        artist_name="ABBA",
        release_name="Arrival",
        label="Polar",
        release_date="1976-10-11",
        country="SE",
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    # 後からQueenを登録
    repository.add_collection(
        musicbrainz_id="test-002",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD"],
        jacket_url=None,
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    window = MainWindow(
        root,
        repository
    )

    # アーティスト名順に並び替える
    window.collection_sort.set("アーティスト名順")
    window.on_collection_sort_changed()

    # 一覧の先頭（ABBA）を選択
    window.collection_listbox.selection_set(0)

    collection = window.get_selected_collection()

    assert collection[1] == "ABBA"
    assert collection[2] == "Arrival"

def test_artist_search_result_does_not_request_release_group(root, monkeypatch):
    """
    アーティスト検索結果を選択したときに、
    アーティストIDをRelease Groupとして取得しないことを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_artist(self, artist_name):
            return {
                "artists": [
                    {
                        "id": "artist-001",
                        "name": "Queen"
                    }
                ]
            }

        def get_release_group(self, musicbrainz_id):
            raise AssertionError(
                "アーティストIDでget_release_groupが呼ばれています"
            )

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("アーティスト")
    window.search_entry.insert(
        0,
        "Queen"
    )

    window.search()

    window.result_listbox.selection_set(0)

    window.on_result_selected(None)

def test_album_search_results_display_artist_and_album(root, monkeypatch):
    """
    アルバム検索結果に、
    アーティスト名と作品名の両方が表示されることを確認する。
    """

    repository = CollectionRepository(":memory:")

    class FakeMusicBrainzAPI:

        def search_release_group(self, album_name):
            return {
                "release-groups": [
                    {
                        "id": "release-group-001",
                        "title": "A Night at the Opera",
                        "artist-credit": [
                            {
                                "name": "Queen"
                            }
                        ]
                    }
                ]
            }

    monkeypatch.setattr(
        "gui.MusicBrainzAPI",
        FakeMusicBrainzAPI
    )

    window = MainWindow(
        root,
        repository
    )

    window.search_target.set("アルバム")

    window.search_entry.insert(
        0,
        "A Night at the Opera"
    )

    window.search()

    items = window.result_listbox.get(
        0,
        tk.END
    )

    assert len(items) == 1
    assert "Queen" in items[0]
    assert "A Night at the Opera" in items[0]