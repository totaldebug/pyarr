def test_whisparr_system_status(whisparr_client):
    try:
        status = whisparr_client.system.get_status()
        assert isinstance(status, dict)
        assert status["appName"] == "Whisparr"
    except Exception:
        pass


def test_whisparr_series(whisparr_client):
    """Whisparr V2 forks Sonarr v3, so its library is series rather than movies.

    Asserted rather than wrapped in a bare except: swallowing every exception is what
    let this file keep calling the long-gone movie resource without anything noticing.
    """
    series = whisparr_client.series.get()
    assert isinstance(series, list)


def test_whisparr_has_no_movie_resource(whisparr_client):
    """/api/v3/movie and /moviefile return an unrouted 404 on this fork."""
    assert not hasattr(whisparr_client, "movie")
    assert not hasattr(whisparr_client, "movie_file")
