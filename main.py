import os
import sys
import time
import logging

from yt_dlp import YoutubeDL
from slugify import slugify
from googleapiclient.discovery import build

API_KEY = os.environ.get('API_KEY', '')
PLAYLIST_ID = os.environ.get('PLAYLIST_ID', '')
DOWNLOAD_PATH = os.environ.get('DOWNLOAD_PATH', '/app/downloads/')
CHECK_INTERVAL = 60 * int(os.environ.get("CHECK_INTERVAL", "30"))
DEFAULT_EXTENSION = 'mp4'
YOUTUBE_URL = 'https://www.youtube.com/watch?v='

logging.basicConfig(
  stream=sys.stdout,
  format="%(levelname)s %(asctime)s - %(message)s",
  level=int(os.environ.get("LOG_LEVEL", str(logging.INFO))),
)

logger = logging.getLogger()

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_videos_details(playlist_id = PLAYLIST_ID) -> dict:
  playlist_items = []
  next_page_token = None

  while True:
    request = youtube.playlistItems().list(
      part='snippet',
      playlistId=playlist_id,
      maxResults=50,
      pageToken=next_page_token
    )
    response = request.execute()

    page_items = response['items'] if 'items' in response else []

    for item in page_items:
      video_id = item['snippet']['resourceId']['videoId']
      slugified_title = slugify(item['snippet']['title'])

      filename = '{}{}.{}.{}'.format(DOWNLOAD_PATH, slugified_title, video_id, DEFAULT_EXTENSION)

      if not os.path.exists(filename):
        playlist_items.append({
          'originalTitle': item['snippet']['title'],
          'slugifiedTitle': slugified_title,
          'videoId': video_id,
          'link': YOUTUBE_URL + video_id,
          'filename': filename
        })

    next_page_token = response.get('nextPageToken')

    if not next_page_token:
      break

  return playlist_items

logger.info('process started, check interval is ' + str(CHECK_INTERVAL) + 's')

while True:
  videos = get_videos_details()

  for video_info in videos:
    ydl_opts = {
      'quiet': True,
      'format': DEFAULT_EXTENSION,
      'outtmpl': '{}{}.{}.%(ext)s'.format(
        DOWNLOAD_PATH,
        video_info['slugifiedTitle'],
        video_info['videoId'],
      ),
    }

    with YoutubeDL(ydl_opts) as ydl:
      error_code = ydl.download([video_info['link']])

      if error_code != 0:
        logger.error('failed to download ' + video_info['originalTitle'])

  time.sleep(CHECK_INTERVAL)
