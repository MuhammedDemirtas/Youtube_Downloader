# YouTube Mp4 & Mp3 Downloader

## Description
YouTube Video Downloader is a Python-based GUI application that allows users to download YouTube videos and audio in various formats and resolutions. It utilizes the `yt-dlp` library for video extraction and `tkinter` for the user interface.

## Features
- Fetch video details including title and thumbnail.
- Download videos in multiple resolutions and formats.
- Download high-quality audio in MP3 format.
- Support for multiple audio downloads at once.
- Progress bar to show download progress.

## Technologies Used
- Python
- Tkinter
- yt-dlp
- Pillow
- Requests
- Threading
- FFmpeg (for audio extraction)

## Installation
### Prerequisites
Ensure you have Python installed on your system. You also need to install FFmpeg for audio processing.

### Install Required Dependencies
```sh
pip install yt-dlp pillow requests
```

### Install FFmpeg (Required for Audio Extraction)
- **Windows:** Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) and add it to your system PATH.
- **Linux:** Install via package manager:
  ```sh
  sudo apt install ffmpeg
  ```
- **Mac:** Install via Homebrew:
  ```sh
  brew install ffmpeg
  ```

## Usage
1. Run the script:
   ```sh
   python youtube_downloader.py
   ```
2. Enter a YouTube video URL.
3. Click the **Fetch Video Info** button.
4. Select a resolution and download the video or choose to download the audio.
5. To download multiple audios, enter multiple URLs (one per line) and click **Multiple Download Audio (MP3)**.

## Screenshots
![Application Screenshot](screenshot.png)

## Developer
**M. Demirtaş**

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

