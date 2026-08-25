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
        "test-001",
        "Queen",
        "A Night at the Opera",
        None,
        None,
        None,
        [],
        0,
        0,
        None

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

    repository.add_collection(
        musicbrainz_id,
        artist_name,
        release_name,
        label,
        release_date,
        country,
        formats,
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
        cd_owned,
        vinyl_owned,
        memo
    )

def test_collections_can_be_retrieved():
    """登録されているコレクションを一覧で取得できること"""

    repository = CollectionRepository(":memory:")

    # コレクションを2件登録
    repository.add_collection(
        "test-001",
        "Queen",
        "A Night at the Opera",
        None,
        None,
        None,
        [],
        0,
        0,
        None
    )

    repository.add_collection(
        "test-002",
        "The Beatles",
        "Abbey Road",
        None,
        None,
        None,
        [],
        0,
        0,
        None
    )

    # コレクション一覧を取得
    collections = repository.get_collections()

    # 2件取得できることを確認
    assert len(collections) == 2

    # 登録した内容を確認
    assert collections[0][0] == "test-001"
    assert collections[0][1] == "Queen"
    assert collections[0][2] == "A Night at the Opera"

    assert collections[1][0] == "test-002"
    assert collections[1][1] == "The Beatles"
    assert collections[1][2] == "Abbey Road"

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
        1,
        1,
        "CDとVinylの両方を所有"
    )