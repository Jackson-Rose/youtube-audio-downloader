# YouTube Audio Downloader

A Python program that downloads audio from YouTube videos and converts them to MP3 format using `yt-dlp`.

## Features

- ✅ Download audio from YouTube videos
- ✅ **Download entire YouTube playlists**
- ✅ Convert to high-quality MP3 format (192kbps)
- ✅ URL validation for YouTube links
- ✅ Command-line interface
- ✅ Custom output filenames and directories
- ✅ Video information display
- ✅ **Batch processing with progress tracking**
- ✅ **Configurable delays between downloads**
- ✅ **Playlist organization in subdirectories**
- ✅ Error handling and user-friendly messages

## Prerequisites

You need to have **FFmpeg** installed on your system for audio conversion:

### macOS
```bash
brew install ffmpeg
```

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

### Windows
Download from [FFmpeg official website](https://ffmpeg.org/download.html) or use chocolatey:
```bash
choco install ffmpeg
```

## Installation

### Quick Install
```bash
# Install from PyPI (when available)
pip install youtube-audio-downloader

# Or install from GitHub
pip install git+https://github.com/YOURUSERNAME/youtube-audio-downloader.git
```

### Manual Installation
1. Clone or download this repository
2. Install the package:
```bash
cd youtube-audio-downloader
pip install .
```

### Standalone Script
```bash
# Download and run directly
python3 youtube_audio_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Note:** The program uses `yt-dlp`'s built-in audio conversion, which eliminates dependency issues.

**For detailed installation instructions, see [INSTALL.md](INSTALL.md)**

### Prerequisites
- **Python 3.8+**
- **FFmpeg** (automatically detected)
  - **macOS**: `brew install ffmpeg`
  - **Ubuntu/Debian**: `sudo apt install ffmpeg`  
  - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

### Single Video Download

#### Basic Usage
```bash
python3 youtube_audio_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Custom Output Filename
```bash
python3 youtube_audio_downloader.py -o "my_song.mp3" "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Custom Output Directory
```bash
python3 youtube_audio_downloader.py -d "my_music_folder" "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Playlist Download

#### Download Entire Playlist
```bash
python3 youtube_audio_downloader.py --playlist "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

#### Download First N Videos from Playlist
```bash
python3 youtube_audio_downloader.py --playlist --max-videos 10 "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

#### Custom Delay Between Downloads
```bash
python3 youtube_audio_downloader.py --playlist --delay 2.5 "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

#### Playlist with All Options
```bash
python3 youtube_audio_downloader.py --playlist -d "my_playlists" --max-videos 20 --delay 1.5 "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

### Auto-Detection
The program automatically detects playlist URLs, so you can also use:
```bash
python3 youtube_audio_downloader.py "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

### Help
```bash
python3 youtube_audio_downloader.py --help
```

## Programmatic Usage

You can also use the `YouTubeAudioDownloader` class in your own Python scripts:

### Single Video Download
```python
from youtube_audio_downloader import YouTubeAudioDownloader

# Create downloader instance
downloader = YouTubeAudioDownloader(output_dir="my_downloads")

# Download single video
try:
    file_path = downloader.download_audio("https://www.youtube.com/watch?v=VIDEO_ID")
    print(f"Downloaded: {file_path}")
except Exception as e:
    print(f"Error: {e}")

# Get video info without downloading
try:
    info = downloader.get_video_info("https://www.youtube.com/watch?v=VIDEO_ID")
    print(f"Title: {info['title']}")
    print(f"Duration: {info['duration']} seconds")
    print(f"Uploader: {info['uploader']}")
except Exception as e:
    print(f"Error: {e}")
```

### Playlist Download
```python
from youtube_audio_downloader import YouTubeAudioDownloader

# Create downloader instance
downloader = YouTubeAudioDownloader(output_dir="playlist_downloads")

# Get playlist info first
try:
    playlist_info = downloader.get_playlist_info("https://www.youtube.com/playlist?list=PLAYLIST_ID")
    print(f"Playlist: {playlist_info['title']}")
    print(f"Videos: {playlist_info['video_count']}")
    
    # Show first few videos
    for i, video in enumerate(playlist_info['videos'][:3], 1):
        print(f"{i}. {video['title']}")
        
except Exception as e:
    print(f"Error: {e}")

# Download entire playlist
try:
    result = downloader.download_playlist("https://www.youtube.com/playlist?list=PLAYLIST_ID")
    print(f"Downloaded {result['successful_downloads']}/{result['total_videos']} videos")
    print(f"Saved to: {result['output_directory']}")
except Exception as e:
    print(f"Error: {e}")

# Download with limits and delays
try:
    result = downloader.download_playlist(
        "https://www.youtube.com/playlist?list=PLAYLIST_ID",
        max_videos=10,           # Download first 10 videos only
        delay_between_downloads=2  # 2 second delay between downloads
    )
except Exception as e:
    print(f"Error: {e}")
```

## Supported URL Formats

### Video URLs
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://www.youtube-nocookie.com/watch?v=VIDEO_ID`

### Playlist URLs
- `https://www.youtube.com/playlist?list=PLAYLIST_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID`
- Any video URL that contains a `list=` parameter

## Output

### Single Videos
- Audio files are saved as MP3 format with 192kbps bitrate
- Default output directory is `downloads/`
- Filenames are based on the video title (can be customized)

### Playlists
- Each playlist is saved in its own subdirectory
- Directory name is based on the playlist title
- Individual MP3 files are named after their video titles
- Example structure:
  ```
  downloads/
  └── My_Awesome_Playlist/
      ├── Song_1.mp3
      ├── Song_2.mp3
      └── Song_3.mp3
  ```

## Error Handling

The program includes comprehensive error handling for:
- Invalid YouTube URLs
- Invalid or private playlists
- Network connection issues
- Video availability problems (private, deleted, region-restricted)
- File system permissions
- Audio conversion errors
- Partial playlist failures (continues with remaining videos)

## Dependencies

- `yt-dlp`: Modern YouTube video downloader with built-in audio conversion
- `FFmpeg`: Required by yt-dlp for audio processing (see installation instructions above)

## Legal Notice

Please respect copyright laws and YouTube's Terms of Service. Only download content you have permission to download or that is available under appropriate licenses.

## Troubleshooting

### "FFmpeg not found" error
Make sure FFmpeg is installed and available in your system PATH.

### "Unable to extract video data" error
The video might be private, deleted, or region-restricted. Try a different video.

### Permission denied errors
Make sure you have write permissions to the output directory.

### Slow downloads
This depends on your internet connection and YouTube's servers. The program downloads the best available audio quality.

### Playlist download stops after a few videos
Some playlists may have private or deleted videos. The program will skip these and continue with available videos.

### Rate limiting or "Too many requests" errors
YouTube may rate-limit requests. Increase the delay between downloads using `--delay` option (e.g., `--delay 3`).

**For more troubleshooting help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

## Distribution

Want to share this program with others? See [DISTRIBUTION.md](DISTRIBUTION.md) for complete instructions on:
- Creating GitHub releases
- Publishing to PyPI
- Building standalone executables
- Docker distribution
- Platform testing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
