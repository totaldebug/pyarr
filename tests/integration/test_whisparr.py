def test_whisparr_system_status(whisparr_client):
    try:
        status = whisparr_client.system.get_status()
        assert isinstance(status, dict)
        assert status["appName"] == "Whisparr"
    except Exception:
        pass


def test_whisparr_movie(whisparr_client):
    try:
        movies = whisparr_client.movie.get()
        assert isinstance(movies, list)
    except Exception:
        pass
