from spotify.spotify_api import get_spotify_token
from spotify.data_processing import (
    process_playlist,
    gather_artist_details,
    gather_song_details,
    gather_audio_features
)
from spotify.utils import save_to_json, create_directory, json_to_csv, upload_file_to_s3
from spotify.config import logger, AWS_S3_BUCKET_NAME

def main():
    token = get_spotify_token()
    headers = {'Authorization': f'Bearer {token}'}

    # List of playlist names
    playlist_names = [
        "Today's Top Hits",
        "RapCaviar"
    ]
    
    all_tracks = []
    all_artist_ids = set()
    all_track_ids = []
    all_artists = {}
    all_top_tracks = {}
    all_related_artists = {}
    all_audio_features = []
    all_songs = []
    all_top_track_ids = []

    for playlist_name in playlist_names:
        logger.info(f"Processing playlist: {playlist_name}")
        process_playlist(playlist_name, headers, all_tracks, all_artist_ids, all_track_ids)

    gather_artist_details(all_artist_ids, headers, all_artists, all_top_tracks, all_related_artists, all_top_track_ids)
    gather_song_details(all_track_ids + all_top_track_ids, headers, all_songs)
    gather_audio_features(all_track_ids + all_top_track_ids, headers, all_audio_features)

    # Create raw_json_data and raw_csv_data directories if they don't exist
    create_directory('raw_json_data')
    create_directory('raw_csv_data')

    # Dictionary to map file names to data
    file_data_mapping = {
        'playlist_tracks': all_tracks,
        'artists': list(all_artists.values()),
        'audio_features': all_audio_features,
        'songs': all_songs,
        'top_tracks': all_top_tracks,
        'related_artists': all_related_artists,
    }

    # Save data to JSON files, convert to CSV, and upload to S3
    for file_name, data in file_data_mapping.items():
        json_file_path = f'raw_json_data/{file_name}.json'
        csv_file_path = f'raw_csv_data/{file_name}.csv'
        s3_key = f'json/{file_name}.json'

        logger.info(f"Saving data to {json_file_path}")
        save_to_json(data, json_file_path)

        logger.info(f"Converting {json_file_path} to {csv_file_path}")
        json_to_csv(json_file_path, csv_file_path)

        logger.info(f"Uploading {json_file_path} to S3 bucket {AWS_S3_BUCKET_NAME}")
        upload_file_to_s3(json_file_path, AWS_S3_BUCKET_NAME, s3_key)

    logger.info("Data extraction, conversion, and upload completed.")

if __name__ == '__main__':
    main()
