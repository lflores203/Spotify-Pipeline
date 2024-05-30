from spotify.spotify_api import (
    get_playlist_id_by_name,
    get_playlist_tracks,
    get_artist_data,
    get_top_tracks,
    get_related_artists,
    get_audio_features,
    get_tracks_data
)
from spotify.config import logger

def process_playlist(playlist_name, headers, all_tracks, all_artist_ids, all_track_ids):
    try:
        playlist_id = get_playlist_id_by_name(playlist_name, headers)
    except Exception as e:
        logger.error(f"Failed to find playlist: {e}")
        return

    # Fetch playlist tracks
    logger.info(f"Fetching playlist tracks for '{playlist_name}'...")
    tracks = get_playlist_tracks(playlist_id, headers)
    
    if not tracks:
        logger.warning(f"No tracks found in the playlist '{playlist_name}'.")
        return
    
    # Collect track and artist IDs
    logger.info("Collecting track and artist IDs...")
    for track in tracks:
        if track['track']:
            track_id = track['track']['id']
            artist_id = track['track']['artists'][0]['id']
            all_track_ids.append(track_id)
            all_artist_ids.add(artist_id)
            # Add track with added_at information to all_tracks
            track['track']['added_at'] = track['added_at']
    
    all_tracks.extend(tracks)

def gather_artist_details(all_artist_ids, headers, all_artists, all_top_tracks, all_related_artists, all_top_track_ids):
    logger.info("Fetching artist details...")
    for artist_id in all_artist_ids:
        artist_data = get_artist_data(artist_id, headers)
        all_artists[artist_id] = artist_data

        top_tracks = get_top_tracks(artist_id, headers)
        all_top_tracks[artist_id] = top_tracks

        for track in top_tracks:
            all_top_track_ids.append(track['id'])

        related_artists = get_related_artists(artist_id, headers)
        all_related_artists[artist_id] = related_artists

def gather_song_details(all_track_ids, headers, all_songs):
    logger.info("Fetching song details...")
    for i in range(0, len(all_track_ids), 50):
        batch = all_track_ids[i:i+50]
        songs_batch = get_tracks_data(batch, headers)
        all_songs.extend(songs_batch)

def gather_audio_features(all_track_ids, headers, all_audio_features):
    logger.info("Fetching audio features...")
    for i in range(0, len(all_track_ids), 100):
        batch = all_track_ids[i:i+100]
        audio_features_batch = get_audio_features(batch, headers)
        all_audio_features.extend(audio_features_batch)
