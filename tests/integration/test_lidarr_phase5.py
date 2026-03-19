def test_lidarr_artist(lidarr_client):
    root_folders = lidarr_client.root_folder.get()
    if not root_folders:
        lidarr_client.root_folder.add(
            path="/config",
            name="config",
            default_quality_profile_id=1,
            default_metadata_profile_id=1,
        )
        root_folders = lidarr_client.root_folder.get()

    artists = lidarr_client.artist.get()
    if not artists:
        # Add an artist for testing (Metallica)
        lookup = lidarr_client.artist.lookup(term="lidarr:65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab")
        lidarr_client.artist.add(
            artist=lookup[0],
            root_dir=root_folders[0]["path"],
            quality_profile_id=1,
            metadata_profile_id=1,
        )
        artists = lidarr_client.artist.get()

    artist_id = artists[0]["id"]
    artist = lidarr_client.artist.get(item_id=artist_id)
    assert isinstance(artist, dict)
    assert artist["id"] == artist_id


def test_lidarr_album(lidarr_client):
    artists = lidarr_client.artist.get()
    if artists:
        artist_id = artists[0]["id"]
        albums = lidarr_client.album.get(artist_id=artist_id)
        assert isinstance(albums, list)


def test_lidarr_track(lidarr_client):
    artists = lidarr_client.artist.get()
    if artists:
        artist_id = artists[0]["id"]
        tracks = lidarr_client.track.get(artist_id=artist_id)
        assert isinstance(tracks, list)


def test_lidarr_track_file(lidarr_client):
    artists = lidarr_client.artist.get()
    if artists:
        artist_id = artists[0]["id"]
        files = lidarr_client.track_file.get(artist_id=artist_id)
        assert isinstance(files, list)


def test_lidarr_release(lidarr_client):
    artists = lidarr_client.artist.get()
    if artists:
        releases = lidarr_client.release.get(artist_id=artists[0]["id"])
        assert isinstance(releases, list)


def test_lidarr_manual_import(lidarr_client):
    imports = lidarr_client.manual_import.get(folder="/config")
    assert isinstance(imports, list)
