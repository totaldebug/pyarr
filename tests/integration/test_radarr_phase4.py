def test_radarr_movie(radarr_client):
    root_folders = radarr_client.root_folder.get()
    if not root_folders:
        radarr_client.root_folder.add(path="/config")
        root_folders = radarr_client.root_folder.get()

    movies = radarr_client.movie.get()
    if not movies:
        # Add a movie for testing (The Matrix)
        lookup = radarr_client.movie.lookup(term="tmdb:603")
        radarr_client.movie.add(movie=lookup[0], root_dir=root_folders[0]["path"], quality_profile_id=1)
        movies = radarr_client.movie.get()

    movie_id = movies[0]["id"]
    movie = radarr_client.movie.get(item_id=movie_id)
    assert isinstance(movie, dict)
    assert movie["id"] == movie_id


def test_radarr_movie_file(radarr_client):
    movies = radarr_client.movie.get()
    if movies:
        movie_id = movies[0]["id"]
        files = radarr_client.movie_file.get(movie_id=movie_id)
        assert isinstance(files, list)


def test_radarr_release(radarr_client):
    movies = radarr_client.movie.get()
    if movies:
        releases = radarr_client.release.get(movie_id=movies[0]["id"])
        assert isinstance(releases, list)


def test_radarr_manual_import(radarr_client):
    imports = radarr_client.manual_import.get(folder="/config")
    assert isinstance(imports, list)


def test_radarr_custom_filter(radarr_client):
    filters = radarr_client.custom_filter.get()
    assert isinstance(filters, list)
