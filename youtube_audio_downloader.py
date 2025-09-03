#!/usr/bin/env python3
"""
YouTube Audio Downloader - Simple Version

A Python script that downloads audio from YouTube videos and converts them to MP3 format.
Requires yt-dlp and ffmpeg to be installed.

This is the simplified version without continuous monitoring features.
"""

import os
import sys
import argparse
import re
import time
import shutil
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import yt_dlp

# Try to import pydub, but provide fallback if not available
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("Warning: pydub not available, using yt-dlp for audio conversion")


class YouTubeAudioDownloader:
    def __init__(self, output_dir="downloads"):
        """Initialize the downloader with an output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Find FFmpeg location (cross-platform)
        ffmpeg_path = shutil.which('ffmpeg')
        if not ffmpeg_path:
            # Try common locations on different systems
            common_paths = [
                '/usr/local/bin/ffmpeg',  # macOS Homebrew
                '/usr/bin/ffmpeg',        # Linux
                '/opt/homebrew/bin/ffmpeg',  # macOS Apple Silicon Homebrew
                'C:\\ffmpeg\\bin\\ffmpeg.exe',  # Windows common location
                'C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe',  # Windows Program Files
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    ffmpeg_path = path
                    break
            
            if not ffmpeg_path:
                raise Exception(
                    "FFmpeg not found. Please install FFmpeg:\n"
                    "• macOS: brew install ffmpeg\n"
                    "• Ubuntu/Debian: sudo apt install ffmpeg\n"
                    "• Windows: Download from https://ffmpeg.org/download.html\n"
                    "Make sure FFmpeg is in your system PATH."
                )
        
        # Configure yt-dlp options
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': ffmpeg_path,
            'prefer_ffmpeg': True,
        }
    
    def is_valid_youtube_url(self, url):
        """Validate if the provided URL is a valid YouTube URL."""
        youtube_regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        return youtube_regex.match(url) is not None
    
    def is_playlist_url(self, url):
        """Check if the URL is a YouTube playlist URL."""
        playlist_patterns = [
            r'[&?]list=([a-zA-Z0-9_-]+)',
            r'youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)',
            r'youtube\.com/watch\?.*list=([a-zA-Z0-9_-]+)'
        ]
        return any(re.search(pattern, url) for pattern in playlist_patterns)
    
    def extract_playlist_id(self, url):
        """Extract playlist ID from YouTube URL."""
        parsed = urlparse(url)
        if 'list' in parsed.query:
            return parse_qs(parsed.query)['list'][0]
        
        # Try regex patterns as fallback
        playlist_match = re.search(r'[&?]list=([a-zA-Z0-9_-]+)', url)
        if playlist_match:
            return playlist_match.group(1)
        
        return None
    
    def get_video_info(self, url):
        """Get video information without downloading."""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown')
                }
        except Exception as e:
            raise Exception(f"Failed to get video info: {str(e)}")
    
    def get_playlist_info(self, url):
        """Get playlist information and video URLs."""
        if not self.is_playlist_url(url):
            raise ValueError("URL is not a valid YouTube playlist")
        
        try:
            # Configure yt-dlp for playlist extraction
            playlist_opts = {
                'quiet': True,
                'extract_flat': True,  # Only get URLs, don't download
                'playlistend': None,   # Get all videos
            }
            
            with yt_dlp.YoutubeDL(playlist_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if 'entries' not in info:
                    raise Exception("No videos found in playlist")
                
                # Extract video information
                videos = []
                for entry in info['entries']:
                    if entry:  # Skip None entries (private/deleted videos)
                        videos.append({
                            'url': f"https://www.youtube.com/watch?v={entry['id']}",
                            'title': entry.get('title', 'Unknown Title'),
                            'duration': entry.get('duration', 0),
                            'uploader': entry.get('uploader', 'Unknown')
                        })
                
                playlist_info = {
                    'title': info.get('title', 'Unknown Playlist'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'video_count': len(videos),
                    'videos': videos
                }
                
                return playlist_info
                
        except Exception as e:
            raise Exception(f"Failed to get playlist info: {str(e)}")
    
    def download_audio(self, url, output_filename=None):
        """Download audio from YouTube URL and convert to MP3."""
        if not self.is_valid_youtube_url(url):
            raise ValueError("Invalid YouTube URL provided")
        
        try:
            # Get video info first
            video_info = self.get_video_info(url)
            print(f"Downloading: {video_info['title']}")
            print(f"Uploader: {video_info['uploader']}")
            
            # Sanitize the title for filename
            safe_title = self._sanitize_filename(video_info['title'])
            
            # Configure output template for this download
            current_ydl_opts = self.ydl_opts.copy()
            
            if output_filename:
                # Use custom filename if provided
                base_name = output_filename.replace('.mp3', '')
                safe_base_name = self._sanitize_filename(base_name)
                current_ydl_opts['outtmpl'] = str(self.output_dir / f"{safe_base_name}.%(ext)s")
                expected_final_name = f"{safe_base_name}.mp3"
            else:
                # Use sanitized video title
                current_ydl_opts['outtmpl'] = str(self.output_dir / f"{safe_title}.%(ext)s")
                expected_final_name = f"{safe_title}.mp3"
            
            # Add verbose output for debugging
            current_ydl_opts['verbose'] = False  # Set to True for debugging
            
            print(f"Output directory: {self.output_dir}")
            print(f"Expected filename: {expected_final_name}")
            
            # Download and convert the audio using yt-dlp
            with yt_dlp.YoutubeDL(current_ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Look for the downloaded MP3 file
                final_path = self.output_dir / expected_final_name
                
                # If the exact expected file doesn't exist, search for any MP3 files
                if not final_path.exists():
                    print(f"Expected file not found: {final_path}")
                    print("Searching for downloaded files...")
                    
                    # List all files in the output directory
                    all_files = list(self.output_dir.glob("*"))
                    print(f"Files in directory: {[f.name for f in all_files]}")
                    
                    # Search for MP3 files
                    mp3_files = list(self.output_dir.glob("*.mp3"))
                    if mp3_files:
                        # Get the most recently created MP3 file
                        final_path = max(mp3_files, key=os.path.getctime)
                        print(f"Found MP3 file: {final_path}")
                    else:
                        raise Exception(f"No MP3 file found in {self.output_dir}. Files present: {[f.name for f in all_files]}")
                
                print(f"✓ Audio downloaded successfully: {final_path}")
                return str(final_path)
                
        except yt_dlp.utils.DownloadError as e:
            raise Exception(f"yt-dlp download error: {str(e)}")
        except FileNotFoundError as e:
            raise Exception(f"File system error (check FFmpeg installation): {str(e)}")
        except Exception as e:
            raise Exception(f"Download failed: {str(e)}")
    
    def download_multiple(self, urls):
        """Download audio from multiple YouTube URLs."""
        results = []
        for i, url in enumerate(urls, 1):
            try:
                print(f"\n[{i}/{len(urls)}] Processing: {url}")
                result = self.download_audio(url)
                results.append({"url": url, "file": result, "status": "success"})
            except Exception as e:
                print(f"✗ Failed to download {url}: {e}")
                results.append({"url": url, "file": None, "status": "failed", "error": str(e)})
        
        return results
    
    def download_playlist(self, playlist_url, max_videos=None, delay_between_downloads=1):
        """Download all audio from a YouTube playlist."""
        if not self.is_playlist_url(playlist_url):
            raise ValueError("URL is not a valid YouTube playlist")
        
        try:
            # Get playlist information
            print("📋 Analyzing playlist...")
            playlist_info = self.get_playlist_info(playlist_url)
            
            print(f"Playlist: {playlist_info['title']}")
            print(f"Uploader: {playlist_info['uploader']}")
            print(f"Total videos: {playlist_info['video_count']}")
            
            # Limit videos if specified
            videos_to_download = playlist_info['videos']
            if max_videos and max_videos > 0:
                videos_to_download = videos_to_download[:max_videos]
                print(f"Limiting download to first {max_videos} videos")
            
            # Create playlist-specific subdirectory
            playlist_name = self._sanitize_filename(playlist_info['title'])
            playlist_dir = self.output_dir / playlist_name
            playlist_dir.mkdir(exist_ok=True)
            
            # Temporarily change output directory
            original_output_dir = self.output_dir
            self.output_dir = playlist_dir
            self.ydl_opts['outtmpl'] = str(playlist_dir / '%(title)s.%(ext)s')
            
            print(f"\n🎵 Starting download of {len(videos_to_download)} videos...")
            print(f"📁 Saving to: {playlist_dir}")
            print("=" * 50)
            
            results = []
            successful_downloads = 0
            
            for i, video in enumerate(videos_to_download, 1):
                try:
                    print(f"\n[{i}/{len(videos_to_download)}] {video['title']}")
                    print(f"🔗 {video['url']}")
                    
                    result = self.download_audio(video['url'])
                    results.append({
                        "video": video,
                        "file": result,
                        "status": "success"
                    })
                    successful_downloads += 1
                    
                    # Add delay between downloads to be respectful
                    if delay_between_downloads > 0 and i < len(videos_to_download):
                        print(f"⏳ Waiting {delay_between_downloads} seconds...")
                        time.sleep(delay_between_downloads)
                        
                except Exception as e:
                    print(f"✗ Failed to download: {e}")
                    results.append({
                        "video": video,
                        "file": None,
                        "status": "failed",
                        "error": str(e)
                    })
                    continue
            
            # Restore original output directory
            self.output_dir = original_output_dir
            self.ydl_opts['outtmpl'] = str(original_output_dir / '%(title)s.%(ext)s')
            
            # Summary
            print("\n" + "=" * 50)
            print(f"🎉 Playlist download completed!")
            print(f"✅ Successfully downloaded: {successful_downloads}/{len(videos_to_download)}")
            print(f"❌ Failed downloads: {len(videos_to_download) - successful_downloads}")
            print(f"📁 Files saved to: {playlist_dir}")
            
            return {
                "playlist_info": playlist_info,
                "results": results,
                "successful_downloads": successful_downloads,
                "total_videos": len(videos_to_download),
                "output_directory": str(playlist_dir)
            }
            
        except Exception as e:
            # Restore original output directory in case of error
            if 'original_output_dir' in locals():
                self.output_dir = original_output_dir
                self.ydl_opts['outtmpl'] = str(original_output_dir / '%(title)s.%(ext)s')
            raise Exception(f"Playlist download failed: {str(e)}")
    
    def _sanitize_filename(self, filename):
        """Sanitize filename for filesystem compatibility."""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limit length and strip whitespace
        filename = filename.strip()[:100]
        
        return filename or "Unknown_Playlist"


def main():
    """Main function to handle command-line usage."""
    parser = argparse.ArgumentParser(
        description="Download audio from YouTube videos or playlists in MP3 format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Single video:
    %(prog)s "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    %(prog)s -o "my_song.mp3" "https://youtu.be/dQw4w9WgXcQ"
    %(prog)s -d "my_music" "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  
  Playlist:
    %(prog)s --playlist "https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMHjMZOz59Ys8KQJOx"
    %(prog)s --playlist --max-videos 10 "https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMHjMZOz59Ys8KQJOx"
    %(prog)s --playlist --delay 2 "https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMHjMZOz59Ys8KQJOx"
        """
    )
    
    parser.add_argument(
        "url",
        help="YouTube video or playlist URL to download audio from"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output filename (only for single videos, default: uses video title)"
    )
    
    parser.add_argument(
        "-d", "--directory",
        default="downloads",
        help="Output directory (default: downloads)"
    )
    
    parser.add_argument(
        "--playlist",
        action="store_true",
        help="Download entire playlist (auto-detected if URL contains playlist)"
    )
    
    parser.add_argument(
        "--max-videos",
        type=int,
        help="Maximum number of videos to download from playlist"
    )
    
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between downloads in seconds (default: 1.0)"
    )
    
    args = parser.parse_args()
    
    try:
        # Create downloader instance
        downloader = YouTubeAudioDownloader(output_dir=args.directory)
        
        # Detect if it's a playlist URL or if playlist flag is set
        is_playlist = args.playlist or downloader.is_playlist_url(args.url)
        
        if is_playlist:
            # Download playlist
            if args.output:
                print("⚠️  Warning: --output option is ignored for playlists")
            
            result = downloader.download_playlist(
                args.url,
                max_videos=args.max_videos,
                delay_between_downloads=args.delay
            )
            
            print(f"\n🎉 Playlist download completed!")
            print(f"✅ Successfully downloaded: {result['successful_downloads']}/{result['total_videos']} videos")
            print(f"📁 Files saved to: {result['output_directory']}")
            
        else:
            # Download single video
            if args.max_videos:
                print("⚠️  Warning: --max-videos option is ignored for single videos")
            if args.delay != 1.0:
                print("⚠️  Warning: --delay option is ignored for single videos")
                
            result = downloader.download_audio(args.url, args.output)
            print(f"\n🎵 Download completed successfully!")
            print(f"File saved to: {result}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Download cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
