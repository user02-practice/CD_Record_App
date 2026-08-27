from unittest.mock import Mock, patch

import pytest
import requests

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

@patch("musicbrainz_api.requests.get")
def test_search_release_group_returns_requested_album(mock_get):
    """指定したAlbumが検索結果に含まれること"""

    # MusicBrainzから返ってくるデータを再現する
    mock_response = Mock()
    mock_response.json.return_value = {
        "release-groups": [
            {
                "id": "test-release-group-id",
                "title": "A Night at the Opera"
            },
            {
                "id": "other-release-group-id",
                "title": "Other Album"
            }
        ]
    }

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    result = api.search_release_group("A Night at the Opera")

    release_groups = result["release-groups"]

    album_titles = [
        release_group["title"]
        for release_group in release_groups
    ]

    assert "A Night at the Opera" in album_titles

@patch("musicbrainz_api.requests.get")
def test_search_release_group_prioritizes_exact_title(mock_get):
    """検索したAlbumと完全一致する作品を優先すること"""

    # 検索結果に別の作品が先に入っているケースを再現する
    mock_response = Mock()
    mock_response.json.return_value = {
        "release-groups": [
            {
                "id": "other-release-group-id",
                "title": "Other Album"
            },
            {
                "id": "test-release-group-id",
                "title": "A Night at the Opera"
            }
        ]
    }

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    result = api.search_release_group("A Night at the Opera")

    # 完全一致するAlbumが先頭になること
    assert result["release-groups"][0]["id"] == "test-release-group-id"
    assert result["release-groups"][0]["title"] == "A Night at the Opera"

@patch("musicbrainz_api.requests.get")
def test_search_track_returns_requested_track(mock_get):
    """指定したTrackが検索結果に含まれること"""

    # MusicBrainzから返ってくるデータを再現する
    mock_response = Mock()
    mock_response.json.return_value = {
        "recordings": [
            {
                "id": "test-recording-id",
                "title": "Bohemian Rhapsody"
            }
        ]
    }

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    result = api.search_track("Bohemian Rhapsody")

    assert result["recordings"][0]["id"] == "test-recording-id"
    assert result["recordings"][0]["title"] == "Bohemian Rhapsody"

@patch("musicbrainz_api.requests.get")
def test_search_track_prioritizes_exact_title(mock_get):
    """検索したTrackと完全一致する曲を優先すること"""

    # 検索結果に別の曲が先に入っているケースを再現する
    mock_response = Mock()
    mock_response.json.return_value = {
        "recordings": [
            {
                "id": "other-recording-id",
                "title": "Other Song"
            },
            {
                "id": "bohemian-rhapsody-id",
                "title": "Bohemian Rhapsody"
            }
        ]
    }

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    result = api.search_track("Bohemian Rhapsody")

    # 完全一致するTrackが先頭になること
    assert result["recordings"][0]["id"] == "bohemian-rhapsody-id"
    assert result["recordings"][0]["title"] == "Bohemian Rhapsody"

def test_search_keyword_returns_search_results():
    """Keyword検索でArtist、Album、Trackの検索結果を取得できること"""

    api = MusicBrainzAPI()

    # 各検索メソッドをテスト用に置き換える
    api.search_artist = Mock(return_value={
        "artists": [
            {
                "id": "test-artist-id",
                "name": "Queen"
            }
        ]
    })

    api.search_release_group = Mock(return_value={
        "release-groups": [
            {
                "id": "test-release-group-id",
                "title": "Queen"
            }
        ]
    })

    api.search_track = Mock(return_value={
        "recordings": [
            {
                "id": "test-recording-id",
                "title": "Queen"
            }
        ]
    })

    result = api.search_keyword("Queen")

    assert result["artists"][0]["name"] == "Queen"
    assert result["release-groups"][0]["title"] == "Queen"
    assert result["recordings"][0]["title"] == "Queen"

def test_search_keyword_calls_all_search_methods():
    """Keyword検索でArtist、Album、Trackの検索が実行されること"""

    api = MusicBrainzAPI()

    api.search_artist = Mock(return_value={
        "artists": []
    })

    api.search_release_group = Mock(return_value={
        "release-groups": []
    })

    api.search_track = Mock(return_value={
        "recordings": []
    })

    api.search_keyword("Queen")

    api.search_artist.assert_called_once_with("Queen")
    api.search_release_group.assert_called_once_with("Queen")
    api.search_track.assert_called_once_with("Queen")

@patch("musicbrainz_api.requests.get")
def test_search_artist_raises_error_when_api_returns_error(mock_get):
    """Artist検索でAPIエラーが発生した場合に例外が発生すること"""

    # APIがエラーを返すケースを再現する
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError()

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    # APIエラーが発生することを確認する
    with pytest.raises(requests.HTTPError):
        api.search_artist("Queen")

@patch("musicbrainz_api.requests.get")
def test_search_artist_returns_empty_result_when_no_artist_found(mock_get):
    """Artistが見つからない場合に空の検索結果を返すこと"""

    # Artistが見つからないケースを再現する
    mock_response = Mock()
    mock_response.json.return_value = {
        "artists": []
    }

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    result = api.search_artist("存在しないアーティスト")

    # 検索結果が空であることを確認する
    assert result["artists"] == []

@patch("musicbrainz_api.requests.get")
def test_search_release_group_raises_error_when_api_returns_error(mock_get):
    """作品検索でAPIエラーが発生した場合に例外が発生すること"""

    # APIがエラーを返すケースを再現する
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError()

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    # APIエラーが発生することを確認する
    with pytest.raises(requests.HTTPError):
        api.search_release_group("A Night at the Opera")


@patch("musicbrainz_api.requests.get")
def test_search_release_group_returns_empty_result_when_no_album_found(mock_get):
    """作品が見つからない場合に空の検索結果を返すこと"""

    # 作品が見つからないケースを再現する
    mock_response = Mock()
    mock_response.json.return_value = {
        "release-groups": []
    }

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    result = api.search_release_group("存在しない作品")

    # 検索結果が空であることを確認する
    assert result["release-groups"] == []

@patch("musicbrainz_api.requests.get")
def test_search_track_raises_error_when_api_returns_error(mock_get):
    """Track検索でAPIエラーが発生した場合に例外が発生すること"""

    # APIがエラーを返すケースを再現する
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError()

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    # APIエラーが発生することを確認する
    with pytest.raises(requests.HTTPError):
        api.search_track("Bohemian Rhapsody")

@patch("musicbrainz_api.requests.get")
def test_search_track_returns_empty_result_when_no_track_found(mock_get):
    """Trackが見つからない場合に空の検索結果を返すこと"""

    # Trackが見つからないケースを再現する
    mock_response = Mock()
    mock_response.json.return_value = {
        "recordings": []
    }

    mock_get.return_value = mock_response

    api = MusicBrainzAPI()

    result = api.search_track("存在しないTrack")

    # 検索結果が空であることを確認する
    assert result["recordings"] == []

def test_search_keyword_returns_empty_results_when_nothing_found():
    """Keyword検索で何も見つからない場合に空の検索結果を返すこと"""

    api = MusicBrainzAPI()

    # 各検索メソッドが0件を返すケースを再現する
    api.search_artist = Mock(return_value={
        "artists": []
    })

    api.search_release_group = Mock(return_value={
        "release-groups": []
    })

    api.search_track = Mock(return_value={
        "recordings": []
    })

    result = api.search_keyword("存在しないキーワード")

    # 3種類すべての検索結果が空であることを確認する
    assert result["artists"] == []
    assert result["release-groups"] == []
    assert result["recordings"] == []

def test_search_keyword_raises_error_when_api_returns_error():
    """Keyword検索でAPIエラーが発生した場合に例外が発生すること"""

    api = MusicBrainzAPI()

    # Artist検索でAPIエラーが発生するケースを再現する
    api.search_artist = Mock(
        side_effect=requests.HTTPError()
    )

    api.search_release_group = Mock(return_value={
        "release-groups": []
    })

    api.search_track = Mock(return_value={
        "recordings": []
    })

    # APIエラーが発生することを確認する
    with pytest.raises(requests.HTTPError):
        api.search_keyword("Queen")


def test_get_release_group():
    """
    MusicBrainz IDを指定すると、
    Release Groupの詳細情報を取得できることを確認する。
    """

    api = MusicBrainzAPI()

    # テスト用のMusicBrainz ID
    musicbrainz_id = "test-release-group-id"

    # API通信をモックする
    with patch("musicbrainz_api.requests.get") as mock_get:

        # APIから返ってくるデータを設定する
        mock_response = Mock()

        mock_response.json.return_value = {
            "id": musicbrainz_id,
            "title": "A Night at the Opera",
            "first-release-date": "1975-11-21"
        }

        mock_response.raise_for_status.return_value = None

        mock_get.return_value = mock_response

        # Release Groupを取得する
        result = api.get_release_group(musicbrainz_id)

    # ========================================
    # 確認
    # ========================================

    assert result["id"] == musicbrainz_id
    assert result["title"] == "A Night at the Opera"
    assert result["first-release-date"] == "1975-11-21"