import contextlib

import pytest

from pyarr.exceptions import (
    PyarrMissingArgument,
    PyarrMissingProfile,
    PyarrResourceNotFound,
)
from pyarr.models.common import PyarrSortDirection
from pyarr.models.readarr import (
    ReadarrAuthorMonitor,
    ReadarrBookTypes,
    ReadarrCommands,
    ReadarrSortKeys,
)

from tests import load_fixture


@pytest.mark.usefixtures
def test_lookup(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/search?term=goodreads%3A123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.lookup(term="goodreads:123456")
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_lookup_book(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/book/lookup?term=goodreads%3A123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/lookup_book.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.lookup_book(term="goodreads:123456")
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_lookup_author(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/author/lookup?term=j.k. rowling",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/lookup_author.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.lookup_author(term="j.k. rowling")
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test__book_json(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/book/lookup?term=goodreads%3A123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/lookup_book.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/book/lookup?term=asin%3A123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/lookup_book.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/book/lookup?term=isbn%3A123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/lookup_book.json"),
        status=200,
        match_querystring=True,
    )

    data = readarr_client._book_json(
        id_="123456",
        book_id_type=ReadarrBookTypes.GOODREADS,
        root_dir="/",
        quality_profile_id=1,
        metadata_profile_id=1,
        monitored=False,
        search_for_new_book=True,
        author_monitor=ReadarrAuthorMonitor.EXISTING,
        author_search_for_missing_books=False,
    )
    assert isinstance(data, dict)
    assert data["author"]["metadataProfileId"] == 1
    assert data["author"]["qualityProfileId"] == 1
    assert data["author"]["rootFolderPath"] == "/"
    assert data["author"]["addOptions"]["monitor"] == "existing"
    assert data["author"]["addOptions"]["searchForMissingBooks"] == False
    assert data["monitored"] == False
    assert data["author"]["manualAdd"] == True
    assert data["addOptions"]["searchForNewBook"] == True

    data = readarr_client._book_json(
        id_="123456",
        book_id_type=ReadarrBookTypes.ASIN,
        root_dir="/",
        quality_profile_id=1,
        metadata_profile_id=1,
        monitored=False,
        search_for_new_book=True,
        author_monitor=ReadarrAuthorMonitor.EXISTING,
        author_search_for_missing_books=False,
    )
    assert isinstance(data, dict)

    data = readarr_client._book_json(
        id_="123456",
        book_id_type=ReadarrBookTypes.ISBN,
        root_dir="/",
        quality_profile_id=1,
        metadata_profile_id=1,
        monitored=False,
        search_for_new_book=True,
        author_monitor=ReadarrAuthorMonitor.EXISTING,
        author_search_for_missing_books=False,
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test__book_json_2(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/qualityprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/metadataprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    with contextlib.suppress(PyarrMissingProfile):
        data = readarr_client._book_json(
            id_="123456", book_id_type=ReadarrBookTypes.ISBN, root_dir="/"
        )
        assert False

    with contextlib.suppress(PyarrMissingProfile):
        data = readarr_client._book_json(
            id_="123456",
            book_id_type=ReadarrBookTypes.ISBN,
            root_dir="/",
            quality_profile_id=1,
        )
        assert False


@pytest.mark.usefixtures
def test__author_json(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/author/lookup?term=J.K.+Rowling",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/lookup_author.json"),
        status=200,
        match_querystring=True,
    )

    data = readarr_client._author_json(
        term="J.K. Rowling",
        root_dir="/",
        quality_profile_id=1,
        metadata_profile_id=1,
        monitored=False,
        author_monitor=ReadarrAuthorMonitor.EXISTING,
        search_for_missing_books=False,
    )
    assert isinstance(data, dict)
    assert data["metadataProfileId"] == 1
    assert data["qualityProfileId"] == 1
    assert data["rootFolderPath"] == "/"
    assert data["addOptions"]["monitor"] == "existing"
    assert data["addOptions"]["searchForMissingBooks"] == False
    assert data["monitored"] == False


@pytest.mark.usefixtures
def test__author_json_2(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/qualityprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/metadataprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    with contextlib.suppress(PyarrMissingProfile):
        data = readarr_client._author_json(term="J.K. Rowling", root_dir="/")
        assert False

    with contextlib.suppress(PyarrMissingProfile):
        data = readarr_client._author_json(
            term="J.K. Rowling",
            root_dir="/",
            quality_profile_id=1,
        )
        assert False


@pytest.mark.usefixtures
def test_get_command(responses, readarr_client):

    # No args
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/command",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/command_all.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.get_command()
    assert isinstance(data, list)

    # When an ID is supplied
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/command/4327826",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/command.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.get_command(4327826)
    assert isinstance(data, dict)

    # when an incorrect ID is supplied, not found response
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/command/4321",
        headers={"Content-Type": "application/json"},
        status=404,
        match_querystring=True,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = readarr_client.get_command(4321)
        assert False


@pytest.mark.usefixtures
def test_post_command(responses, readarr_client):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8787/api/v1/command",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/command.json"),
        status=201,
        match_querystring=True,
    )

    data = readarr_client.post_command(name=ReadarrCommands.APP_UPDATE_CHECK)
    assert isinstance(data, dict)
    data = readarr_client.post_command(ReadarrCommands.AUTHOR_SEARCH, authorId=1)
    assert isinstance(data, dict)
    data = readarr_client.post_command(ReadarrCommands.BOOK_SEARCH, bookId=1)
    assert isinstance(data, dict)
    data = readarr_client.post_command(ReadarrCommands.REFRESH_AUTHOR, authorId=1)
    assert isinstance(data, dict)
    data = readarr_client.post_command(ReadarrCommands.REFRESH_BOOK, bookId=1)
    assert isinstance(data, dict)
    data = readarr_client.post_command(
        ReadarrCommands.RENAME_AUTHOR, authorIds=[1, 2, 3]
    )
    assert isinstance(data, dict)
    data = readarr_client.post_command(ReadarrCommands.RESCAN_FOLDERS)
    assert isinstance(data, dict)
    data = readarr_client.post_command(ReadarrCommands.RSS_SYNC)
    assert isinstance(data, dict)
    data = readarr_client.post_command(ReadarrCommands.BACKUP)
    assert isinstance(data, dict)
    data = readarr_client.post_command(ReadarrCommands.MISSING_BOOK_SEARCH)
    assert isinstance(data, dict)
    data = readarr_client.post_command(ReadarrCommands.RENAME_FILES, authorId=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_missing(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/wanted/missing",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/wanted_missing.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.get_missing()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/wanted/missing?page=2&pageSize=20&sortKey=Books.Id&sortDirection=ascending",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/wanted_missing.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.get_missing(
        page=2,
        page_size=20,
        sort_key=ReadarrSortKeys.BOOK_ID,
        sort_dir=PyarrSortDirection.ASC,
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = readarr_client.get_missing(sort_key=ReadarrSortKeys.TIMELEFT)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = readarr_client.get_missing(sort_dir=PyarrSortDirection.DEFAULT)
        assert False


@pytest.mark.usefixtures
def test_get_cutoff(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/wanted/cutoff",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/wanted_cutoff.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.get_cutoff()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/wanted/cutoff?page=2&pageSize=20&sortKey=Books.Id&sortDirection=ascending&monitored=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/wanted_cutoff.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.get_cutoff(
        page=2,
        page_size=20,
        sort_key=ReadarrSortKeys.BOOK_ID,
        sort_dir=PyarrSortDirection.ASC,
        monitored=True,
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = readarr_client.get_cutoff(sort_key=ReadarrSortKeys.TIMELEFT)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = readarr_client.get_cutoff(sort_dir=PyarrSortDirection.DEFAULT)
        assert False


@pytest.mark.usefixtures
def test_get_queue(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/queue",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/queue.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.get_queue()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/queue?page=2&pageSize=20&sortKey=Books.Id&sortDirection=ascending&includeUnknownAuthorItems=True&includeAuthor=True&includeBook=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/queue.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.get_queue(
        page=2,
        page_size=20,
        sort_key=ReadarrSortKeys.BOOK_ID,
        sort_dir=PyarrSortDirection.ASC,
        unknown_authors=True,
        include_author=True,
        include_book=True,
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = readarr_client.get_queue(sort_key=ReadarrSortKeys.TIMELEFT)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = readarr_client.get_queue(sort_dir=PyarrSortDirection.DEFAULT)
        assert False


@pytest.mark.usefixtures
def test_get_metadata_profile(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/metadataprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/metadataprofile_all.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.get_metadata_profile()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/metadataprofile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/metadataprofile.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.get_metadata_profile(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_delay_profile(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/delayprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/delayprofile_all.json"),
        status=200,
        match_querystring=True,
    )

    data = readarr_client.get_delay_profile()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/delayprofile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/delayprofile.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.get_delay_profile(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_release_profile(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/releaseprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/releaseprofile_all.json"),
        status=200,
        match_querystring=True,
    )

    data = readarr_client.get_release_profile()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/releaseprofile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/releaseprofile.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.get_release_profile(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_book(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/book",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/book_all.json"),
        status=200,
        match_querystring=True,
    )

    data = readarr_client.get_book()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/book/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/book.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.get_book(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_add_book(responses, readarr_client):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8787/api/v1/book",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/book.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/book/lookup?term=goodreads%3A123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/lookup_book.json"),
        status=200,
        match_querystring=True,
    )

    data = readarr_client.add_book(
        id_="123456",
        book_id_type=ReadarrBookTypes.GOODREADS,
        root_dir="/books/",
        quality_profile_id=1,
        metadata_profile_id=1,
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_add_book_2(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/qualityprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/metadataprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    with contextlib.suppress(PyarrMissingProfile):
        data = readarr_client.add_book(
            id_="123456", book_id_type=ReadarrBookTypes.ISBN, root_dir="/"
        )
        assert False

    with contextlib.suppress(PyarrMissingProfile):
        data = readarr_client.add_book(
            id_="123456",
            book_id_type=ReadarrBookTypes.ISBN,
            root_dir="/",
            quality_profile_id=1,
        )
        assert False


@pytest.mark.usefixtures
def test_upd_book(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/book/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/book.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.PUT,
        "https://127.0.0.1:8787/api/v1/book/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/book.json"),
        status=200,
        match_querystring=True,
    )
    book = readarr_client.get_book(id_=1)

    data = readarr_client.upd_book(id_=1, data=book)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_del_book(responses, readarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8787/api/v1/book/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.del_book(1)
    assert isinstance(data, dict)
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8787/api/v1/book/1?deleteFiles=True&addImportListExclusion=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.del_book(id_=1, delete_files=True, import_list_exclusion=True)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_author(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/author",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/author_all.json"),
        status=200,
        match_querystring=True,
    )

    data = readarr_client.get_author()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/author/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/author.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.get_author(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_add_author(responses, readarr_client):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8787/api/v1/author",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/author.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/author/lookup?term=J.k+Rowling",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/lookup_author.json"),
        status=200,
        match_querystring=True,
    )

    data = readarr_client.add_author(
        term="J.k Rowling",
        root_dir="/books/",
        quality_profile_id=1,
        metadata_profile_id=1,
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_add_author_2(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/qualityprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/metadataprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    with contextlib.suppress(PyarrMissingProfile):
        data = readarr_client.add_author(term="123456", root_dir="/")
        assert False

    with contextlib.suppress(PyarrMissingProfile):
        data = readarr_client.add_author(
            term="123456",
            root_dir="/",
            quality_profile_id=1,
        )
        assert False


@pytest.mark.usefixtures
def test_upd_author(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/author/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/author.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.PUT,
        "https://127.0.0.1:8787/api/v1/author/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/author.json"),
        status=200,
        match_querystring=True,
    )
    author = readarr_client.get_author(id_=1)

    data = readarr_client.upd_author(id_=1, data=author)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_del_author(responses, readarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8787/api/v1/author/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.del_author(1)
    assert isinstance(data, dict)
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8787/api/v1/author/1?deleteFiles=True&addImportListExclusion=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = readarr_client.del_author(
        id_=1, delete_files=True, import_list_exclusion=True
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_log_file(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/log/file",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/logfile_all.json"),
        status=200,
        match_querystring=True,
    )

    data = readarr_client.get_log_file()
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_add_root_folder(responses, readarr_client):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8787/api/v1/rootFolder",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/rootfolder.json"),
        status=201,
        match_querystring=True,
    )
    data = readarr_client.add_root_folder(
        name="test",
        path="/path/to/folder",
        default_quality_profile_id=1,
        default_metadata_profile_id=1,
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_metadata_provider(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/config/metadataProvider",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/metadataprovider.json"),
        status=200,
        match_querystring=True,
    )

    data = readarr_client.get_metadata_provider()
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_upd_metadata_provider(responses, readarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8787/api/v1/config/metadataProvider",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/metadataprovider.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.PUT,
        "https://127.0.0.1:8787/api/v1/config/metadataProvider",
        headers={"Content-Type": "application/json"},
        body=load_fixture("readarr/metadataprovider.json"),
        status=200,
        match_querystring=True,
    )
    provider = readarr_client.get_metadata_provider()
    data = readarr_client.upd_metadata_provider(data=provider)
    assert isinstance(data, dict)
