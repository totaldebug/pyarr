from unittest.mock import AsyncMock

import pytest

from pyarr._async.common.config import Config, MediaConfig
from pyarr._async.utils.http import RequestHandler


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method", "section"),
    [
        ("get_host", "host"),
        ("get_ui", "ui"),
        ("get_download_client", "downloadclient"),
    ],
)
async def test_config_get_sections(method, section):
    """Every shared section reads from config/<section>."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {"id": 1}
    config = Config(mock_handler)

    response = await getattr(config, method)()

    assert response == {"id": 1}
    mock_handler.request.assert_called_with(f"config/{section}")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method", "section"),
    [
        ("update_host", "host"),
        ("update_ui", "ui"),
        ("update_download_client", "downloadclient"),
    ],
)
async def test_config_update_sections(method, section):
    """Every shared section writes with a PUT to the un-suffixed path."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {"id": 1}
    config = Config(mock_handler)

    response = await getattr(config, method)({"id": 1})

    assert response == {"id": 1}
    mock_handler.request.assert_called_with(f"config/{section}", method="PUT", json_data={"id": 1})


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method", "section"),
    [
        ("get_indexer", "indexer"),
        ("get_media_management", "mediamanagement"),
        ("get_naming", "naming"),
    ],
)
async def test_media_config_get_sections(method, section):
    """The media manager sections read from config/<section>."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {"id": 1}
    config = MediaConfig(mock_handler)

    await getattr(config, method)()

    mock_handler.request.assert_called_with(f"config/{section}")


@pytest.mark.asyncio
async def test_media_config_naming_examples():
    """Naming examples pass the preview format through as query parameters."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {"singleEpisodeExample": "..."}
    config = MediaConfig(mock_handler)

    await config.get_naming_examples()
    mock_handler.request.assert_called_with("config/naming/examples", params=None)

    await config.get_naming_examples({"standardEpisodeFormat": "{Series Title}"})
    mock_handler.request.assert_called_with(
        "config/naming/examples", params={"standardEpisodeFormat": "{Series Title}"}
    )


@pytest.mark.asyncio
async def test_config_rejects_non_dict_response():
    """A list response means the path was wrong, so it should not be returned as config."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = []
    config = Config(mock_handler)

    with pytest.raises(ValueError):
        await config.get_host()

    with pytest.raises(ValueError):
        await config.update_host({"id": 1})


@pytest.mark.asyncio
async def test_prowlarr_config_has_no_media_sections():
    """Prowlarr manages no media, so it must not advertise the media manager sections."""
    from pyarr._async.prowlarr.config import Config as ProwlarrConfig

    mock_handler = AsyncMock(spec=RequestHandler)
    config = ProwlarrConfig(mock_handler)

    assert not isinstance(config, MediaConfig)
    for absent in ("get_indexer", "get_media_management", "get_naming", "get_naming_examples"):
        assert not hasattr(config, absent), f"Prowlarr should not expose {absent}"

    assert hasattr(config, "get_host")
    assert hasattr(config, "get_development")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("module", "method", "section"),
    [
        ("pyarr._async.sonarr.config", "get_import_list", "importlist"),
        ("pyarr._async.radarr.config", "get_import_list", "importlist"),
        ("pyarr._async.radarr.config", "get_metadata", "metadata"),
        ("pyarr._async.lidarr.config", "get_metadata_provider", "metadataProvider"),
        ("pyarr._async.readarr.config", "get_metadata_provider", "metadataProvider"),
        ("pyarr._async.readarr.config", "get_development", "development"),
        ("pyarr._async.prowlarr.config", "get_development", "development"),
    ],
)
async def test_app_specific_config_sections(module, method, section):
    """Each application's extra sections target the path that application actually serves."""
    import importlib

    config_class = importlib.import_module(module).Config
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {"id": 1}
    config = config_class(mock_handler)

    await getattr(config, method)()

    mock_handler.request.assert_called_with(f"config/{section}")
