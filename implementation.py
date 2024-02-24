import subprocess

from googleapiclient.discovery import build, Resource

from graph import Edge, Graph 

class Link(Edge):
    def __init__(self, source:str, target:str):
        self.source = source
        self.target = target
    
    def startNode(self):
        return self.source
    
    def endNode(self):
        return self.target

def get_youtube_API_key():
    youtube_API_key_raw = subprocess.run(['/home/solteszistvan/scripts/access_tokens/youtube_API_key.py'], stdout=subprocess.PIPE)
    youtube_API_key = youtube_API_key_raw.stdout.decode('utf-8').strip()
    return youtube_API_key
    
def get_video_resources(username):
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
        maxResults=50  # Change this to get more videos
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

    return video_resources

videoResources = get_video_resources('schafer5')

videoLinks = ["https://www.youtube.com/watch?v="+ video["id"] for video in videoResources]

print(videoLinks)