import time
import requests


class MusicBrainzAPI:
    """
    MusicBrainz APIを扱うクラス。
    """

    def __init__(self):
        """
        MusicBrainzAPIを初期化する。
        """
        pass

    def search_artist(self, artist_name, offset=0):
        """
        アーティスト名でMusicBrainzを検索する。

        Args:
            artist_name (str):
                検索するアーティスト名。

        Returns:
            dict:
                検索したアーティストの情報。
        """

        url = "https://musicbrainz.org/ws/2/artist/"

        params = {
            "query": f"artist:{artist_name}",
            "fmt": "json",
            "limit": 20,
            "offset": offset
        }

        headers = {
            "User-Agent": "CD-Record-App/1.0"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        # 検索結果から、名前が一致するGroupを探す
        for artist in result.get("artists", []):
            if (
                    artist.get("name") == artist_name
                    and artist.get("type") == "Group"
            ):
                result["artists"].remove(artist)
                result["artists"].insert(0, artist)
                break

        return result

    def search_release_group(self, release_group_name, offset=0):
        """
        作品名でMusicBrainzのRelease Groupを検索する。

        Args:
            release_group_name (str):
                検索する作品名。

        Returns:
            dict:
                MusicBrainz APIから取得した検索結果。
        """

        url = "https://musicbrainz.org/ws/2/release-group/"

        params = {
            "query": f'releasegroup:"{release_group_name}"',
            "fmt": "json",
            "limit": 20,
            "offset": offset
        }

        headers = {
            "User-Agent": "CD-Record-App/1.0"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        # 検索したAlbum名と完全一致する作品を探す
        for release_group in result.get("release-groups", []):
            if release_group.get("title") == release_group_name:
                result["release-groups"].remove(release_group)
                result["release-groups"].insert(0, release_group)
                break

        return result

    def search_release_group_by_artist(self, artist_name, offset=0):
        """
        アーティスト名でMusicBrainzのRelease Groupを検索する。

        503エラーが発生した場合は、1回だけ再試行する。
        """

        url = "https://musicbrainz.org/ws/2/release-group/"

        params = {
            "query": f'artist:"{artist_name}"',
            "fmt": "json",
            "limit": 20,
            "offset": offset
        }

        headers = {
            "User-Agent": "CD-Record-App/1.0"
        }

        for attempt in range(2):
            try:
                response = requests.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=10
                )

                response.raise_for_status()

                return response.json()


            except requests.HTTPError as e:

                status_code = (

                    e.response.status_code

                    if e.response is not None

                    else None

                )

                if status_code != 503:
                    raise

                if attempt == 1:
                    raise

                time.sleep(1)

    def search_track(self, track_name, offset=0):
        """
        Track名でMusicBrainzのRecordingを検索する。

        Args:
            track_name (str):
                検索するTrack名。

        Returns:
            dict:
                MusicBrainz APIから取得した検索結果。
        """

        url = "https://musicbrainz.org/ws/2/recording/"

        params = {
            "query": f'recording:"{track_name}"',
            "fmt": "json",
            "limit": 20,
            "offset": offset
        }

        headers = {
            "User-Agent": "CD-Record-App/1.0"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        # 検索したTrack名と完全一致する曲を探す
        for recording in result.get("recordings", []):
            if recording.get("title") == track_name:
                result["recordings"].remove(recording)
                result["recordings"].insert(0, recording)
                break

        return result

    def search_keyword(self, keyword, offset=0):
        """
        キーワードでArtist、Album、Trackを検索する。

        Args:
            keyword (str):
                検索するキーワード。

        Returns:
            dict:
                Artist、Album、Trackの検索結果。
        """

        artist_result = self.search_artist(
            keyword,
            offset=offset
        )

        release_group_result = self.search_release_group(
            keyword,
            offset=offset
        )

        recording_result = self.search_track(
            keyword,
            offset=offset
        )

        return {
            "artists": artist_result["artists"],
            "artist_count": artist_result.get("count", 0),

            "release-groups": release_group_result["release-groups"],
            "release_group_count": release_group_result.get("count", 0),

            "recordings": recording_result["recordings"],
            "recording_count": recording_result.get("count", 0)
        }

    def get_release_group_info(self, release_group):
        """
        Release Groupの検索結果から作品情報を取得する。

        Args:
            release_group (dict):
                MusicBrainzから取得したRelease Groupの情報。

        Returns:
            dict:
                アプリで使用する作品情報。
        """

        return {
            "musicbrainz_id": release_group["id"],
            "artist_name": release_group["artist-credit"][0]["name"],
            "release_name": release_group["title"]
        }

    def get_release_group(self, musicbrainz_id):
        """
        MusicBrainz IDを使ってRelease Groupの詳細を取得する。

        Args:
            musicbrainz_id (str):
                取得するRelease GroupのMusicBrainz ID。

        Returns:
            dict:
                MusicBrainz APIから取得したRelease Groupの情報。
        """

        url = f"https://musicbrainz.org/ws/2/release-group/{musicbrainz_id}"

        params = {
            "fmt": "json",
            "inc": "artist-credits"
        }

        headers = {
            "User-Agent": "CD-Record-App/1.0"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    def get_releases(self, release_group_id):
        """
        Release Group IDを使ってRelease一覧を取得する。

        Args:
            release_group_id (str):
                Release GroupのMusicBrainz ID。

        Returns:
            dict:
                MusicBrainz APIから取得したRelease一覧。
        """

        url = "https://musicbrainz.org/ws/2/release"

        params = {
            "release-group": release_group_id,
            "fmt": "json",
            "limit": 20,
            "inc": "media+labels"
        }

        headers = {
            "User-Agent": "CD-Record-App/1.0"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    def get_release_info(self, release):
        """
        Releaseからアプリで使用する発売情報を取得する。

        Args:
            release (dict):
                MusicBrainzから取得したRelease情報。

        Returns:
            dict:
                発売日、国、レーベル
        """

        return {
            "release_date": release["date"],
            "country": release["country"],
            "label": self.get_release_label(release)
        }

    def get_release_format(self, release):
        """
        Releaseからフォーマットを取得する。

        Args:
            release (dict):
                MusicBrainzから取得したRelease情報。

        Returns:
            list:
                CDやVinylなどのフォーマット一覧。
        """

        return [
            medium["format"]
            for medium in release["media"]
            if medium.get("format")
        ]

    def get_release_label(self, release):
        """Releaseからレーベルを取得する"""

        label_info = release.get("label-info", [])

        if not label_info:
            return None

        label = label_info[0].get("label")

        if not label:
            return None

        return label.get("name")

    def get_cover_art_url(self, release_id):
        """
        Release IDからジャケット画像URLを取得する。
        """

        if not release_id:
            return ""

        return (
            f"https://coverartarchive.org/release/"
            f"{release_id}/front-500"
        )
