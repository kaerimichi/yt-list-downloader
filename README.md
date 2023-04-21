# yt-list-downloader

Download YouTube videos from a playlist using `yt-dlp`.

## Requirements

- python >= 3.10
- pipenv
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Installation

```
pipenv install
```

## Usage

```
pipenv run main
INFO 2023-04-21 01:13:49,632 - process started, check interval is 600s
INFO 2023-04-21 01:13:50,038 - downloading "Why Windows Still Has The Old Control Panel"
```

This will start a process that will monitor the playlist (`PLAYLIST_ID`) and download the videos to a folder (`DOWNLOAD_PATH`). Existing videos on the download directory won't be downloaded again (a filename check is performed).

### Configuration

| Variable            | Description                                                                                    | Default Value   | Required |
|---------------------|------------------------------------------------------------------------------------------------|-----------------|----------|
| API_KEY             | The API key for YouTube API v3                                                                 | -               | Yes      |
| PLAYLIST_ID         | YouTube's playlist ID                                                                          | -               | Yes      |
| DOWNLOAD_PATH       | The path where the MP4 files will downloaded                                                   | /app/downloads/ | No       |
| DEFAULT\_FORMAT\_ID | Format code (see [yt-dlp format selection](https://github.com/yt-dlp/yt-dlp#format-selection)) | 22              | No       |
| CHECK_INTERVAL      | The number of minutes to check the playlist for updates                                        | 30              | No       |
| LOG_LEVEL           | The log level for the application                                                              | 20 (Info)       | No       |