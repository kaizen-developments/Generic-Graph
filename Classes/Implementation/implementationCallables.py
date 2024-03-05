import subprocess
from googleapiclient.discovery import build, Resource
from typing import List
import logging 
import pickle
from typeguard import typechecked

logging.basicConfig(level=logging.INFO)

import sys
import os

import inspect

class YoutubeVideo(object):
    def __init__(self, kind, etag, items, pageInfo):
        self.kind = kind
        self.etag = etag
        self.items = items
        self.pageInfo = pageInfo

def import_the_folder_n_steps_above(n: int) -> None:
    current_folder = os.path.abspath(os.path.dirname(__file__))
    steps = [".."] * n
    target_folder = os.path.abspath(os.path.join(current_folder, *steps))
    sys.path.insert(0, target_folder)
import_the_folder_n_steps_above(n=2)

from Classes.classModule_debugMessage import DebugMessage

def get_youtube_API_key():
    youtube_API_key_raw = subprocess.run(['/home/solteszistvan/scripts/access_tokens/youtube_API_key.py'], stdout=subprocess.PIPE)
    youtube_API_key = youtube_API_key_raw.stdout.decode('utf-8').strip()
    return youtube_API_key

@typechecked
def VideoResource(resource)->bool:
    pass

@typechecked
def get_videos_on_the_channel(username)->List[YoutubeVideo]:
    #Get the youtube resource
    youtube = build('youtube', 'v3', developerKey=get_youtube_API_key())
    logging.debug(DebugMessage.identityOfObject(module_or_className="implementationCallables", methodName="get_video_resources", linenumber=36, variableName="youtube", variable=youtube))
    # Get the channel's content details
    channel_request = youtube.channels().list(
        part='contentDetails',
        forUsername=username,
        maxResults=2
    )
    logging.debug(DebugMessage.identityOfObject(module_or_className="implementationCallables", methodName="get_videos_on_the_channel", linenumber=39, variableName="channel_request", variable=channel_request))
    channel_response = channel_request.execute()
    uploads_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Get the list of videos in the uploads playlist
    playlist_request = youtube.playlistItems().list(
        part='snippet',
        playlistId=uploads_id,
        maxResults=2  # Change this to get more videos
    )
    logging.debug(DebugMessage.identityOfObject(module_or_className=__name__, methodName="get_videos_on_the_channel", linenumber=49, variableName="playlist_request", variable=playlist_request))
    playlist_response = playlist_request.execute()
    logging.debug(DebugMessage.identityOfObject(module_or_className=__name__, methodName="get_videos_on_the_channel", linenumber=55, variableName="playlist_response", variable=playlist_response))

    # Extract the video IDs from the response
    video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_response['items']]
    logging.debug(DebugMessage.identityOfObject(module_or_className="implementationCallables", methodName="get_videos_on_the_channel", linenumber=66, variableName='video_ids', variable=video_ids))
    # Get the video resources
    videos = []
    for video_id in video_ids:
        video_request = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_id
        )
        executed_video_request = video_request.execute()
        youtube_playlist_items = executed_video_request['items']
        for index, video in enumerate(youtube_playlist_items):
            logging.debug(DebugMessage.identityOfObject(module_or_className="implementationCallables", methodName="get_videos_on_the_channel", linenumber=77, variableName="video", variable=video))
        logging.debug(DebugMessage.identityOfObject(module_or_className="implementationCallables", methodName="get_videos_on_the_channel", linenumber=84, variableName="executed_video_request().keys()", variable=executed_video_request.keys()))
        logging.debug(DebugMessage.identityOfObject(module_or_className="implementationCallables", methodName="get_videos_on_the_channel", linenumber=76, variableName=f"youtube_playlist_items[{index}]", variable=youtube_playlist_items[index]))
        video = YoutubeVideo(kind=executed_video_request['kind'], etag=executed_video_request['etag'], items=executed_video_request['items'], pageInfo=executed_video_request['pageInfo'])
        logging.debug(DebugMessage.identityOfObject(module_or_className="implementationCallables", methodName="get_videos_on_the_channel", linenumber=73, variableName="video", variable=video))
        videos.append(video)
    
    #TODO: Fix assert (result_s_elements_are_videos := all([VideoResource(video_resource) for video_resource in video_resources])), "All resources returned must be youtube videos."
    logging.debug(f"Returning {len(videos)} videos with get_videos.")
    for index, video_resource in enumerate(videos):
        logging.debug(DebugMessage.identityOfObject(module_or_className="implementationCallables", methodName="get_videos_on_the_channel", linenumber=79, variableName=f"{index}th element of videos", variable=videos))#logIdentityOf_a_Variable snippet
    return videos