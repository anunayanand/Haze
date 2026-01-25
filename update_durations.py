"""
Extract Real Song Durations from MP3 Files (Alternative Method)
Uses ffprobe (comes with FFmpeg) instead of mutagen
"""

import os
import json
import subprocess

def get_mp3_duration_ffprobe(file_path):
    """Get duration of MP3 file using ffprobe"""
    try:
        # Use ffprobe to get duration
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 
             'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', 
             file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            duration_seconds = float(result.stdout.strip())
            minutes = int(duration_seconds // 60)
            seconds = int(duration_seconds % 60)
            return f"{minutes}:{seconds:02d}"
        else:
            return "0:00"
    except Exception as e:
        print(f"  Error: {e}")
        return "0:00"

def update_playlist_durations():
    """Update playlists.json with real MP3 durations"""
    
    # Check if ffprobe is available
    try:
        subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: ffprobe not found!")
        print("\nffprobe comes with FFmpeg. Please install FFmpeg:")
        print("  winget install ffmpeg")
        print("  OR download from: https://ffmpeg.org/download.html")
        return False
    
    # Load existing playlists.json
    if not os.path.exists('playlists.json'):
        print("❌ Error: playlists.json not found!")
        return False
    
    with open('playlists.json', 'r', encoding='utf-8') as f:
        playlists = json.load(f)
    
    print("🎵 Extracting real song durations using ffprobe...\n")
    
    total_songs = 0
    updated_songs = 0
    
    # Update each playlist
    for playlist_id, songs in playlists.items():
        print(f"📀 {playlist_id}:")
        
        for song in songs:
            total_songs += 1
            file_path = song['file']
            
            if os.path.exists(file_path):
                duration = get_mp3_duration_ffprobe(file_path)
                song['duration'] = duration
                updated_songs += 1
                print(f"  ✓ {song['title']}: {duration}")
            else:
                print(f"  ⚠️  File not found: {file_path}")
                song['duration'] = "0:00"
        
        print()
    
    # Save updated playlists.json
    with open('playlists.json', 'w', encoding='utf-8') as f:
        json.dump(playlists, f, indent=2, ensure_ascii=False)
    
    print("=" * 60)
    print(f"✅ Updated {updated_songs}/{total_songs} songs with real durations!")
    print("\n📁 playlists.json has been updated.")
    return True

if __name__ == "__main__":
    success = update_playlist_durations()
    if not success:
        exit(1)
