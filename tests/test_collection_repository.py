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
    artist = "Queen"
    album = "A Night at the Opera"

    # ========================================
    # 実行：コレクションをDBへ登録する
    # ========================================

    repository.add_collection(
        musicbrainz_id,
        artist,
        album
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
        artist,
        album
    )