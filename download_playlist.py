"""
YouTube Music Playlist Downloader
Downloads all songs from a YouTube Music playlist as MP3 files

Requirements:
    pip install yt-dlp

Usage:
    python download_playlist.py
    Then paste your YouTube Music playlist URL when prompted
"""

import os
import sys

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed.")
    print("Please install it using: pip install yt-dlp")
    sys.exit(1)


def download_playlist(playlist_url, output_folder="downloaded_songs"):
    """
    Download all songs from a YouTube Music playlist
    
    Args:
        playlist_url (str): URL of the YouTube Music playlist
        output_folder (str): Folder to save downloaded songs
    """
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"✓ Created folder: {output_folder}")
    
    # yt-dlp options for best audio quality
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',  # 320 kbps for best quality
        }],
        'outtmpl': os.path.join(output_folder, '%(playlist_index)s - %(title)s.%(ext)s'),
        'ignoreerrors': True,  # Continue on errors
        'no_warnings': False,
        'quiet': False,
        'extract_flat': 'in_playlist',  # Faster playlist extraction
        'playlist_items': None,  # Download all items
        'retries': 10,  # Retry failed downloads
        'fragment_retries': 10,  # Retry failed fragments
        'skip_unavailable_fragments': True,
        'keepvideo': False,  # Delete video file after audio extraction
        'prefer_free_formats': True,
        'nocheckcertificate': True,
    }
    
    print(f"\n🎵 Starting download from playlist...")
    print(f"📁 Saving to: {os.path.abspath(output_folder)}\n")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("📋 Downloading playlist...\n")
            print("=" * 60)
            
            # Download the playlist directly without pre-extraction
            ydl.download([playlist_url])
            
        print("\n" + "=" * 60)
        print("✅ Download complete!")
        print(f"📂 Files saved in: {os.path.abspath(output_folder)}")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure the playlist URL is correct")
        print("2. Check your internet connection")
        print("3. Ensure FFmpeg is installed (required for MP3 conversion)")
        print("   Download from: https://ffmpeg.org/download.html")
        sys.exit(1)


def main():
    """Main function to run the script"""
    
    print("=" * 60)
    print("🎵 YouTube Music Playlist Downloader")
    print("=" * 60)
    print()
    
    # Get playlist URL from user
    playlist_url = input("📎 Paste your YouTube Music playlist URL: ").strip()
    
    if not playlist_url:
        print("❌ No URL provided. Exiting...")
        sys.exit(1)
    
    # Validate URL
    if 'youtube.com' not in playlist_url and 'youtu.be' not in playlist_url:
        print("⚠️  Warning: This doesn't look like a YouTube URL")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            sys.exit(0)
    
    # Optional: Custom output folder
    print()
    custom_folder = input("📁 Output folder (press Enter for 'downloaded_songs'): ").strip()
    output_folder = custom_folder if custom_folder else "downloaded_songs"
    
    # Start download
    download_playlist(playlist_url, output_folder)


if __name__ == "__main__":
    main()
