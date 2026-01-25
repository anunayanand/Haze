"""
Simple YouTube Playlist Downloader
A simpler alternative that downloads one song at a time

Usage:
    python simple_download.py <playlist_url>
    
Example:
    python simple_download.py "https://music.youtube.com/playlist?list=PLxxxxxx"
"""

import os
import sys
import subprocess

def download_playlist_simple(playlist_url, output_folder="downloaded_songs"):
    """
    Download playlist using yt-dlp command line directly
    This is more reliable than using the Python API
    """
    
    # Create output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"✓ Created folder: {output_folder}\n")
    
    # Build the command
    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",  # Best quality
        "--output", f"{output_folder}/%(playlist_index)s - %(title)s.%(ext)s",
        "--ignore-errors",
        "--no-warnings",
        "--progress",
        playlist_url
    ]
    
    print("🎵 Starting download...")
    print(f"📁 Saving to: {os.path.abspath(output_folder)}\n")
    print("=" * 60)
    
    try:
        # Run the command
        subprocess.run(command, check=True)
        
        print("\n" + "=" * 60)
        print("✅ Download complete!")
        print(f"📂 Files saved in: {os.path.abspath(output_folder)}")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("1. yt-dlp is installed: pip install yt-dlp")
        print("2. FFmpeg is installed and in PATH")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user")
        print("You can resume by running the script again with the same URL")
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python simple_download.py <playlist_url>")
        print("\nExample:")
        print('  python simple_download.py "https://music.youtube.com/playlist?list=PLxxxxxx"')
        sys.exit(1)
    
    playlist_url = sys.argv[1]
    
    # Optional: custom folder as second argument
    output_folder = sys.argv[2] if len(sys.argv) > 2 else "downloaded_songs"
    
    download_playlist_simple(playlist_url, output_folder)
