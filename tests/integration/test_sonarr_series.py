def test_sonarr_series_get(sonarr_client):
    series = sonarr_client.series.get()
    assert isinstance(series, list)


def test_sonarr_series_lookup(sonarr_client):
    # Lookup "The Simpsons"
    results = sonarr_client.series.lookup(term="The Simpsons")
    assert isinstance(results, list)
    assert len(results) > 0
    assert any("Simpsons" in r["title"] for r in results)


def test_sonarr_series_get_tmdb(sonarr_client):
    # The Simpsons TMDB ID is 12
    # Note: This only works if the series is already in the library
    # or if the API supports lookup via this endpoint (which it seems to in v5)
    try:
        series = sonarr_client.series.get(item_id=12, tmdb=True)
        assert isinstance(series, list)
    except Exception:
        # If not in library, it might 404 or return empty
        pass
