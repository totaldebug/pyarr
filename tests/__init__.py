import pathlib
import xml.etree.ElementTree as ET


def _get_api_key(path: str) -> str:
    root = ET.parse(path).getroot()
    api_key_element = root.find("ApiKey")
    if api_key_element is not None and api_key_element.text is not None:
        return api_key_element.text
    return ""


MOCK_HOST = "127.0.0.1"
MOCK_API_KEY = "123456789abcdefg123456789"
SONARR_API_KEY = _get_api_key("tests/docker_configs/sonarr/config.xml")
RADARR_API_KEY = _get_api_key("tests/docker_configs/radarr/config.xml")
READARR_API_KEY = _get_api_key("tests/docker_configs/readarr/config.xml")
LIDARR_API_KEY = _get_api_key("tests/docker_configs/lidarr/config.xml")

RADARR_IMDB = "tt1213644"
RADARR_IMDB_LIST = ["tt0060666", "tt1316037"]
RADARR_TMDB = 129
RADARR_MOVIE_TERM = "Movie"

SONARR_TVDB = 305288

LIDARR_TERM = "Silvertin"
LIDARR_ARTIST_TERM = "Silvertin"
LIDARR_ALBUM_TERM = "Dawn"
LIDARR_MUSICBRAINZ_ARTIST_ID = "171a57fb-1a66-4094-8373-72c7d1b0c621"
LIDARR_MUSICBRAINZ_ALBUM_ID = "f3f61963-359d-4f2f-8fc6-63856ffbe070"

READARR_GOODREADS_ID = "489521"
READARR_ASIN_ID = "9780691017846"
READARR_ISBN_ID = "9780691017846"
READARR_AUTHOR_ID = "7182094"
READARR_AUTHOR_TERM = "Maurice Maeterlinck"


def load_fixture(filename) -> str:
    """Load a fixture."""
    return pathlib.Path(__file__).parent.joinpath("fixtures", filename).read_text(encoding="utf8")
