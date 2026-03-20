from pyarr import Lidarr


def test_lidarr_artist(lidarr_client: Lidarr):
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

    # Update artist
    artist["monitored"] = not artist["monitored"]
    updated_artist = lidarr_client.artist.update(data=artist)
    assert updated_artist["monitored"] == artist["monitored"]


def test_lidarr_album(lidarr_client: Lidarr):
    artists = lidarr_client.artist.get()
    if not artists:
        test_lidarr_artist(lidarr_client)
        artists = lidarr_client.artist.get()

    artist_id = artists[0]["id"]
    albums = lidarr_client.album.get(artist_id=artist_id)
    assert isinstance(albums, list)
    assert len(albums) > 0

    album_id = albums[0]["id"]
    album = lidarr_client.album.get(item_id=album_id)
    assert isinstance(album, dict)
    assert album["id"] == album_id

    # Update album
    album["monitored"] = not album["monitored"]
    updated_album = lidarr_client.album.update(data=album)
    assert updated_album["monitored"] == album["monitored"]


def test_lidarr_track(lidarr_client: Lidarr):
    artists = lidarr_client.artist.get()
    if artists:
        artist_id = artists[0]["id"]
        tracks = lidarr_client.track.get(artist_id=artist_id)
        assert isinstance(tracks, list)


def test_lidarr_track_file(lidarr_client: Lidarr):
    artists = lidarr_client.artist.get()
    if artists:
        artist_id = artists[0]["id"]
        files = lidarr_client.track_file.get(artist_id=artist_id)
        assert isinstance(files, list)


def test_lidarr_release(lidarr_client: Lidarr):
    artists = lidarr_client.artist.get()
    if artists:
        releases = lidarr_client.release.get(artist_id=artists[0]["id"])
        assert isinstance(releases, list)


def test_lidarr_manual_import(lidarr_client: Lidarr):
    imports = lidarr_client.manual_import.get(folder="/config")
    assert isinstance(imports, list)
