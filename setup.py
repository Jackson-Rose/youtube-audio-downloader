#!/usr/bin/env python3
"""
Setup script for YouTube Audio Downloader
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "YouTube Audio Downloader - Download audio from YouTube videos and playlists"

setup(
    name="youtube-audio-downloader",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Download audio from YouTube videos and playlists in MP3 format",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/youtube-audio-downloader",
    py_modules=["youtube_audio_downloader"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "yt-dlp>=2024.1.0",
    ],
    entry_points={
        "console_scripts": [
            "youtube-audio-downloader=youtube_audio_downloader:main",
            "ytdl-audio=youtube_audio_downloader:main",
        ],
    },
    keywords="youtube audio downloader mp3 playlist music",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/youtube-audio-downloader/issues",
        "Source": "https://github.com/yourusername/youtube-audio-downloader",
        "Documentation": "https://github.com/yourusername/youtube-audio-downloader/blob/main/README.md",
    },
)
