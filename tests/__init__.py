import pathlib

API_TOKEN = "1234567890abcdef1234567890abcdef"
HOST_URL = "https://127.0.0.1"


def load_fixture(filename) -> str:
    """Load a fixture."""
    return (
        pathlib.Path(__file__)
        .parent.joinpath("fixtures", filename)
        .read_text(encoding="utf8")
    )
