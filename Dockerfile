# Dockerfile for YouTube Audio Downloader
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY youtube_audio_downloader.py .
COPY setup.py .
COPY README.md .
COPY LICENSE .

# Install the application
RUN pip install .

# Create downloads directory
RUN mkdir -p /app/downloads

# Set up non-root user for security
RUN useradd -m -u 1000 downloader && \
    chown -R downloader:downloader /app
USER downloader

# Set volume for downloads
VOLUME ["/app/downloads"]

# Default command
ENTRYPOINT ["youtube-audio-downloader"]
CMD ["--help"]
