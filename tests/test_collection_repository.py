from collection_repository import CollectionRepository


def test_collection_can_be_registered():
    """
    コレクションをDBへ登録できることを確認するテスト。
    """

    # CollectionRepositoryを作成する
    repository = CollectionRepository(":memory:")

    # 登録する作品情報
    musicbrainz_id = "test-001"
    artist_name = "Queen"
    release_name = "A Night at the Opera"

    # コレクションをDBへ登録する
    repository.add_collection(
        musicbrainz_id,
        artist_name,
        release_name
    )

    # 登録したコレクションを取得する
    result = repository.get_collection(musicbrainz_id)

    # 登録した内容と取得した内容が一致することを確認する
    assert result == (
        musicbrainz_id,
        artist_name,
        release_name
    )