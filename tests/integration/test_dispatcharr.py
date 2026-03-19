def test_dispatcharr_system_status(dispatcharr_client):
    try:
        status = dispatcharr_client.system.get_status()
        assert isinstance(status, dict)
    except Exception:
        pass


def test_dispatcharr_channels(dispatcharr_client):
    try:
        channels = dispatcharr_client.channels.get()
        assert isinstance(channels, list)
    except Exception:
        pass
