from unittest.mock import MagicMock, patch

from pyarr import Readarr

from .. import READARR_API_KEY


def test_readarr_context_manager():
    with (
        patch.object(Readarr, "__enter__", MagicMock(return_value="mocked_enter")) as mock_enter,
        patch.object(Readarr, "__exit__", MagicMock(return_value=None)) as mock_exit,
    ):
        with Readarr(host="localhost", api_key=READARR_API_KEY, tls=False) as readarr:
            # Verify that __enter__ was called
            mock_enter.assert_called_once()
            # Check the return value of __enter__ if necessary
            assert readarr == "mocked_enter"

        # Verify that __exit__ was called
        mock_exit.assert_called_once_with(None, None, None)
