import os
import sys
import json
import yt_dlp
import re

def clean_filename(title):
    # Remove common extra info like (Lyrics), (Official Video), etc.
    title = re.sub(r'\s*\([^)]*\)', '', title)
    title = re.sub(r'\s*\[[^\]]*\]', '', title)
    title = re.sub(r'\s*\|.*$', '', title)
    # Remove non-alphanumeric chars for comparison
    return "".join([c for c in title if c.isalnum()]).lower()

def get_existing_songs(folder):
    existing = set()
    if not os.path.exists(folder):
        return existing
        
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".mp3"):
                # Clean the filename for better matching
                clean_name = clean_filename(file.replace(".mp3", ""))
                existing.add(clean_name)
    return existing

def download_playlist(playlist_url, output_base="downloaded_song"):
    print(f"Scanning {output_base} for existing songs...")
    existing_songs = get_existing_songs(output_base)
    print(f"Found {len(existing_songs)} existing songs.")

    # Extract playlist info
    ydl_opts_info = {
        'extract_flat': True,
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
        playlist_dict = ydl.extract_info(playlist_url, download=False)
        playlist_title = playlist_dict.get('title', 'Downloaded Playlist')
        entries = playlist_dict.get('entries', [])
        
    # Clean folder name
    folder_name = "".join([c for c in playlist_title if c.isalnum() or c in (' ', '-', '_')]).strip()
    folder_name = folder_name.replace(' ', '-').lower()
    output_folder = os.path.join(output_base, folder_name)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Filter entries to skip existing ones
    to_download = []
    for entry in entries:
        title = entry.get('title', '')
        if not title: continue
        clean_title = clean_filename(title)
        if clean_title in existing_songs:
            print(f"⏭️ Skipping (already exists): {title}")
        else:
            to_download.append(entry)

    if not to_download:
        print("✅ All songs are already downloaded!")
        return

    print(f"🚀 Downloading {len(to_download)} new songs...")

    # Download options - focus on stability and MP3 conversion
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'ignoreerrors': True,
        'nooverwrites': True,
        'socket_timeout': 60,
        'retries': 20,
        'fragment_retries': 20,
        'nocheckcertificate': True,
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for entry in to_download:
            try:
                print(f"📥 Downloading: {entry.get('title')}")
                ydl.download([entry['url']])
            except Exception as e:
                print(f"❌ Error downloading {entry.get('title')}: {e}")

    # Process metadata for app.js
    songs_data = []
    if os.path.exists(output_folder):
        for filename in os.listdir(output_folder):
            if filename.endswith((".mp3", ".m4a")):
                filepath = os.path.join(output_folder, filename).replace("\\", "/")
                songs_data.append({
                    "title": os.path.splitext(filename)[0],
                    "file": filepath,
                    "thumbnail": None
                })

    metadata_file = os.path.join(output_folder, "metadata.json")
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump({"playlist_id": folder_name, "playlist_title": playlist_title, "songs": songs_data}, f, indent=2)
        
    print(f"✅ Download complete! Metadata saved to {metadata_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python downloader.py <playlist_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    download_playlist(url)
