from collection_repository import CollectionRepository


def test_collection_can_be_registered():
    """
    コレクションをDBへ登録し、
    登録したコレクションを正しく取得できることを確認するテスト。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成する
    # ========================================

    # :memory: を指定すると、テスト専用の一時的なDBを作成する
    # テスト終了後にDBの内容は破棄される
    repository = CollectionRepository(":memory:")

    # テストで登録する作品情報
    musicbrainz_id = "test-001"
    artist_name = "Queen"
    release_name = "A Night at the Opera"
    label = None
    release_date = None
    country = None
    formats = []

    # ジャケット画像URL
    # このテストでは画像URLを設定しないためNoneにする
    jacket_url = None

    # ========================================
    # 実行：コレクションをDBへ登録する
    # ========================================

    repository.add_collection(
        musicbrainz_id,
        artist_name,
        release_name,
        label,
        release_date,
        country,
        formats,
        jacket_url,
        0,
        0,
        None
    )

    # ========================================
    # 確認：登録したコレクションを取得する
    # ========================================

    result = repository.get_collection(musicbrainz_id)

    # ========================================
    # 結果：登録した内容と取得した内容が一致することを確認する
    # ========================================

    assert result == (
        musicbrainz_id,
        artist_name,
        release_name,
        label,
        release_date,
        country,
        formats,
        jacket_url,
        0,
        0,
        None
    )

def test_get_collection_returns_none_when_id_does_not_exist():
    """存在しないMusicBrainz IDを検索した場合、Noneが返ること"""

    repository = CollectionRepository(":memory:")

    result = repository.get_collection("not-exist-id")

    assert result is None


def test_delete_collection():
    """登録したコレクションを削除すると、検索結果がNoneになること"""

    repository = CollectionRepository(":memory:")

    # コレクションを登録
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

    # 削除
    repository.delete_collection("test-001")

    # 削除後は存在しないことを確認
    result = repository.get_collection("test-001")

    assert result is None


def test_delete_collection_when_id_does_not_exist():
    """存在しないMusicBrainz IDを削除してもエラーにならないこと"""

    repository = CollectionRepository(":memory:")

    # 存在しないMusicBrainz IDを削除する
    repository.delete_collection("not-exist-id")

    # エラーが発生せず、検索結果がNoneであることを確認
    result = repository.get_collection("not-exist-id")

    assert result is None


def test_collection_can_be_registered_with_release_info():
    """発売情報を含むコレクションをDBへ登録し、取得できること"""

    repository = CollectionRepository(":memory:")

    musicbrainz_id = "test-003"
    artist_name = "Queen"
    release_name = "A Night at the Opera"
    label = "EMI"
    release_date = "1975-11-21"
    country = "GB"
    formats = ["CD"]

    # ジャケット画像URL
    # このテストでは画像URLを設定しないためNoneにする
    jacket_url = None

    repository.add_collection(
        musicbrainz_id,
        artist_name,
        release_name,
        label,
        release_date,
        country,
        formats,
        jacket_url,
        0,
        0,
        None
    )

    result = repository.get_collection(musicbrainz_id)

    assert result == (
        musicbrainz_id,
        artist_name,
        release_name,
        label,
        release_date,
        country,
        formats,
        jacket_url,
        0,
        0,
        None
    )


def test_collection_can_be_registered_with_owned_status():
    """CDとVinylの所有状態を含むコレクションを登録・取得できること"""

    repository = CollectionRepository(":memory:")

    musicbrainz_id = "test-004"
    artist_name = "Queen"
    release_name = "A Night at the Opera"
    label = "EMI"
    release_date = "1975-11-21"
    country = "GB"
    formats = ["CD"]
    # ジャケット画像URL
    # このテストでは画像URLを設定しないためNoneにする
    jacket_url = None

    cd_owned = 1
    vinyl_owned = 0

    repository.add_collection(
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
        None
    )

    result = repository.get_collection(musicbrainz_id)

    assert result == (
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
        None
    )


def test_collection_can_be_registered_with_memo():
    """メモを含むコレクションを登録・取得できること"""

    repository = CollectionRepository(":memory:")

    musicbrainz_id = "test-005"
    artist_name = "Queen"
    release_name = "A Night at the Opera"
    label = "EMI"
    release_date = "1975-11-21"
    country = "GB"
    formats = ["CD"]
    # ジャケット画像URL
    # このテストでは画像URLを設定しないためNoneにする
    jacket_url = None

    cd_owned = 1
    vinyl_owned = 0
    memo = "中古で購入。ジャケットに少し傷あり。"

    repository.add_collection(
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
    )

    result = repository.get_collection(musicbrainz_id)

    assert result == (
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
    )

def test_collections_can_be_retrieved():
    """登録されているコレクションを一覧で取得できること"""

    repository = CollectionRepository(":memory:")

    # コレクションを2件登録
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
        "test-002",
        "The Beatles",
        "Abbey Road",
        None,
        None,
        None,
        [],
        None,  # jacket_url
        0,
        0,
        None
    )

    # コレクション一覧を取得
    collections = repository.get_collections()

    # 2件取得できることを確認
    assert len(collections) == 2

    # 後から登録した作品が先に取得されることを確認する
    assert collections[0][0] == "test-002"
    assert collections[0][1] == "The Beatles"
    assert collections[0][2] == "Abbey Road"

    # 先に登録した作品はその次に取得される
    assert collections[1][0] == "test-001"
    assert collections[1][1] == "Queen"
    assert collections[1][2] == "A Night at the Opera"

def test_get_collections_returns_empty_list_when_no_collections():
    """コレクションが登録されていない場合、空のリストが返ること"""

    # テスト用のRepositoryを作成
    repository = CollectionRepository(":memory:")

    # コレクション一覧を取得
    collections = repository.get_collections()

    # 空のリストが返ることを確認
    assert collections == []

def test_collection_can_be_updated():
    """登録済みコレクションの所有状態とメモを更新できること"""

    # テスト用のRepositoryを作成
    repository = CollectionRepository(":memory:")

    # コレクションを登録
    repository.add_collection(
        "test-006",
        "Queen",
        "A Night at the Opera",
        "EMI",
        "1975-11-21",
        "GB",
        ["CD"],
        None,  # jacket_url
        0,
        0,
        None
    )

    # CDを所有、Vinylは未所有、メモを更新
    repository.update_collection(
        "test-006",
        1,
        0,
        "中古で購入した。"
    )

    # 更新後のコレクションを取得
    result = repository.get_collection("test-006")

    # 更新された内容を確認
    assert result == (
        "test-006",
        "Queen",
        "A Night at the Opera",
        "EMI",
        "1975-11-21",
        "GB",
        ["CD"],
        None,  # jacket_url
        1,
        0,
        "中古で購入した。"
    )

def test_update_collection_when_id_does_not_exist():
    """存在しないMusicBrainz IDを更新してもエラーにならないこと"""

    # テスト用のRepositoryを作成
    repository = CollectionRepository(":memory:")

    # 存在しないIDを更新する
    repository.update_collection(
        "not-exist-id",
        1,
        0,
        "存在しないコレクション"
    )

    # エラーが発生しないことを確認
    result = repository.get_collection("not-exist-id")

    # 存在しないためNoneであることを確認
    assert result is None

def test_collection_can_be_updated_to_own_both_formats():
    """CDとVinylの両方を所有状態に更新できること"""

    # テスト用のRepositoryを作成
    repository = CollectionRepository(":memory:")

    # CD・Vinylともに未所有で登録
    repository.add_collection(
        "test-007",
        "The Beatles",
        "Abbey Road",
        "Apple Records",
        "1969-09-26",
        "GB",
        ["CD", "Vinyl"],
        None,  # jacket_url
        0,
        0,
        None
    )

    # CD・Vinylの両方を所有状態に変更
    repository.update_collection(
        "test-007",
        1,
        1,
        "CDとVinylの両方を所有"
    )

    # 更新後のコレクションを取得
    result = repository.get_collection("test-007")

    # 更新内容を確認
    assert result == (
        "test-007",
        "The Beatles",
        "Abbey Road",
        "Apple Records",
        "1969-09-26",
        "GB",
        ["CD", "Vinyl"],
        None,  # jacket_url
        1,
        1,
        "CDとVinylの両方を所有"
    )

def test_collections_can_be_searched_by_keyword():
    """
    アーティスト名や作品名に含まれるキーワードで
    コレクションを検索できることを確認するテスト。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成
    # ========================================

    repository = CollectionRepository(":memory:")

    # テスト用データを登録
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

    repository.add_collection(
        musicbrainz_id="test-003",
        artist_name="Queen",
        release_name="News of the World",
        label="EMI",
        release_date="1977-10-28",
        country="GB",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    # ========================================
    # 実行：Queenで検索
    # ========================================

    results = repository.search_collections("Queen")

    # ========================================
    # 検証
    # ========================================

    assert len(results) == 2

    assert results[0][0] == "test-003"
    assert results[1][0] == "test-001"


def test_collections_can_be_searched_by_release_name():
    """
    作品名に含まれるキーワードで
    コレクションを検索できることを確認するテスト。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成
    # ========================================

    repository = CollectionRepository(":memory:")

    # テスト用データを登録
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

    repository.add_collection(
        musicbrainz_id="test-003",
        artist_name="Queen",
        release_name="News of the World",
        label="EMI",
        release_date="1977-10-28",
        country="GB",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    # ========================================
    # 実行：作品名で検索
    # ========================================

    results = repository.search_collections("Abbey Road")

    # ========================================
    # 検証
    # ========================================

    assert len(results) == 1
    assert results[0][0] == "test-002"
    assert results[0][1] == "The Beatles"
    assert results[0][2] == "Abbey Road"

def test_collections_can_be_searched_by_partial_keyword():
    """
    アーティスト名や作品名の一部を指定して
    コレクションを検索できることを確認するテスト。
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

    repository.add_collection(
        musicbrainz_id="test-003",
        artist_name="Queen",
        release_name="News of the World",
        label="EMI",
        release_date="1977-10-28",
        country="GB",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    # ========================================
    # 実行：一部のキーワードで検索
    # ========================================

    results = repository.search_collections("Beat")

    # ========================================
    # 検証
    # ========================================

    assert len(results) == 1
    assert results[0][0] == "test-002"
    assert results[0][1] == "The Beatles"

def test_search_collections_returns_empty_list_when_no_match():
    """
    検索キーワードに一致するコレクションが存在しない場合、
    空のリストが返ることを確認するテスト。
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

    # ========================================
    # 実行：存在しないキーワードで検索
    # ========================================

    results = repository.search_collections("Michael Jackson")

    # ========================================
    # 検証
    # ========================================

    assert results == []

def test_search_collections_returns_all_collections_when_keyword_is_empty():
    """
    検索キーワードが空文字の場合、
    すべてのコレクションが返ることを確認するテスト。
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

    repository.add_collection(
        musicbrainz_id="test-003",
        artist_name="Queen",
        release_name="News of the World",
        label="EMI",
        release_date="1977-10-28",
        country="GB",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    # ========================================
    # 実行：空文字で検索
    # ========================================

    results = repository.search_collections("")

    # ========================================
    # 検証
    # ========================================

    assert len(results) == 3

    assert results[0][0] == "test-003"
    assert results[1][0] == "test-002"
    assert results[2][0] == "test-001"

def test_collections_can_be_filtered_by_cd_owned():
    """
    CDを所有しているコレクションだけを
    絞り込んで取得できることを確認するテスト。
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

    repository.add_collection(
        musicbrainz_id="test-003",
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

    # ========================================
    # 実行：CD所有で絞り込み
    # ========================================

    results = repository.get_collections_by_cd_owned()

    # ========================================
    # 検証
    # ========================================

    assert len(results) == 2

    assert results[0][0] == "test-002"
    assert results[1][0] == "test-001"

def test_collections_can_be_filtered_by_vinyl_owned():
    """
    Vinylを所有しているコレクションだけを
    絞り込んで取得できることを確認するテスト。
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

    repository.add_collection(
        musicbrainz_id="test-003",
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

    # ========================================
    # 実行：Vinyl所有で絞り込み
    # ========================================

    results = repository.get_collections_by_vinyl_owned()

    # ========================================
    # 検証
    # ========================================

    assert len(results) == 2

    assert results[0][0] == "test-003"
    assert results[1][0] == "test-002"

def test_get_collections_by_cd_owned_returns_empty_list_when_no_match():
    """
    CDを所有しているコレクションが存在しない場合、
    空のリストが返ることを確認するテスト。
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
        formats=["Vinyl"],
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    # ========================================
    # 実行：CD所有で絞り込み
    # ========================================

    results = repository.get_collections_by_cd_owned()

    # ========================================
    # 検証
    # ========================================

    assert results == []

def test_get_collections_by_vinyl_owned_returns_empty_list_when_no_match():
    """
    Vinylを所有しているコレクションが存在しない場合、
    空のリストが返ることを確認するテスト。
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

    # ========================================
    # 実行：Vinyl所有で絞り込み
    # ========================================

    results = repository.get_collections_by_vinyl_owned()

    # ========================================
    # 検証
    # ========================================

    assert results == []

def test_collections_can_be_filtered_by_keyword_and_cd_owned():
    """
    キーワードとCD所有状態を組み合わせて
    コレクションを絞り込めることを確認するテスト。
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
        vinyl_owned=1,
        memo=""
    )

    # ========================================
    # 実行：Queen + CD所有で絞り込み
    # ========================================

    results = repository.filter_collections(
        keyword="Queen",
        cd_owned=True
    )

    # ========================================
    # 検証
    # ========================================

    assert len(results) == 1
    assert results[0][0] == "test-001"

def test_collections_can_be_filtered_by_keyword_and_vinyl_owned():
    """
    キーワードとVinyl所有状態を組み合わせて
    コレクションを絞り込めることを確認するテスト。
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
        vinyl_owned=1,
        memo=""
    )

    # ========================================
    # 実行：Queen + Vinyl所有で絞り込み
    # ========================================

    results = repository.filter_collections(
        keyword="Queen",
        vinyl_owned=True
    )

    # ========================================
    # 検証
    # ========================================

    assert len(results) == 1
    assert results[0][0] == "test-002"

def test_collections_can_be_filtered_by_cd_and_vinyl_owned():
    """
    CDとVinylの両方を所有しているコレクションだけを
    絞り込めることを確認するテスト。
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
    # 実行：CD + Vinyl所有で絞り込み
    # ========================================

    results = repository.filter_collections(
        cd_owned=True,
        vinyl_owned=True
    )

    # ========================================
    # 検証
    # ========================================

    assert len(results) == 1
    assert results[0][0] == "test-002"

def test_collections_can_be_filtered_by_neither_cd_nor_vinyl_owned():
    """
    CDもVinylも所有していないコレクションだけを
    絞り込めることを確認するテスト。
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

    repository.add_collection(
        musicbrainz_id="test-004",
        artist_name="David Bowie",
        release_name="Low",
        label="RCA",
        release_date="1977-01-14",
        country="GB",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=0,
        memo=""
    )

    # ========================================
    # 実行：CDもVinylも未所有で絞り込み
    # ========================================

    results = repository.filter_collections(
        cd_owned=False,
        vinyl_owned=False
    )

    # ========================================
    # 検証
    # ========================================

    assert len(results) == 1
    assert results[0][0] == "test-004"


def test_filter_collections_returns_all_collections_when_no_conditions():
    """
    検索条件を指定しなかった場合、
    すべてのコレクションが返ることを確認するテスト。
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
    # 実行：条件なしで絞り込み
    # ========================================

    results = repository.filter_collections()

    # ========================================
    # 検証
    # ========================================

    assert len(results) == 2
    assert results[0][0] == "test-002"
    assert results[1][0] == "test-001"

def test_collection_can_be_registered_with_jacket_url():
    """ジャケット画像URLを含むコレクションを登録・取得できること"""

    repository = CollectionRepository(":memory:")

    repository.add_collection(
        musicbrainz_id="test-jacket-001",
        artist_name="Queen",
        release_name="A Night at the Opera",
        label="EMI",
        release_date="1975-11-21",
        country="GB",
        formats=["CD"],
        jacket_url="https://example.com/jacket.jpg",
        cd_owned=1,
        vinyl_owned=0,
        memo=""
    )

    result = repository.get_collection("test-jacket-001")

    assert result[7] == "https://example.com/jacket.jpg"

def test_collections_are_returned_newest_first():
    """
    コレクション一覧を取得したとき、
    新しく登録した作品が先に返ることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成する
    # ========================================

    repository = CollectionRepository(":memory:")

    # 1件目を登録する
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

    # 2件目を登録する
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
    # 実行：コレクション一覧を取得する
    # ========================================

    collections = repository.get_collections()

    # ========================================
    # 確認：後から登録した作品が先に返る
    # ========================================

    assert collections[0][0] == "test-002"
    assert collections[1][0] == "test-001"

def test_collections_can_be_sorted_by_artist_name():
    """
    コレクションをアーティスト名の昇順で
    並び替えて取得できることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成する
    # ========================================

    repository = CollectionRepository(":memory:")

    # Queen
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

    # The Beatles
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

    # ABBA
    repository.add_collection(
        musicbrainz_id="test-003",
        artist_name="ABBA",
        release_name="Arrival",
        label="Polar",
        release_date="1976-10-11",
        country="SE",
        formats=["CD", "Vinyl"],
        jacket_url=None,
        cd_owned=0,
        vinyl_owned=1,
        memo=""
    )

    # ========================================
    # 実行：アーティスト名で並び替える
    # ========================================

    results = repository.get_collections_sorted_by_artist()

    # ========================================
    # 確認：アーティスト名の昇順になる
    # ========================================

    assert len(results) == 3

    assert results[0][1] == "ABBA"
    assert results[1][1] == "Queen"
    assert results[2][1] == "The Beatles"

def test_collections_can_be_searched_by_memo():
    """
    メモに含まれるキーワードで
    コレクションを検索できることを確認する。
    """

    # ========================================
    # 準備：テスト用のRepositoryを作成する
    # ========================================

    repository = CollectionRepository(":memory:")

    # Queen
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

    # The Beatles
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

    # ========================================
    # 実行：メモの内容で検索する
    # ========================================

    results = repository.search_collections(
        "お気に入り"
    )

    # ========================================
    # 確認：メモが一致した作品だけ取得できる
    # ========================================

    assert len(results) == 1
    assert results[0][0] == "test-001"
    assert results[0][1] == "Queen"
    assert results[0][2] == "A Night at the Opera"

def test_collections_can_be_searched_by_artist_only():
    """
    検索対象をアーティスト名にした場合、
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

    # ========================================
    # 実行：アーティスト名だけを検索する
    # ========================================

    results = repository.search_collections_by_artist(
        "Queen"
    )

    # ========================================
    # 確認：アーティスト名が一致する作品だけ取得できる
    # ========================================

    assert len(results) == 1
    assert results[0][0] == "test-001"
    assert results[0][1] == "Queen"

def test_collections_can_be_searched_by_album_only():
    """
    検索対象をアルバム名にした場合、
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

    # ========================================
    # 実行：アルバム名だけを検索する
    # ========================================

    results = repository.search_collections_by_album(
        "Queen"
    )

    # ========================================
    # 確認：アルバム名が一致する作品だけ取得できる
    # ========================================

    assert len(results) == 1
    assert results[0][0] == "test-001"
    assert results[0][2] == "Queen Tribute"