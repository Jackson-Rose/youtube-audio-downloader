#!/usr/bin/env python3
"""
Example script demonstrating playlist download functionality
"""

from youtube_audio_downloader import YouTubeAudioDownloader

def main():
    # Example playlist URLs (replace with actual playlists)
    playlist_urls = [
        "https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMHjMZOz59Ys8KQJOx",  # Example playlist
        # Add more playlist URLs here
    ]
    
    print("🎵 YouTube Playlist Audio Downloader - Example")
    print("=" * 50)
    
    # Create downloader instance
    downloader = YouTubeAudioDownloader(output_dir="playlist_downloads")
    
    for i, playlist_url in enumerate(playlist_urls, 1):
        try:
            print(f"\n📋 Processing playlist {i}/{len(playlist_urls)}")
            print(f"URL: {playlist_url}")
            
            # First, get playlist information
            playlist_info = downloader.get_playlist_info(playlist_url)
            print(f"Playlist: {playlist_info['title']}")
            print(f"Videos: {playlist_info['video_count']}")
            
            # Ask user for confirmation
            response = input(f"\nDownload this playlist? (y/n/s for skip): ").lower()
            
            if response in ['y', 'yes']:
                # Option 1: Download entire playlist
                result = downloader.download_playlist(playlist_url)
                print(f"✅ Completed: {result['successful_downloads']}/{result['total_videos']} videos")
                
            elif response in ['s', 'skip']:
                print("⏭️  Skipping this playlist")
                continue
                
            else:
                print("❌ Skipping this playlist")
                continue
                
        except Exception as e:
            print(f"❌ Error processing playlist: {e}")
            continue
    
    print("\n🎉 All playlists processed!")

def download_with_options_example():
    """Example showing different download options"""
    
    playlist_url = "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
    downloader = YouTubeAudioDownloader(output_dir="custom_downloads")
    
    try:
        print("Example 1: Download first 5 videos only")
        result = downloader.download_playlist(
            playlist_url,
            max_videos=5,
            delay_between_downloads=2  # 2 second delay between downloads
        )
        
        print("Example 2: Get playlist info without downloading")
        info = downloader.get_playlist_info(playlist_url)
        print(f"Playlist has {info['video_count']} videos")
        
        # Show first few video titles
        for i, video in enumerate(info['videos'][:3], 1):
            print(f"{i}. {video['title']} ({video['duration']}s)")
            
    except Exception as e:
        print(f"Error: {e}")

def batch_playlist_download():
    """Example of downloading multiple playlists with different settings"""
    
    playlists = [
        {
            "url": "https://www.youtube.com/playlist?list=PLAYLIST1",
            "max_videos": 10,
            "delay": 1.5
        },
        {
            "url": "https://www.youtube.com/playlist?list=PLAYLIST2",
            "max_videos": None,  # Download all
            "delay": 2.0
        }
    ]
    
    downloader = YouTubeAudioDownloader(output_dir="batch_downloads")
    
    for playlist_config in playlists:
        try:
            print(f"Downloading playlist: {playlist_config['url']}")
            result = downloader.download_playlist(
                playlist_config['url'],
                max_videos=playlist_config['max_videos'],
                delay_between_downloads=playlist_config['delay']
            )
            print(f"Success: {result['successful_downloads']} videos downloaded")
            
        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    print("Choose an example to run:")
    print("1. Interactive playlist downloader")
    print("2. Download with custom options")
    print("3. Batch playlist download")
    
    choice = input("Enter choice (1-3): ")
    
    if choice == "1":
        main()
    elif choice == "2":
        download_with_options_example()
    elif choice == "3":
        batch_playlist_download()
    else:
        print("Invalid choice. Running default example...")
        main()
