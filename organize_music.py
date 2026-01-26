"""
Music Organizer for SaasuFy
Organizes downloaded songs into playlist folders
"""

import os
import shutil
import json
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

# Define playlist categories based on song mood/theme
PLAYLISTS = {
    'neet-warrior': {
        'folder': 'music/neet-warrior',
        'songs': [
            # Motivational & Energetic
            '27 - Unstoppable.mp3',
            '44 - Hall of Fame.mp3',
            '29 - Nee Singam Dhan.mp3',
            '30 - Powerhouse (From ＂Coolie＂) (Tamil).mp3',
            '31 - SNAP.mp3',
            '14 - Amplifier.mp3',
            '35 - Rasputin.mp3',
            '61 - Running Up That Hill (A Deal With God).mp3',
            '28 - 7 Years.mp3',
            '43 - End of Beginning.mp3',
            'Immigrant Song (Remaster).mp3',
            'King Shit.mp3',
            'Backbone.mp3',
            'Bones.mp3',
            '8 Parche.mp3',
            'Pathu Thala - Nee Singam Dhan Video ｜ Silambarasan TR ｜ A. R Rahman ｜ Gautham Karthik.mp3'
        ]
    },
    'chef-specials': {
        'folder': 'music/chef-specials',
        'songs': [
            # Upbeat, Fun & Energetic
            '37 - Instant Cooker Paneer Recipe #Shorts.mp3',
            '48 - Everything at Once.mp3',
            '46 - Dance Monkey.mp3',
            '51 - Espresso.mp3',
            '60 - Lahore.mp3',
            '15 - Libaas.mp3',
            '16 - Teeji Seat.mp3',
            '17 - Mitti De Tibbe.mp3',
            '56 - Temporary Pyar.mp3',
            '32 - Heeriye (feat. Arijit Singh).mp3',
            '33 - Wellerman (Sea Shanty).mp3',
            '36 - Татьяна Куртукова - Матушка.mp3',
            '40 - As It Was.mp3',
            '50 - Alone, Pt. II.mp3',
            '55 - Ya Lili.mp3',
            '62 - Callin\' U (Tamally Maak).mp3',
            'Cupid - Twin Ver. (FIFTY FIFTY) (Sped Up Version).mp3',
            'On & On.mp3',
            'Pagol (feat. Bohemia).mp3',
            'Soni Soni (From ＂Ishq Vishk Rebound＂).mp3',
            'Yimmy Yimmy.mp3',
            'TANDOORI NIGHTS.mp3',
            'Channa Ve.mp3',
            'Chellakuttiye (Avastha Love Song).mp3',
            'Chitthi.mp3',
            'Ek Ladki Bheegi Bhaagi Si ｜ Kishore Kumar ｜ Madhubala ｜ Chalti Ka Naam Gaadi (1958) ｜ Old Hit Song.mp3'
        ]
    },
    'soft-break': {
        'folder': 'music/soft-break',
        'songs': [
            # Emotional, Slow & Melancholic
            '08 - Let Her Go (Anniversary Edition).mp3',
            '45 - A Thousand Years.mp3',
            '47 - somewhere only we know.mp3',
            '59 - The Night We Met.mp3',
            '05 - Until I Found You (Em Beihold Version).mp3',
            '06 - Dancing With Your Ghost.mp3',
            '34 - Khairiyat.mp3',
            '24 - Tera Yaar Hoon Main.mp3',
            '49 - Let Me Down Slowly.mp3',
            '63 - Dandelions.mp3',
            '09 - Broken Angel - Feat. Helena.mp3',
            '10 - Alan Walker, K-391 & Emelie Hollow - Lily (Lyrics).mp3',
            '13 - Sapphire.mp3',
            '26 - happier.mp3',
            '38 - Play Date.mp3',
            '39 - Spirits.mp3',
            '42 - I Think They Call This Love (Cover).mp3',
            '52 - People You Know.mp3',
            '53 - People.mp3',
            '54 - Bad Liar.mp3',
            '57 - Dido - Thank You (Thunderstorm Remix Louder).mp3',
            '58 - Forever Young (2019 Remaster).mp3',
            'Dido - Thank You (Thunderstorm Remix Louder).mp3',
            'Forever Young (2019 Remaster).mp3',
            'Your Eyes.mp3',
            'Fairytale.mp3',
            'Skyfall.mp3',
            'Sajni.mp3',
            'Suzume (feat. Toaka).mp3'
        ]
    },
    'bahurani-picks': {
        'folder': 'music/bahurani-picks',
        'songs': [
            # Romantic & Popular Hits
            '12 - Die With A Smile.mp3',
            '02 - Skyfall.mp3',
            '04 - Fairytale.mp3',
            '07 - I Wanna Be Yours.mp3',
            '11 - Summertime Sadness.mp3',
            '18 - We Don\'t Talk Anymore (feat. Selena Gomez).mp3',
            '19 - Attention.mp3',
            '21 - STAY.mp3',
            '25 - Arcade.mp3',
            '41 - Love Me Like You Do (From ＂Fifty Shades Of Grey＂).mp3',
            '20 - Marshmello & Anne-Marie - FRIENDS (Lyrics).mp3',
            '22 - Let Me Love You.mp3',
            '23 - Intentions.mp3',
            # Bollywood Romantic
            'Aa Zara.mp3',
            'Aapke Pyaar Mein Hum.mp3',
            'Ab Tere Dil Mein To.mp3',
            'Adharam Madhuram (Slowed Lofi).mp3',
            'Agar Tum Mil Jao (From ＂Zeher＂).mp3',
            'Ajab Si.mp3',
            'Apna Bana Le (From ＂Bhediya＂).mp3',
            'Aye Mere Humsafar.mp3',
            'BEKHUDI.mp3',
            'Bahara.mp3',
            'Bol Do Na Zara.mp3',
            'Bol Na Halke Halke.mp3',
            'Bulleya (From ＂Sultan＂).mp3',
            'Chal Wahan Jaate Hain.mp3',
            'Chale Aana (From ＂De De Pyaar De＂).mp3',
            'Chand Sifarish.mp3',
            'Darmiyaan.mp3',
            'Dekha Hazaro Dafaa.mp3',
            'Dekhha Tenu (From ＂Mr. And Mrs. Mahi＂).mp3',
            'Dil Hi Toh Hai.mp3',
            'Dil Ibaadat.mp3',
            'Dil Meri Na Sune.mp3',
            'DIL KE BADLE SANAM.mp3',
            'DIL TO BACHCHA HAI.mp3',
            'DUPATTA TERA NAU RANG DA.mp3',
            'Do Pal.mp3',
            'Halka Halka (From ＂Fanney Khan＂).mp3',
            'Ho Gaya Hai Tujhko To Pyar Sajna.mp3',
            'Hua Main.mp3',
            'Hum Nashe Mein Toh Nahin.mp3',
            'Jaana Samjho Na.mp3',
            'Jadoo Ki Jhappi.mp3',
            'Jeene Laga Hoon.mp3',
            'Kabhii Tumhhe.mp3',
            'Kaise Hua.mp3',
            'Khamoshiyan.mp3',
            'Koi Naa (From ＂Bhool Chuk Maaf＂).mp3',
            'MAIN WOH CHAAND.mp3',
            'Main Yahaan Hoon.mp3',
            'Maiyya Mainu.mp3',
            'Mehrama (From ＂Love Aaj Kal＂).mp3',
            'Mehrama.mp3',
            'Mere Haath Mein.mp3',
            'Muskurane (Romantic).mp3',
            'Nazm Nazm.mp3',
            'PHIR KABHI.mp3',
            'Panna Ki Tamanna Hai.mp3',
            'Pee Loon Lofi Mix (Remix By Kedrock,Sd Style).mp3',
            'Pehle to Kabhi Kabhi.mp3',
            'Pehli Nazar Mein.mp3',
            'Phir Bhi Tumko Chaahunga.mp3',
            'Phir Chala.mp3',
            'Phir Mohabbat.mp3',
            'Qaafirana.mp3',
            'Saiyaara.mp3',
            'Satranga.mp3',
            'Sochenge Tumhe Pyar (From ＂Deewana＂).mp3',
            'Subhanallah (From ＂Yeh Jawaani Hai Deewani＂).mp3',
            'TUM JO AAYE.mp3',
            'TUM SE HI.mp3',
            'Tera Fitoor.mp3',
            'Tere Liye.mp3',
            'Tere Sang Yaara.mp3',
            'Teri Meri.mp3',
            'Tum Hi Aana (From ＂Marjaavaan＂).mp3',
            'Tum Kya Mile (From ＂Rocky Aur Rani Kii Prem Kahaani＂).mp3',
            'Tumhare Hi Rahenge Hum (From ＂Stree 2＂).mp3',
            'WAFA NE BEWAFAI.mp3',
            'Woh Ladki Bahut Yaad Aati.mp3',
            'ZINDAGI KUCH TOH BATA - REPRISEW-IN.mp3'
        ]
    },
    'morning-walk': {
        'folder': 'music/morning-walk',
        'source_playlists': {
            # Fresh, uplifting morning vibes
            'Everything at Once.mp3': 'music/chef-specials/Everything at Once.mp3',
            'somewhere only we know.mp3': 'music/soft-break/somewhere only we know.mp3',
            'Fairytale.mp3': 'music/soft-break/Fairytale.mp3',
            'Dandelions.mp3': 'music/soft-break/Dandelions.mp3',
            'Espresso.mp3': 'music/chef-specials/Espresso.mp3',
            '7 Years.mp3': 'music/neet-warrior/7 Years.mp3',
            'Dance Monkey.mp3': 'music/chef-specials/Dance Monkey.mp3',
            'As It Was.mp3': 'music/chef-specials/As It Was.mp3',
            'Wellerman (Sea Shanty).mp3': 'music/chef-specials/Wellerman (Sea Shanty).mp3',
            'Ya Lili.mp3': 'music/chef-specials/Ya Lili.mp3',
            'Yimmy Yimmy.mp3': 'music/chef-specials/Yimmy Yimmy.mp3',
            'Soni Soni (From ＂Ishq Vishk Rebound＂).mp3': 'music/chef-specials/Soni Soni (From ＂Ishq Vishk Rebound＂).mp3',
            'End of Beginning.mp3': 'music/neet-warrior/End of Beginning.mp3',
            'Intentions.mp3': 'music/bahurani-picks/Intentions.mp3',
            'STAY.mp3': 'music/bahurani-picks/STAY.mp3'
        }
    },
    'chai-and-chill': {
        'folder': 'music/chai-and-chill',
        'source_playlists': {
            # Cozy, relaxing evening songs
            'Let Her Go (Anniversary Edition).mp3': 'music/soft-break/Let Her Go (Anniversary Edition).mp3',
            'A Thousand Years.mp3': 'music/soft-break/A Thousand Years.mp3',
            'Khairiyat.mp3': 'music/soft-break/Khairiyat.mp3',
            'Tera Yaar Hoon Main.mp3': 'music/soft-break/Tera Yaar Hoon Main.mp3',
            'Heeriye (feat. Arijit Singh).mp3': 'music/chef-specials/Heeriye (feat. Arijit Singh).mp3',
            'Arcade.mp3': 'music/bahurani-picks/Arcade.mp3',
            'The Night We Met.mp3': 'music/soft-break/The Night We Met.mp3',
            'Dancing With Your Ghost.mp3': 'music/soft-break/Dancing With Your Ghost.mp3',
            'Let Me Down Slowly.mp3': 'music/soft-break/Let Me Down Slowly.mp3',
            'Sajni.mp3': 'music/soft-break/Sajni.mp3',
            'Kabhii Tumhhe.mp3': 'music/bahurani-picks/Kabhii Tumhhe.mp3',
            'Kaise Hua.mp3': 'music/bahurani-picks/Kaise Hua.mp3',
            'Nazm Nazm.mp3': 'music/bahurani-picks/Nazm Nazm.mp3',
            'Tum Hi Aana (From ＂Marjaavaan＂).mp3': 'music/bahurani-picks/Tum Hi Aana (From ＂Marjaavaan＂).mp3',
            'Satranga.mp3': 'music/bahurani-picks/Satranga.mp3'
        }
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
        
        # Check if this is a curated playlist (copies from other playlists)
        if 'source_playlists' in playlist_data:
            print(f"\n📋 Curating {playlist_id}...")
            for dest_name, source_path in playlist_data['source_playlists'].items():
                dest_path = os.path.join(folder, dest_name)
                
                if os.path.exists(source_path):
                    shutil.copy2(source_path, dest_path)
                    print(f"  ✓ Copied: {dest_name}")
                else:
                    print(f"  ⚠️  Source not found: {source_path}")
        else:
            # Regular playlist - copy from downloaded_songs
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
    print("    ├── bahurani-picks/")
    print("    ├── morning-walk/")
    print("    └── chai-and-chill/")
    print("\n📁 You can now use these songs in the SaasuFy app!")

def get_mp3_metadata(file_path):
    """Extract duration and artist from MP3 file"""
    try:
        audio = MP3(file_path)
        
        # Get duration in MM:SS format
        duration_seconds = int(audio.info.length)
        minutes = duration_seconds // 60
        seconds = duration_seconds % 60
        duration = f"{minutes}:{seconds:02d}"
        
        # Get artist from ID3 tags
        artist = "Unknown Artist"
        try:
            tags = ID3(file_path)
            if 'TPE1' in tags:  # TPE1 is the artist tag
                artist = str(tags['TPE1'])
            elif 'TPE2' in tags:  # TPE2 is the album artist tag
                artist = str(tags['TPE2'])
        except:
            pass
        
        return duration, artist
    except Exception as e:
        print(f"  ⚠️  Could not read metadata: {e}")
        return "0:00", "Unknown Artist"

def generate_playlist_json():
    """Generate JSON file with playlist data for the web app"""
    
    playlist_data = {}
    
    for playlist_id, playlist_info in PLAYLISTS.items():
        folder = playlist_info['folder']
        songs = []
        
        print(f"\n📝 Processing {playlist_id}...")
        
        # Check if this is a curated playlist
        if 'source_playlists' in playlist_info:
            # For curated playlists, use the destination filenames
            for dest_name in playlist_info['source_playlists'].keys():
                title = dest_name.replace('.mp3', '')
                file_path = os.path.join(folder, dest_name)
                
                # Get metadata
                duration, artist = get_mp3_metadata(file_path)
                
                songs.append({
                    'title': title,
                    'artist': artist,
                    'file': f"{folder}/{dest_name}",
                    'duration': duration
                })
                
                print(f"  ✓ {title} - {artist} ({duration})")
        else:
            # Regular playlist
            for song_file in playlist_info['songs']:
                # Clean filename
                if ' - ' in song_file:
                    clean_name = ' - '.join(song_file.split(' - ')[1:])
                else:
                    clean_name = song_file
                
                title = clean_name.replace('.mp3', '')
                file_path = os.path.join(folder, clean_name)
                
                # Get metadata
                duration, artist = get_mp3_metadata(file_path)
                
                songs.append({
                    'title': title,
                    'artist': artist,
                    'file': f"{folder}/{clean_name}",
                    'duration': duration
                })
                
                print(f"  ✓ {title} - {artist} ({duration})")
        
        playlist_data[playlist_id] = songs
    
    # Save to JSON file
    with open('playlists.json', 'w', encoding='utf-8') as f:
        json.dump(playlist_data, f, indent=2, ensure_ascii=False)
    
    print("\n✓ Generated playlists.json with metadata")

if __name__ == "__main__":
    organize_music()
    generate_playlist_json()
