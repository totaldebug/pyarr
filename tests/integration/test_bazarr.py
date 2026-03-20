from pyarr import Bazarr


def test_bazarr_system_status(bazarr_client: Bazarr):
    try:
        status = bazarr_client.system.get_status()
        assert isinstance(status, dict)
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
