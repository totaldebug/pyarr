import contextlib

from pyarr import PyarrMissingArgument, Readarr


def test_readarr_get_history(readarr_client: Readarr):
    # Initialize the history object from Readarr client
    history = readarr_client.history

    # Call the get method with various parameters
    response = history.get(page=1, page_size=10, sort_key="eventType", sort_dir="ascending")

    # Perform assertions on the response
    assert isinstance(response, dict)  # Ensure response is a dictionary
    assert response["page"] == 1
    assert response["pageSize"] == 10
    assert response["sortDirection"] == "ascending"
    assert "records" in response  # Ensure 'items' key is present in the response
    assert isinstance(response["records"], list)  # Ensure 'items' is a list of items

    # Add more specific assertions based on your expected response format

    print(response)  # Print the response for inspection

    with contextlib.suppress(PyarrMissingArgument):
        response = history.get(sort_key="date")
        raise AssertionError("PyarrMissingArgument not raised")

    with contextlib.suppress(PyarrMissingArgument):
        response = history.get(sort_dir="descending")
        raise AssertionError("PyarrMissingArgument not raised")
