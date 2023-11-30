# Spotify Top Tracks Playlist Generator

This script utilizes the Spotipy library to interact with the Spotify API and create playlists of a user's top tracks for the last 6 months and the last month.
It requires valid Spotify API credentials and a username, which can be provided as environmental variables.

## Requirements

- Python 3.x
- [Spotipy Library](https://spotipy.readthedocs.io/)

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/spotify-top-artist-playlist-generator.git

# Install the required dependencies:
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python -m spotify_top_tracks_generator
```

If prompted, input your Spotify username.
The script will authenticate with the Spotify API and create or replace playlists with your top tracks for the specified time ranges.

## Configuration
Before running the script, make sure to set up your Spotify API credentials as environment variables in a .env file at the root of the project.
The required variables are:

```dotenv
# .env

SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_SECRET=your_client_secret
SPOTIFY_USERNAME=your_spotify_username
```

Make sure to adjust the values accordingly.
The REDIRECT_URI is already configured in the config.py file.

## Note

If running the script for the first time, it may prompt you to authorize access to your Spotify account.

## License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE.md) file for details.