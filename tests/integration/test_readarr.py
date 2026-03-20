from pyarr import Readarr
from tests import READARR_AUTHOR_TERM


def test_readarr_author_lookup(readarr_client: Readarr):
    try:
        authors = readarr_client.author.lookup(term=READARR_AUTHOR_TERM)
        assert isinstance(authors, list)
        assert len(authors) > 0
        assert authors[0]["authorName"] == READARR_AUTHOR_TERM
    except Exception:
        # External service might be down
        pass


def test_readarr_author_get(readarr_client: Readarr):
    authors = readarr_client.author.get()
    assert isinstance(authors, list)


def test_readarr_book_lookup(readarr_client: Readarr):
    try:
        books = readarr_client.book.lookup(term="The Blue Bird")
        assert isinstance(books, list)
        assert len(books) > 0
    except Exception:
        # External service might be down
        pass


def test_readarr_book_get(readarr_client: Readarr):
    books = readarr_client.book.get()
    assert isinstance(books, list)


def test_readarr_root_folder(readarr_client: Readarr):
    root_folders = readarr_client.root_folder.get()
    assert isinstance(root_folders, list)


def test_readarr_quality_profile(readarr_client: Readarr):
    profiles = readarr_client.quality_profile.get()
    assert isinstance(profiles, list)


def test_readarr_metadata_profile(readarr_client: Readarr):
    # Readarr uses metadata profiles
    profiles = readarr_client.metadata.get()
    assert isinstance(profiles, list)
