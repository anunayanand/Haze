"""
Improved YouTube Playlist Downloader
With better error handling and slower download speed to avoid timeouts
"""

import os
import sys
import subprocess

def download_playlist_improved(playlist_url, output_folder="downloaded_songs"):
    """
    Download playlist with improved settings to handle network issues
    """
    
    # Create output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"✓ Created folder: {output_folder}\n")
    
    # Build the command with better retry settings
    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",  # Best quality
        "--output", f"{output_folder}/%(playlist_index)s - %(title)s.%(ext)s",
        "--ignore-errors",
        "--no-warnings",
        "--retries", "20",  # More retries
        "--fragment-retries", "20",
        "--retry-sleep", "5",  # Wait 5 seconds between retries
        "--limit-rate", "2M",  # Limit speed to avoid timeouts
        "--throttled-rate", "100K",  # Minimum rate
        "--no-playlist-reverse",
        "--download-archive", "downloaded.txt",  # Skip already downloaded
        playlist_url
    ]
    
    print("🎵 Starting download with improved settings...")
    print(f"📁 Saving to: {os.path.abspath(output_folder)}\n")
    print("⚙️  Settings: Slower speed, more retries, better error handling")
    print("=" * 60)
    
    try:
        # Run the command
        subprocess.run(command, check=True)
        
        print("\n" + "=" * 60)
        print("✅ Download complete!")
        print(f"📂 Files saved in: {os.path.abspath(output_folder)}")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: {e}")
        print("\nSome songs may have failed. Check the output above.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user")
        print("Progress saved. Run again to resume.")
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python improved_download.py <playlist_url>")
        sys.exit(1)
    
    playlist_url = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else "downloaded_songs"
    
    download_playlist_improved(playlist_url, output_folder)
