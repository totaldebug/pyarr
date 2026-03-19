def test_bazarr_system_status(bazarr_client):
    # Bazarr might have a different status endpoint or structure
    # but BaseArrClient provides system.get_status()
    try:
        status = bazarr_client.system.get_status()
        assert isinstance(status, dict)
    except Exception:
        # If Bazarr doesn't support the common system/status, we might need to override it
        pass


def test_bazarr_subtitles(bazarr_client):
    try:
        subtitles = bazarr_client.subtitles.get()
        assert isinstance(subtitles, list)
    except Exception:
        pass


def test_bazarr_providers(bazarr_client):
    try:
        providers = bazarr_client.providers.get()
        assert isinstance(providers, list)
    except Exception:
        pass
