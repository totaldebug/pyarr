from pyarr import Bazarr


def test_bazarr_system_status(bazarr_client: Bazarr):
    status = bazarr_client.system.get_status()
    assert isinstance(status, dict)
    assert isinstance(status["data"], dict)


def test_bazarr_providers(bazarr_client: Bazarr):
    providers = bazarr_client.providers.get()
    assert isinstance(providers, dict)
    assert isinstance(providers["data"], list)


def test_bazarr_series(bazarr_client: Bazarr):
    series = bazarr_client.series.get()
    assert isinstance(series, dict)
    assert isinstance(series["data"], list)


def test_bazarr_movies(bazarr_client: Bazarr):
    movies = bazarr_client.movies.get()
    assert isinstance(movies, dict)
    assert isinstance(movies["data"], list)


def test_bazarr_episodes(bazarr_client: Bazarr):
    episodes = bazarr_client.episodes.get(series_id=[1, 2])
    assert isinstance(episodes, dict)
    assert isinstance(episodes["data"], list)
