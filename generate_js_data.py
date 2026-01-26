"""
Generate JavaScript playlist data from playlists.json
This script reads playlists.json and generates the PLAYLIST_DATA constant for app.js
"""

import json

# Read playlists.json
with open('playlists.json', 'r', encoding='utf-8') as f:
    playlists = json.load(f)

# Generate JavaScript code
js_code = "// Embedded playlist data (to avoid CORS issues with file:// protocol)\nconst PLAYLIST_DATA = "
js_code += json.dumps(playlists, indent=2, ensure_ascii=False)
js_code += ";\n"

# Write to a temporary file
with open('playlist_data.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("✓ Generated playlist_data.js")
print(f"  Total playlists: {len(playlists)}")
for playlist_id, songs in playlists.items():
    print(f"  - {playlist_id}: {len(songs)} songs")
