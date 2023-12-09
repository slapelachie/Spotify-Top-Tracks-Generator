"""
Spotify API Credentials Configuration

Author: <slapelachie@gmail.com>

This script loads Spotify API credentials and a username from environmental variables using dotenv.
It is intended to be used to configure the Spotify API settings before running other scripts that
interact with the Spotify API.

Usage:
1. Create a `.env` file in the same directory as this script.
2. Add the following entries to the `.env` file:
   - SPOTIFY_CLIENT_ID: Spotify API client ID
   - SPOTIFY_SECRET: Spotify API client secret
   - SPOTIFY_USERNAME: Your Spotify username (optional, set to None if not applicable)
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Spotipy Settings
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET = os.getenv("SPOTIFY_SECRET")
SPOTIFY_USERNAME = os.getenv("SPOTIFY_USERNAME", None)
REDIRECT_URI = "http://localhost:8888/callback/"

# Playlist Names
TOP_SHORT_TERM_PLAYLIST_NAME = "Top Songs - Last Month"
TOP_MEDIUM_TERM_PLAYLIST_NAME = "Top Songs - Last 6 Months"
TOP_LONG_TERM_PLAYLIST_NAME = "Top Songs - All Time"

# Other Settings
DEFAULT_TIME_FRAMES = ["short_term", "medium_term"]
