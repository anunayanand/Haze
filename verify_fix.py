
import os
import re

def verify_playlist(base_dir):
    playlist_path = os.path.join(base_dir, "playlist_data.js")
    with open(playlist_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex to find paths
    # We use the same regex that worked in fix_playlist.py or a simpler one since we trust the file structure more now
    # But wait, looking at the previous regex: r'file.*?[:=].*?(music/[^\s"\'<>]+)'
    # It might be too loose.
    # Let's try to extract paths assuming standard format now.
    
    paths = re.findall(r'"file":\s*"(music/[^"]+)"', content)
    
    missing = []
    for path in paths:
        full_path = os.path.join(base_dir, path)
        if not os.path.exists(full_path):
            missing.append(path)
            
    return missing

if __name__ == "__main__":
    base_dir = r"c:\Users\anuna\OneDrive\Desktop\Haze"
    missing = verify_playlist(base_dir)
    
    if missing:
        print(f"Found {len(missing)} missing files:")
        for m in missing:
            print(f"  {m}")
    else:
        print("All songs found on disk!")
