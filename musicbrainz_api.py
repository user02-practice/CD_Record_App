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

    def search_artist(self, artist_name):
        """
        アーティスト名でMusicBrainzを検索する。

        Args:
            artist_name (str):
                検索するアーティスト名。

        Returns:
            dict:
                MusicBrainz APIから取得した検索結果。
        """

        url = "https://musicbrainz.org/ws/2/artist/"

        params = {
            "query": f"artist:{artist_name}",
            "fmt": "json",
            "limit": 20
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

    def search_release_group(self, release_group_name):
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
            "limit": 20
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
            "fmt": "json"
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
            "limit": 20
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
                発売日と国。
        """

        return {
            "release_date": release["date"],
            "country": release["country"]
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