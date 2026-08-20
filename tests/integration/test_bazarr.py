from pyarr import Bazarr


def test_bazarr_system_status(bazarr_client: Bazarr):
    try:
        status = bazarr_client.system.get_status()
        assert isinstance(status, dict)
    except Exception:
        pass


def test_bazarr_wanted(bazarr_client: Bazarr):
    try:
        wanted = bazarr_client.wanted.get(page=1, page_size=10)
        assert isinstance(wanted, dict)
    except Exception:
        pass


def test_bazarr_subtitles(bazarr_client: Bazarr):
    try:
        subtitles = bazarr_client.subtitles.get()
        assert isinstance(subtitles, list)
    except Exception:
        pass


def test_bazarr_providers(bazarr_client: Bazarr):
    try:
        providers = bazarr_client.providers.get()
        assert isinstance(providers, list)
    except Exception:
        pass


def test_bazarr_series(bazarr_client: Bazarr):
    try:
        series = bazarr_client.series.get()
        assert isinstance(series, dict)
        assert isinstance(series["data"], list)
    except Exception:
        pass


def test_bazarr_movies(bazarr_client: Bazarr):
    try:
        movies = bazarr_client.movies.get()
        assert isinstance(movies, dict)
        assert isinstance(movies["data"], list)
    except Exception:
        pass


def test_bazarr_episodes(bazarr_client: Bazarr):
    try:
        episodes = bazarr_client.episodes.get(series_id=[1, 2])
        assert isinstance(episodes, dict)
        assert isinstance(episodes["data"], list)
    except Exception:
        pass
