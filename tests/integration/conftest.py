import pytest

from pyarr import Bazarr, Dispatcharr, Lidarr, Prowlarr, Radarr, Readarr, Sonarr, Whisparr


@pytest.fixture
def sonarr_client():
    return Sonarr(
        host="localhost",
        api_key="da96fdd18ce147b79b54c2fdadb7e19a",
        port=8989,
        tls=False,
    )


@pytest.fixture
def radarr_client():
    return Radarr(
        host="localhost",
        api_key="6b95b67e9fd34417b002aada8bf5fa3e",
        port=7878,
        tls=False,
    )


@pytest.fixture
def lidarr_client():
    return Lidarr(
        host="localhost",
        api_key="f0b398ba17c04645bea28ca934d003e0",
        port=8686,
        tls=False,
    )


@pytest.fixture
def prowlarr_client():
    return Prowlarr(
        host="localhost",
        api_key="5f96fdd18ce147b79b54c2fdadb7e19a",
        port=9696,
        tls=False,
    )


@pytest.fixture
def bazarr_client():
    return Bazarr(
        host="localhost",
        api_key="fd98c55ede927c1c6637d80173b21ddd",
        port=6767,
        tls=False,
    )


@pytest.fixture
def whisparr_client():
    return Whisparr(
        host="localhost",
        api_key="da96fdd18ce147b79b54c2fdadb7e19a",
        port=6969,
        tls=False,
    )


@pytest.fixture
def dispatcharr_client():
    return Dispatcharr(
        host="localhost",
        api_key="9xXJVdkmKaRtczAfcbbm2XGlCvg6fSHZPeShQ1N8GSNczWBnNVO7a3KuF82t17uGl6aw1snO-bx4wafbshNC6g",
        port=9191,
        tls=False,
    )


@pytest.fixture
def readarr_client():
    return Readarr(
        host="localhost",
        api_key="ccad0c53c68247ac99616747407c185b",
        port=8787,
        tls=False,
    )
