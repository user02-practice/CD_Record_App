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
    assert collection[7] == 1
    assert collection[8] == 0
    assert collection[9] == "名盤"

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

    assert collection[7] == 0
    assert collection[8] == 1
    assert collection[9] == "買い直したい"

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
    assert collection[7] == 1
    assert collection[8] == 0
    assert collection[9] == "名盤"

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