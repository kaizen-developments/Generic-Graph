import subprocess
from googleapiclient.discovery import build, Resource
from typing import List
import logging 

logging.basicConfig(level=logging.INFO)

def get_youtube_API_key():
    youtube_API_key_raw = subprocess.run(['/home/solteszistvan/scripts/access_tokens/youtube_API_key.py'], stdout=subprocess.PIPE)
    youtube_API_key = youtube_API_key_raw.stdout.decode('utf-8').strip()
    return youtube_API_key

def get_video_resources(username)->List[Resource]:
    youtube = build('youtube', 'v3', developerKey=get_youtube_API_key())

    # Get the channel's content details
    channel_request = youtube.channels().list(
        part='contentDetails',
        forUsername=username
    )
    channel_response = channel_request.execute()
    uploads_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Get the list of videos in the uploads playlist
    playlist_request = youtube.playlistItems().list(
        part='snippet',
        playlistId=uploads_id,
        maxResults=1  # Change this to get more videos
    )
    playlist_response = playlist_request.execute()

    # Extract the video IDs from the response
    video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_response['items']]

    # Get the video resources
    video_resources = []
    for video_id in video_ids:
        video_request = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_id
        )
        video_response = video_request.execute()
        video_resources.append(video_response['items'][0])
    
    assert (result_s_elements_are_videos := all([video_resource["kind"] == "youtube#video" for video_resource in video_resources])), "All resources returned must be youtube videos."
    logging.info(f"Returning {len(video_resources)} video resources with get_video_resources.")
    return video_resources