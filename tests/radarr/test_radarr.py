# def test_radarr_context_manager():
#    with patch.object(Radarr, '__enter__', MagicMock(return_value='mocked_enter')) as mock_enter, \
#         patch.object(Radarr, '__exit__', MagicMock(return_value=None)) as mock_exit:
#
#        with Radarr(host="localhost", api_key=READARR_API_KEY, tls=False) as radarr:
#            # Verify that __enter__ was called
#            mock_enter.assert_called_once()
#            # Check the return value of __enter__ if necessary
#            assert radarr == 'mocked_enter'
#
#        # Verify that __exit__ was called
#        mock_exit.assert_called_once_with(None, None, None)
#
