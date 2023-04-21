import os
import sys
import time
import logging
import subprocess

from slugify import slugify
from googleapiclient.discovery import build

API_KEY = os.environ.get('API_KEY', '')
PLAYLIST_ID = os.environ.get('PLAYLIST_ID', '')
DOWNLOAD_PATH = os.environ.get('DOWNLOAD_PATH', './downloads/')
DEFAULT_FORMAT_ID = os.environ.get('DEFAULT_FORMAT_ID', '22')
CHECK_INTERVAL = 60 * int(os.environ.get("CHECK_INTERVAL", "30"))
DEFAULT_EXTENSION = '.mp4'

logging.basicConfig(
  stream=sys.stdout,
  format="%(levelname)s %(asctime)s - %(message)s",
  level=int(os.environ.get("LOG_LEVEL", str(logging.INFO))),
)

logger = logging.getLogger()

youtube = build('youtube', 'v3', developerKey=API_KEY)

def download_video(video_id, video_title):
  filename = DOWNLOAD_PATH + '/' + slugify(video_title) + '.' + video_id + DEFAULT_EXTENSION

  if not os.path.exists(filename):
    logger.info(f"downloading \"{item['snippet']['title']}\"")

    dlcmd = [ 'yt-dlp', 'https://www.youtube.com/watch?v=' + video_id, '-f', DEFAULT_FORMAT_ID, '-o', filename ]

    result = subprocess.run(dlcmd, stdout=subprocess.PIPE)
    result.check_returncode()

def get_playlist_items():
  playlist_items = []
  next_page_token = None

  while True:
    request = youtube.playlistItems().list(
      part='snippet',
      playlistId=PLAYLIST_ID,
      maxResults=50,
      pageToken=next_page_token
    )
    response = request.execute()

    playlist_items += response['items']
    next_page_token = response.get('nextPageToken')

    if not next_page_token:
      break

  return playlist_items

logger.info('process started, check interval is ' + str(CHECK_INTERVAL) + 's')

while True:
  playlist_items = get_playlist_items()

  for item in playlist_items:
    download_video(item['snippet']['resourceId']['videoId'], item['snippet']['title'])

  time.sleep(CHECK_INTERVAL)
