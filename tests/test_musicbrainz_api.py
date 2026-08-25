from unittest.mock import Mock, patch

from musicbrainz_api import MusicBrainzAPI


def test_musicbrainz_api_can_be_created():
    """MusicBrainzAPIクラスを作成できること"""
    api = MusicBrainzAPI()

    assert api is not None


@patch("musicbrainz_api.requests.get")
def test_search_artist_returns_queen(mock_get):
    """Queenを検索するとQueenの情報が含まれること"""

    # APIから返ってくるデータを再現する
    mock_response = Mock()
    mock_response.json.return_value = {
        "artists": [
            {
                "id": "test-id",
                "name": "Queen"
            }
        ]
    }

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    result = api.search_artist("Queen")

    artist_names = [
        artist["name"]
        for artist in result["artists"]
    ]

    assert "Queen" in artist_names


@patch("musicbrainz_api.requests.get")
def test_search_artist(mock_get):
    """アーティスト名で検索できること"""

    # APIから返ってくるデータを再現する
    mock_response = Mock()
    mock_response.json.return_value = {
        "artists": []
    }

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    result = api.search_artist("Queen")

    assert result is not None


@patch("musicbrainz_api.requests.get")
def test_search_release_group(mock_get):
    """作品名を検索すると作品情報が取得できること"""

    # APIから返ってくるデータを再現する
    mock_response = Mock()
    mock_response.json.return_value = {
        "release-groups": [
            {
                "id": "test-release-group-id",
                "title": "A Night at the Opera"
            }
        ]
    }

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    result = api.search_release_group("A Night at the Opera")

    assert result["release-groups"][0]["id"] == "test-release-group-id"
    assert result["release-groups"][0]["title"] == "A Night at the Opera"


def test_get_release_group_info():
    """Release Groupから作品情報を取得できること"""

    api = MusicBrainzAPI()

    release_group = {
        "id": "test-release-group-id",
        "title": "A Night at the Opera",
        "artist-credit": [
            {
                "name": "Queen"
            }
        ]
    }

    result = api.get_release_group_info(release_group)

    assert result["musicbrainz_id"] == "test-release-group-id"
    assert result["artist_name"] == "Queen"
    assert result["release_name"] == "A Night at the Opera"


@patch("musicbrainz_api.requests.get")
def test_get_release_group(mock_get):
    """MusicBrainz IDからRelease Groupの詳細を取得できること"""

    # APIから返ってくるデータを再現する
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": "test-release-group-id",
        "title": "A Night at the Opera",
        "artist-credit": [
            {
                "name": "Queen"
            }
        ]
    }

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    result = api.get_release_group("test-release-group-id")

    assert result["id"] == "test-release-group-id"
    assert result["title"] == "A Night at the Opera"


@patch("musicbrainz_api.requests.get")
def test_get_releases(mock_get):
    """Release Group IDからRelease一覧を取得できること"""

    # APIから返ってくるデータを再現する
    mock_response = Mock()
    mock_response.json.return_value = {
        "releases": [
            {
                "id": "test-release-id",
                "title": "A Night at the Opera",
                "date": "1975-11-21",
                "country": "GB"
            }
        ]
    }

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    result = api.get_releases("test-release-group-id")

    assert len(result["releases"]) == 1
    assert result["releases"][0]["id"] == "test-release-id"
    assert result["releases"][0]["title"] == "A Night at the Opera"


def test_get_release_format():
    """Releaseからフォーマットを取得できること"""

    api = MusicBrainzAPI()

    release = {
        "media": [
            {
                "format": "CD"
            }
        ]
    }

    result = api.get_release_format(release)

    assert result == ["CD"]


def test_get_release_label():
    """Releaseからレーベルを取得できること"""

    api = MusicBrainzAPI()

    release = {
        "label-info": [
            {
                "label": {
                    "name": "EMI"
                }
            }
        ]
    }

    result = api.get_release_label(release)

    assert result == "EMI"


def test_get_release_label_returns_none_when_label_does_not_exist():
    """Releaseにレーベル情報がない場合はNoneを返すこと"""

    api = MusicBrainzAPI()

    release = {
        "label-info": []
    }

    result = api.get_release_label(release)

    assert result is None


def test_get_release_info():
    """Releaseから発売日、国、レーベルを取得できること"""

    api = MusicBrainzAPI()

    release = {
        "id": "test-release-id",
        "title": "A Night at the Opera",
        "date": "1975-11-21",
        "country": "GB",
        "label-info": [
            {
                "label": {
                    "name": "EMI"
                }
            }
        ]
    }

    result = api.get_release_info(release)

    assert result["release_date"] == "1975-11-21"
    assert result["country"] == "GB"
    assert result["label"] == "EMI"

@patch("musicbrainz_api.requests.get")
def test_search_artist_uses_artist_query(mock_get):
    """Artist検索ではartist検索条件を使用すること"""

    # APIから返ってくるデータを再現する
    mock_response = Mock()
    mock_response.json.return_value = {
        "artists": []
    }

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    api.search_artist("Queen")

    # requests.getが呼び出されたことを確認する
    mock_get.assert_called_once()

    # requests.getに渡された引数を確認する
    _, kwargs = mock_get.call_args

    assert kwargs["params"]["query"] == "artist:Queen"

@patch("musicbrainz_api.requests.get")
def test_search_artist_returns_queen_band(mock_get):
    """Queenを検索するとQueenというバンドを取得できること"""

    # MusicBrainzから複数のQueenが返ってくるケースを再現する
    mock_response = Mock()
    mock_response.json.return_value = {
        "artists": [
            {
                "id": "other-queen-id",
                "name": "Queen",
                "type": "Person"
            },
            {
                "id": "queen-band-id",
                "name": "Queen",
                "type": "Group"
            }
        ]
    }

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    result = api.search_artist("Queen")

    # Queenというバンドが取得できること
    assert result["artists"][0]["id"] == "queen-band-id"
    assert result["artists"][0]["name"] == "Queen"
    assert result["artists"][0]["type"] == "Group"