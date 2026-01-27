
import os
import json
import difflib

def load_playlist_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        # Remove the variable declaration to parse key JSON
        json_content = content.replace('const PLAYLIST_DATA = ', '').strip().rstrip(';')
        # Fix trailing commas which are valid in JS objects but not JSON
        # This is a simple regex fix or we can use a library if available, but let's try a simple approach
        # actually, let's just use exec since it is a JS object literal
        # strict JSON parsing might fail on keys without quotes or trailing commas
        # But looking at the file, keys are quoted. Trailing commas might be an issue.
        # Let's try to parse it as python dict by some replacements
        import ast
        try:
             # This might be dangerous if file has malicious code, but assuming it's data
             # playlist_data.js seems to differ from python syntax (true/false, null)
             # but here we only have strings and arrays.
             data = json.loads(json_content)
             return data
        except json.JSONDecodeError:
            # Fallback: simple manual parsing or dirty fix
            # Let's try to clean it up for JSON
            import re
            json_content = re.sub(r',\s*([\]}])', r'\1', json_content) # remove trailing commas
            return json.loads(json_content)

def check_files(data, base_dir):
    missing_files = []
    
    # Get all actual files in music dir for fuzzy matching
    actual_files = {}
    for root, dirs, files in os.walk(os.path.join(base_dir, 'music')):
        for file in files:
            # Create relative path matching the structure in playlist_data
            rel_path = os.path.relpath(os.path.join(root, file), base_dir).replace('\\', '/')
            actual_files[rel_path] = file

    print(f"Index created with {len(actual_files)} files.")

    for playlist_name, songs in data.items():
        for song in songs:
            file_path = song.get('file')
            full_path = os.path.join(base_dir, file_path)
            
            if not os.path.exists(full_path):
                # File missing
                print(f"MISSING: {file_path}")
                
                # unexpected encoding characters?
                # suggest fix
                suggestion = difflib.get_close_matches(file_path, actual_files.keys(), n=1, cutoff=0.6)
                if suggestion:
                    print(f"  SUGGESTION: {suggestion[0]}")
                    missing_files.append((playlist_name, song['title'], file_path, suggestion[0]))
                else:
                    print("  NO MATCH FOUND")
                    missing_files.append((playlist_name, song['title'], file_path, None))
            else:
                # print(f"OK: {file_path}")
                pass
    
    return missing_files

if __name__ == "__main__":
    base_dir = r"c:\Users\anuna\OneDrive\Desktop\Haze"
    playlist_file = os.path.join(base_dir, "playlist_data.js")
    
    try:
        data = load_playlist_data(playlist_file)
        missing = check_files(data, base_dir)
        
        print("\nSUMMARY:")
        print(f"Found {len(missing)} missing files.")
        
        if missing:
            print("\nGenerating fix script...")
            # We can generate a mapping json to be used by another script to patch playlist_data.js
            with open(os.path.join(base_dir, "missing_songs_fix.json"), "w", encoding='utf-8') as f:
                json.dump(missing, f, indent=2)
            print("Fix mapping saved to missing_songs_fix.json")
            
    except Exception as e:
        print(f"Error: {e}")
