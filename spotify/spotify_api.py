import requests
import time
from .config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, logger

def get_spotify_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    })
    auth_response_data = auth_response.json()
    if 'access_token' in auth_response_data:
        logger.info("Spotify token acquired successfully.")
        return auth_response_data['access_token']
    else:
        logger.error("Error acquiring Spotify token.")
        raise Exception("Could not get Spotify token")

def fetch_data(endpoint, headers, params=None):
    while True:
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 1))
            logger.warning(f"Rate limit exceeded. Retrying in {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            logger.error(f"Error fetching data from {endpoint}: {response.status_code}")
            response.raise_for_status()

def get_playlist_id_by_name(playlist_name, headers):
    endpoint = 'https://api.spotify.com/v1/search'
    params = {'q': playlist_name, 'type': 'playlist', 'limit': 1}
    data = fetch_data(endpoint, headers, params)
    if data['playlists']['items']:
        playlist_id = data['playlists']['items'][0]['id']
        logger.info(f"Playlist '{playlist_name}' found with ID: {playlist_id}")
        return playlist_id
    else:
        logger.error(f"Playlist '{playlist_name}' not found.")
        raise Exception(f"Playlist '{playlist_name}' not found.")

def get_playlist_tracks(playlist_id, headers):
    endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    tracks = []
    params = {'limit': 100, 'offset': 0}
    while True:
        response = fetch_data(endpoint, headers, params)
        tracks.extend(response['items'])
        if response['next']:
            params['offset'] += 100
        else:
            break
    logger.info(f"Fetched {len(tracks)} tracks from playlist.")
    return tracks

def get_artist_data(artist_id, headers):
    endpoint = f'https://api.spotify.com/v1/artists/{artist_id}'
    return fetch_data(endpoint, headers)

def get_top_tracks(artist_id, headers, country='US'):
    endpoint = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks'
    params = {'country': country}
    return fetch_data(endpoint, headers, params)['tracks']

def get_related_artists(artist_id, headers):
    endpoint = f'https://api.spotify.com/v1/artists/{artist_id}/related-artists'
    return fetch_data(endpoint, headers)['artists']

def get_audio_features(track_ids, headers):
    endpoint = 'https://api.spotify.com/v1/audio-features'
    params = {'ids': ','.join(track_ids)}
    response = fetch_data(endpoint, headers, params)
    return response['audio_features']

def get_tracks_data(track_ids, headers):
    endpoint = 'https://api.spotify.com/v1/tracks'
    params = {'ids': ','.join(track_ids)}
    response = fetch_data(endpoint, headers, params)
    return response['tracks']
