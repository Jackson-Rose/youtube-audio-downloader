# Installation Guide

This guide will help you install and set up the YouTube Audio Downloader on different operating systems.

## Quick Install (Recommended)

### Method 1: Using pip (when available on PyPI)
```bash
pip install youtube-audio-downloader
```

### Method 2: From Source
```bash
# Clone or download the repository
git clone https://github.com/yourusername/youtube-audio-downloader.git
cd youtube-audio-downloader

# Install the package
pip install .
```

## Platform-Specific Installation

### 🍎 macOS

1. **Install Python 3.8+**
   ```bash
   # Using Homebrew (recommended)
   brew install python
   
   # Or download from https://python.org
   ```

2. **Install FFmpeg**
   ```bash
   brew install ffmpeg
   ```

3. **Install the YouTube Audio Downloader**
   ```bash
   # Method A: From PyPI (when available)
   pip3 install youtube-audio-downloader
   
   # Method B: From source
   git clone https://github.com/yourusername/youtube-audio-downloader.git
   cd youtube-audio-downloader
   pip3 install .
   ```

4. **Usage**
   ```bash
   youtube-audio-downloader "https://www.youtube.com/watch?v=VIDEO_ID"
   # or
   ytdl-audio "https://www.youtube.com/watch?v=VIDEO_ID"
   ```

### 🐧 Linux (Ubuntu/Debian)

1. **Install Python and pip**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install FFmpeg**
   ```bash
   sudo apt install ffmpeg
   ```

3. **Install the YouTube Audio Downloader**
   ```bash
   # Method A: From PyPI (when available)
   pip3 install youtube-audio-downloader
   
   # Method B: From source
   git clone https://github.com/yourusername/youtube-audio-downloader.git
   cd youtube-audio-downloader
   pip3 install .
   ```

4. **Usage**
   ```bash
   youtube-audio-downloader "https://www.youtube.com/watch?v=VIDEO_ID"
   ```

### 🪟 Windows

1. **Install Python 3.8+**
   - Download from [python.org](https://python.org)
   - **Important:** Check "Add Python to PATH" during installation

2. **Install FFmpeg**
   
   **Option A: Using Chocolatey (Recommended)**
   ```cmd
   # Install Chocolatey first: https://chocolatey.org/install
   choco install ffmpeg
   ```
   
   **Option B: Manual Installation**
   - Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Extract to `C:\ffmpeg\`
   - Add `C:\ffmpeg\bin\` to your system PATH

3. **Install the YouTube Audio Downloader**
   ```cmd
   # Method A: From PyPI (when available)
   pip install youtube-audio-downloader
   
   # Method B: From source
   git clone https://github.com/yourusername/youtube-audio-downloader.git
   cd youtube-audio-downloader
   pip install .
   ```

4. **Usage**
   ```cmd
   youtube-audio-downloader "https://www.youtube.com/watch?v=VIDEO_ID"
   ```

### 🐧 Linux (CentOS/RHEL/Fedora)

1. **Install Python and pip**
   ```bash
   # CentOS/RHEL
   sudo yum install python3 python3-pip
   
   # Fedora
   sudo dnf install python3 python3-pip
   ```

2. **Install FFmpeg**
   ```bash
   # Enable EPEL repository first (CentOS/RHEL)
   sudo yum install epel-release
   sudo yum install ffmpeg
   
   # Fedora
   sudo dnf install ffmpeg
   ```

3. **Install the YouTube Audio Downloader**
   ```bash
   pip3 install youtube-audio-downloader
   ```

## Development Installation

If you want to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/yourusername/youtube-audio-downloader.git
cd youtube-audio-downloader

# Install in development mode
pip install -e .

# Now you can edit the code and changes will be reflected immediately
```

## Verification

Test that everything is installed correctly:

```bash
# Test the installation
youtube-audio-downloader --help

# Test with a short video
youtube-audio-downloader "https://www.youtube.com/watch?v=jNQXAC9IVRw"
```

## Alternative: Standalone Script

If you prefer not to install the package, you can run it as a standalone script:

```bash
# Download the script
wget https://raw.githubusercontent.com/yourusername/youtube-audio-downloader/main/youtube_audio_downloader.py

# Make it executable (Linux/macOS)
chmod +x youtube_audio_downloader.py

# Run it
python3 youtube_audio_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Docker Installation (Advanced)

For a completely isolated environment:

```bash
# Build the Docker image
docker build -t youtube-audio-downloader .

# Run the container
docker run -v $(pwd)/downloads:/app/downloads youtube-audio-downloader "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.
