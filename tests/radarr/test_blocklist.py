from pyarr.radarr import Radarr


def test_radarr_blocklist(radarr_client: Radarr):
    # Get blocklist
    blocklist = radarr_client.blocklist.get()
    assert isinstance(blocklist, dict)
    assert "records" in blocklist
