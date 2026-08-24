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

    # ========================================
    # 実行：コレクションをDBへ登録する
    # ========================================

    repository.add_collection(
        musicbrainz_id,
        artist_name,
        release_name,
        label
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
        label
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


def test_collection_can_be_registered_with_label():
    """レーベルを含むコレクションをDBへ登録し、取得できること"""

    repository = CollectionRepository(":memory:")

    musicbrainz_id = "test-002"
    artist_name = "Queen"
    release_name = "A Night at the Opera"
    label = "EMI"

    repository.add_collection(
        musicbrainz_id,
        artist_name,
        release_name,
        label
    )

    result = repository.get_collection(musicbrainz_id)

    assert result == (
        musicbrainz_id,
        artist_name,
        release_name,
        label
    )