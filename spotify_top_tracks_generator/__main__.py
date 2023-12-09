"""
Spotify Top Tracks Playlist Generator

Author: <slapelachie@gmail.com>

This script utilizes the Spotipy library to interact with the Spotify API and create playlists of a
user's top tracks for the last 6 months and the last month. It requires valid Spotify API
credentials and a username, which can be provided as environmental variables.

Usage:
1. Run the script.
2. If prompted, input your Spotify username.
3. The script will authenticate with the Spotify API and create or replace playlists with your top
   tracks for the specified time ranges.

Note: If running the script for the first time, it may prompt you to authorize access to your
Spotify account.
"""
import logging
from datetime import datetime
import spotipy
from spotify_top_tracks_generator.config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_SECRET,
    SPOTIFY_USERNAME,
    REDIRECT_URI,
)

SCOPE = ["user-top-read", "playlist-modify-public", "playlist-modify-private"]
TOP_SIX_MONTHS_PLAYLIST_NAME = "Top Songs - Last 6 Months"
TOP_MONTH_PLAYLIST_NAME = "Top Songs - Last Month"

logging.basicConfig(level=logging.INFO)


def get_top_tracks(spotify, time_range: str = "medium_term", limit: int = 50):
    """
    Retrieves the user's top tracks from Spotify based on the specified time range.

    Args:
        spotify: Spotify API client instance.
        time_range (str, optional): The time range for which to retrieve top tracks.
            Valid values: 'short_term', 'medium_term', 'long_term'. Default is 'medium_term'.
        limit (int, optional): The maximum number of top tracks to retrieve. Default is 50.

    Returns:
        list: A list of dictionaries containing information about the user's top tracks. Each
            dictionary represents a top track and includes details such as track name, artist,
            etc.

    Raises:
        ValueError: If an invalid time_range is provided.
    """
    valid_time_ranges = ["short_term", "medium_term", "long_term"]
    if time_range not in valid_time_ranges:
        raise ValueError(f"Invalid time_range. Please choose from {valid_time_ranges}")

    top_tracks_info = spotify.current_user_top_tracks(
        limit=limit, time_range=time_range
    )
    return top_tracks_info.get("items")


def create_playlist(spotify, name: str, description: str = ""):
    """
    Creates a new playlist on Spotify with the specified name.

    Args:
        spotify: Spotify API client instance.
        name (str): The name of the new playlist.

    Returns:
        str: The unique identifier (ID) of the newly created playlist.

    Raises:
        ValueError: If the playlist creation fails or the response does not contain the expected
            data.
    """
    try:
        new_playlist = spotify.user_playlist_create(
            SPOTIFY_USERNAME, name, description=description
        )
        playlist_id = new_playlist.get("id")
        if not playlist_id:
            raise ValueError(
                "Failed to retrieve playlist ID from the Spotify API response."
            )
        return playlist_id
    except Exception as e:
        raise ValueError(f"Failed to create playlist: {str(e)}") from e


def get_track_ids(tracks):
    """
    Extracts the unique identifiers (IDs) of tracks from a list of track dictionaries.

    Args:
        tracks (list): A list of dictionaries representing tracks, where each dictionary includes
            information about the track, such as its ID.

    Returns:
        list: A list of track IDs extracted from the input track dictionaries.
    """
    return [track.get("id") for track in tracks if track.get("id") is not None]


def get_user_playlists(spotify, limit: int = 50):
    """
    Retrieves the playlists created by the authenticated Spotify user.

    Args:
        spotify: Spotify API client instance.
        limit (int, optional): The maximum number of playlists to retrieve per request. Default is
            50.

    Returns:
        list: A list of dictionaries containing information about the user's playlists.
            Each dictionary represents a playlist and includes details such as name, ID, etc.
    """
    user_playlists = []
    offset = 0

    while True:
        playlists_info = spotify.current_user_playlists(offset=offset, limit=limit)
        user_playlists.extend(playlists_info.get("items", []))

        if not playlists_info.get("next"):
            break

        offset += limit

    return user_playlists


def get_playlist_id_by_name(playlists, name: str):
    """
    Retrieves the unique identifier (ID) of a playlist with the specified name.

    Args:
        playlists (list): A list of dictionaries representing playlists, where each dictionary
            includes information about the playlist, such as its name and ID.
        name (str): The name of the playlist to find.

    Returns:
        str or None: The ID of the playlist with the specified name, or None if no matching
            playlist is found in the provided list.
    """
    for playlist in playlists:
        if playlist.get("name", "") == name:
            return playlist.get("id")

    return None


def create_or_replace_playlist(spotify, playlists, playlist_name, track_ids):
    """
    Creates a new playlist or replaces the tracks of an existing playlist with the specified name.

    Args:
        spotify: Spotify API client instance.
        playlists (list): A list of dictionaries representing existing playlists.
        playlist_name (str): The name of the playlist to create or replace.
        track_ids (list): A list of track IDs to populate the playlist with.
    """
    existing_playlist_id = get_playlist_id_by_name(playlists, playlist_name)

    current_datetime = datetime.now()
    playlist_description = f"Generated: {current_datetime.strftime('%Y-%m-%d %H:%M')}"

    if existing_playlist_id:
        spotify.user_playlist_replace_tracks(
            SPOTIFY_USERNAME, existing_playlist_id, track_ids
        )
        spotify.playlist_change_details(
            existing_playlist_id, description=playlist_description
        )
    else:
        playlist_id = create_playlist(
            spotify, playlist_name, description=playlist_description
        )
        spotify.user_playlist_add_tracks(SPOTIFY_USERNAME, playlist_id, track_ids)


def get_spotify_token():
    """
    Retrieves the Spotify access token for the authenticated user.

    Returns:
        str or None: The Spotify access token if successful, otherwise None.
    """
    token = spotipy.util.prompt_for_user_token(
        SPOTIFY_USERNAME,
        scope=SCOPE,
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_SECRET,
        redirect_uri=REDIRECT_URI,
    )
    if not token:
        logging.error("Failed to retrieve Spotify token!")

    return token


def main():
    """
    Main function to run the Spotify playlist management.

    This function retrieves the user's Spotify token, fetches the user's playlists, gets the top
    tracks for the last six months and the last month, and creates or replaces playlists with
    these top tracks.
    """
    token = get_spotify_token()
    spotify = spotipy.Spotify(auth=token)

    user_playlists = get_user_playlists(spotify)

    top_six_month_tracks = get_top_tracks(spotify, "medium_term")
    top_six_month_track_ids = get_track_ids(top_six_month_tracks)
    create_or_replace_playlist(
        spotify, user_playlists, TOP_SIX_MONTHS_PLAYLIST_NAME, top_six_month_track_ids
    )

    top_month_tracks = get_top_tracks(spotify, "short_term")
    top_month_track_ids = get_track_ids(top_month_tracks)
    create_or_replace_playlist(
        spotify, user_playlists, TOP_MONTH_PLAYLIST_NAME, top_month_track_ids
    )


if __name__ == "__main__":
    if not SPOTIFY_USERNAME:
        SPOTIFY_USERNAME = input("Please input your Spotify username: ")

    main()
