import pathlib
import xml.etree.ElementTree as ET

MOCK_URL = "https://127.0.0.1"
MOCK_API_KEY = "123456789abcdefg123456789"
SONARR_API_KEY = (
    ET.parse("tests/docker_configs/sonarr/config.xml").getroot().find("ApiKey").text
)
RADARR_API_KEY = (
    ET.parse("tests/docker_configs/radarr/config.xml").getroot().find("ApiKey").text
)
READARR_API_KEY = (
    ET.parse("tests/docker_configs/readarr/config.xml").getroot().find("ApiKey").text
)
LIDARR_API_KEY = (
    ET.parse("tests/docker_configs/lidarr/config.xml").getroot().find("ApiKey").text
)

RADARR_IMDB = "tt1213644"
RADARR_IMDB_LIST = ["tt0060666", "tt1316037"]
RADARR_TMDB = 129
RADARR_MOVIE_TERM = "Movie"

SONARR_TVDB = 305288

LIDARR_TERM = "Silvertin"
LIDARR_ARTIST_TERM = "Silvertin"
LIDARR_ALBUM_TERM = "Dawn"
LIDARR_MUSICBRAINZ_ARTIST_ID = "a2324db2-9f11-41cf-bdef-4ccea8aae4bf"
LIDARR_MUSICBRAINZ_ALBUM_ID = "1dc4c347-a1db-32aa-b14f-bc9cc507b843"

READARR_GOODREADS_ID = "489521"
READARR_ASIN_ID = "9780691017846"
READARR_ISBN_ID = "9780691017846"
READARR_AUTHOR_ID = "7182094"
READARR_AUTHOR_TERM = "Maurice Maeterlinck"


def load_fixture(filename) -> str:
    """Load a fixture."""
    return (
        pathlib.Path(__file__)
        .parent.joinpath("fixtures", filename)
        .read_text(encoding="utf8")
    )
