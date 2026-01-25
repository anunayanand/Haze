"""
Music Organizer for SaasuFy
Organizes downloaded songs into playlist folders
"""

import os
import shutil
import json

# Define playlist categories based on song mood/theme
PLAYLISTS = {
    'neet-warrior': {
        'folder': 'music/neet-warrior',
        'songs': [
            '27 - Unstoppable.mp3',
            '44 - Hall of Fame.mp3',
            '29 - Nee Singam Dhan.mp3',
            '30 - Powerhouse (From ＂Coolie＂) (Tamil).mp3',
            '31 - SNAP.mp3',
            '14 - Amplifier.mp3',
            '35 - Rasputin.mp3',
            '61 - Running Up That Hill (A Deal With God).mp3',
            '28 - 7 Years.mp3',
            '43 - End of Beginning.mp3'
        ]
    },
    'chef-specials': {
        'folder': 'music/chef-specials',
        'songs': [
            '37 - Instant Cooker Paneer Recipe #Shorts.mp3',
            '48 - Everything at Once.mp3',
            '46 - Dance Monkey.mp3',
            '51 - Espresso.mp3',
            '60 - Lahore.mp3',
            '15 - Libaas.mp3',
            '16 - Teeji Seat.mp3',
            '17 - Mitti De Tibbe.mp3',
            '56 - Temporary Pyar.mp3',
            '32 - Heeriye (feat. Arijit Singh).mp3'
        ]
    },
    'soft-break': {
        'folder': 'music/soft-break',
        'songs': [
            '08 - Let Her Go (Anniversary Edition).mp3',
            '45 - A Thousand Years.mp3',
            '47 - somewhere only we know.mp3',
            '59 - The Night We Met.mp3',
            '05 - Until I Found You (Em Beihold Version).mp3',
            '06 - Dancing With Your Ghost.mp3',
            '34 - Khairiyat.mp3',
            '24 - Tera Yaar Hoon Main.mp3',
            '49 - Let Me Down Slowly.mp3',
            '63 - Dandelions.mp3'
        ]
    },
    'bahurani-picks': {
        'folder': 'music/bahurani-picks',
        'songs': [
            '12 - Die With A Smile.mp3',
            '02 - Skyfall.mp3',
            '04 - Fairytale.mp3',
            '07 - I Wanna Be Yours.mp3',
            '11 - Summertime Sadness.mp3',
            '18 - We Don\'t Talk Anymore (feat. Selena Gomez).mp3',
            '19 - Attention.mp3',
            '21 - STAY.mp3',
            '25 - Arcade.mp3',
            '41 - Love Me Like You Do (From ＂Fifty Shades Of Grey＂).mp3'
        ]
    }
}

def organize_music():
    """Organize downloaded songs into playlist folders"""
    
    source_folder = 'downloaded_songs'
    
    if not os.path.exists(source_folder):
        print(f"❌ Error: {source_folder} folder not found!")
        return
    
    print("🎵 Organizing music into playlists...\n")
    
    # Create music directory structure
    for playlist_id, playlist_data in PLAYLISTS.items():
        folder = playlist_data['folder']
        
        # Create folder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✓ Created folder: {folder}")
        
        # Copy songs to playlist folder
        for song_file in playlist_data['songs']:
            source_path = os.path.join(source_folder, song_file)
            
            if os.path.exists(source_path):
                # Clean filename (remove number prefix)
                clean_name = ' - '.join(song_file.split(' - ')[1:])
                dest_path = os.path.join(folder, clean_name)
                
                # Copy file
                shutil.copy2(source_path, dest_path)
                print(f"  ✓ Copied: {clean_name}")
            else:
                print(f"  ⚠️  Not found: {song_file}")
        
        print()
    
    print("=" * 60)
    print("✅ Music organization complete!")
    print("\nFolder structure:")
    print("  music/")
    print("    ├── neet-warrior/")
    print("    ├── chef-specials/")
    print("    ├── soft-break/")
    print("    └── bahurani-picks/")
    print("\n📁 You can now use these songs in the SaasuFy app!")

def generate_playlist_json():
    """Generate JSON file with playlist data for the web app"""
    
    playlist_data = {}
    
    for playlist_id, playlist_info in PLAYLISTS.items():
        folder = playlist_info['folder']
        songs = []
        
        for song_file in playlist_info['songs']:
            # Clean filename
            clean_name = ' - '.join(song_file.split(' - ')[1:])
            title = clean_name.replace('.mp3', '')
            
            songs.append({
                'title': title,
                'file': f"{folder}/{clean_name}"
            })
        
        playlist_data[playlist_id] = songs
    
    # Save to JSON file
    with open('playlists.json', 'w', encoding='utf-8') as f:
        json.dump(playlist_data, f, indent=2, ensure_ascii=False)
    
    print("\n✓ Generated playlists.json")

if __name__ == "__main__":
    organize_music()
    generate_playlist_json()
