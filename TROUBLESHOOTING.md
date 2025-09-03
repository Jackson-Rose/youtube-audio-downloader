# Troubleshooting Guide

This guide helps resolve common issues when using the YouTube Audio Downloader.

## Common Issues

### 1. "FFmpeg not found" Error

**Problem:** The program can't find FFmpeg on your system.

**Solutions:**

**macOS:**
```bash
# Install using Homebrew
brew install ffmpeg

# Or using MacPorts
sudo port install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
```cmd
# Using Chocolatey (recommended)
choco install ffmpeg

# Or download manually from https://ffmpeg.org/download.html
# Extract to C:\ffmpeg\ and add C:\ffmpeg\bin\ to PATH
```

**Verify FFmpeg installation:**
```bash
ffmpeg -version
```

### 2. "No module named 'yt_dlp'" Error

**Problem:** The yt-dlp package is not installed.

**Solution:**
```bash
pip install yt-dlp
# or
pip3 install yt-dlp
```

### 3. "Permission denied" Error

**Problem:** The program can't write to the output directory.

**Solutions:**
- Choose a different output directory: `youtube-audio-downloader -d ~/Downloads "URL"`
- Fix permissions: `chmod 755 downloads/`
- Run with appropriate permissions (avoid `sudo` unless necessary)

### 4. "Video unavailable" or "Private video" Error

**Problem:** The video is private, deleted, or region-restricted.

**Solutions:**
- Verify the URL is correct and accessible in a web browser
- Try a different video
- Check if the video is available in your region
- For playlists, the program will skip unavailable videos automatically

### 5. Downloads are Very Slow

**Problem:** Network or YouTube rate limiting.

**Solutions:**
- Increase delay between downloads: `youtube-audio-downloader --delay 3 "URL"`
- Check your internet connection
- Try downloading during off-peak hours
- For playlists, use `--max-videos` to limit the number of downloads

### 6. "No such file or directory" Error

**Problem:** File path or system configuration issues.

**Solutions:**
1. **Check output directory exists and is writable**
2. **Verify FFmpeg is properly installed and in PATH**
3. **Use absolute paths:**
   ```bash
   youtube-audio-downloader -d "/full/path/to/downloads" "URL"
   ```
4. **Check for special characters in filenames**

### 7. "HTTP Error 429: Too Many Requests"

**Problem:** YouTube is rate-limiting your requests.

**Solutions:**
- Wait a few minutes before trying again
- Increase delay: `youtube-audio-downloader --delay 5 "URL"`
- Avoid downloading too many videos in quick succession

### 8. Audio Quality Issues

**Problem:** Downloaded audio has poor quality or wrong format.

**Solutions:**
- The program uses 192kbps MP3 by default (good quality)
- YouTube's audio quality varies by video
- Some very old videos may have lower quality source audio

### 9. Python Command Not Found

**Problem:** Python is not installed or not in PATH.

**Solutions:**

**macOS:**
```bash
# Install Python using Homebrew
brew install python

# Or download from python.org
```

**Ubuntu/Debian:**
```bash
sudo apt install python3 python3-pip
```

**Windows:**
- Download Python from [python.org](https://python.org)
- **Important:** Check "Add Python to PATH" during installation

### 10. Playlist Downloads Stop Unexpectedly

**Problem:** Some videos in the playlist are unavailable.

**Solutions:**
- This is normal behavior - the program skips unavailable videos
- Check the final summary for successful vs. failed downloads
- Use `--max-videos` to limit downloads for testing

## Platform-Specific Issues

### macOS Issues

**"Command not found" after installation:**
```bash
# Add Python user bin to PATH
echo 'export PATH="$HOME/Library/Python/3.x/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Apple Silicon (M1/M2) FFmpeg issues:**
```bash
# Use Homebrew for Apple Silicon
/opt/homebrew/bin/brew install ffmpeg
```

### Windows Issues

**PowerShell execution policy errors:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Path issues:**
- Make sure both Python and FFmpeg are in your system PATH
- Restart Command Prompt/PowerShell after installing

### Linux Issues

**Permission denied for pip install:**
```bash
# Install to user directory
pip3 install --user youtube-audio-downloader
```

**FFmpeg not in repository:**
```bash
# Enable additional repositories
sudo apt install software-properties-common
sudo add-apt-repository ppa:jonathonf/ffmpeg-4
sudo apt update
sudo apt install ffmpeg
```

## Getting Help

### Enable Verbose Output

For debugging, you can modify the script to enable verbose output:
```python
# In youtube_audio_downloader.py, change:
current_ydl_opts['verbose'] = True  # Set to True for debugging
```

### Check System Information

```bash
# Check Python version
python3 --version

# Check pip version
pip3 --version

# Check FFmpeg version
ffmpeg -version

# Check yt-dlp version
yt-dlp --version
```

### Report Issues

If you encounter issues not covered here:

1. **Gather information:**
   - Your operating system and version
   - Python version (`python3 --version`)
   - FFmpeg version (`ffmpeg -version`)
   - Complete error message
   - The URL you're trying to download

2. **Try the standalone script:**
   ```bash
   python3 youtube_audio_downloader.py --help
   ```

3. **Create an issue on GitHub** with the above information

## Performance Tips

### Optimize for Large Playlists

```bash
# Use delays to avoid rate limiting
youtube-audio-downloader --playlist --delay 2 "PLAYLIST_URL"

# Limit concurrent downloads
youtube-audio-downloader --playlist --max-videos 50 "PLAYLIST_URL"

# Use a dedicated directory
youtube-audio-downloader --playlist -d "large_playlist" "PLAYLIST_URL"
```

### Storage Management

```bash
# Check available disk space before large downloads
df -h

# Monitor download directory size
du -sh downloads/
```

Remember: Always respect YouTube's Terms of Service and copyright laws when downloading content.
