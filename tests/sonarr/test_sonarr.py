from unittest.mock import MagicMock, patch

from pyarr import Sonarr

from .. import SONARR_API_KEY


def test_sonarr_context_manager():
    with (
        patch.object(Sonarr, "__enter__", MagicMock(return_value="mocked_enter")) as mock_enter,
        patch.object(Sonarr, "__exit__", MagicMock(return_value=None)) as mock_exit,
    ):
        with Sonarr(host="localhost", api_key=SONARR_API_KEY, tls=False) as sonarr:
            # Verify that __enter__ was called
            mock_enter.assert_called_once()
            # Check the return value of __enter__ if necessary
            assert sonarr == "mocked_enter"

        # Verify that __exit__ was called
        mock_exit.assert_called_once_with(None, None, None)
