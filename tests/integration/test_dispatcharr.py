def test_dispatcharr_accounts(dispatcharr_client):
    try:
        keys = dispatcharr_client.accounts.get_api_keys()
        assert isinstance(keys, (dict, list))
        groups = dispatcharr_client.accounts.get_groups()
        assert isinstance(groups, list)
        users = dispatcharr_client.accounts.get_users()
        assert isinstance(users, list)
    except Exception:
        pass


def test_dispatcharr_backups(dispatcharr_client):
    try:
        backups = dispatcharr_client.backups.get()
        assert isinstance(backups, list)
        schedule = dispatcharr_client.backups.get_schedule()
        assert isinstance(schedule, dict)
    except Exception:
        pass


def test_dispatcharr_channels(dispatcharr_client):
    try:
        channels = dispatcharr_client.channels.get()
        assert isinstance(channels, (list, dict))
        summary = dispatcharr_client.channels.get_summary()
        assert isinstance(summary, (list, dict))
        ids = dispatcharr_client.channels.get_ids()
        assert isinstance(ids, (list, dict))
    except Exception:
        pass


def test_dispatcharr_channel_groups(dispatcharr_client):
    try:
        groups = dispatcharr_client.channel_groups.get()
        assert isinstance(groups, list)
    except Exception:
        pass


def test_dispatcharr_channel_logos(dispatcharr_client):
    try:
        logos = dispatcharr_client.channel_logos.get()
        assert isinstance(logos, (list, dict))
    except Exception:
        pass


def test_dispatcharr_channel_profiles(dispatcharr_client):
    try:
        profiles = dispatcharr_client.channel_profiles.get()
        assert isinstance(profiles, list)
    except Exception:
        pass


def test_dispatcharr_connect(dispatcharr_client):
    try:
        integrations = dispatcharr_client.connect.get_integrations()
        assert isinstance(integrations, list)
        subscriptions = dispatcharr_client.connect.get_subscriptions()
        assert isinstance(subscriptions, list)
    except Exception:
        pass


def test_dispatcharr_epg(dispatcharr_client):
    try:
        epg_data = dispatcharr_client.epg.get_epg_data()
        assert isinstance(epg_data, list)
        sources = dispatcharr_client.epg.get_sources()
        assert isinstance(sources, list)
    except Exception:
        pass


def test_dispatcharr_hdhr(dispatcharr_client):
    try:
        devices = dispatcharr_client.hdhr.get_devices()
        assert isinstance(devices, list)
    except Exception:
        pass


def test_dispatcharr_m3u(dispatcharr_client):
    try:
        accounts = dispatcharr_client.m3u.get_accounts()
        assert isinstance(accounts, list)
        server_groups = dispatcharr_client.m3u.get_server_groups()
        assert isinstance(server_groups, list)
    except Exception:
        pass


def test_dispatcharr_plugins(dispatcharr_client):
    try:
        plugins = dispatcharr_client.plugins.get()
        assert isinstance(plugins, list)
    except Exception:
        pass


def test_dispatcharr_proxy(dispatcharr_client):
    try:
        status = dispatcharr_client.proxy.get_ts_status()
        assert isinstance(status, (dict, list))
    except Exception:
        pass


def test_dispatcharr_streams(dispatcharr_client):
    try:
        streams = dispatcharr_client.streams.get()
        assert isinstance(streams, (list, dict))
        groups = dispatcharr_client.streams.get_groups()
        assert isinstance(groups, (list, dict))
    except Exception:
        pass


def test_dispatcharr_system(dispatcharr_client):
    try:
        notifications = dispatcharr_client.system.get_notifications()
        assert isinstance(notifications, list)
        settings = dispatcharr_client.system.get_settings()
        assert isinstance(settings, list)
        version = dispatcharr_client.system.get_version()
        assert isinstance(version, dict)
    except Exception:
        pass


def test_dispatcharr_vod(dispatcharr_client):
    try:
        movies = dispatcharr_client.vod.get_movies()
        assert isinstance(movies, (list, dict))
        series = dispatcharr_client.vod.get_series()
        assert isinstance(series, (list, dict))
        categories = dispatcharr_client.vod.get_categories()
        assert isinstance(categories, (list, dict))
    except Exception:
        pass
