
const fs = require('fs');
const path = require('path');

try {
    const playlistContent = fs.readFileSync(path.join(__dirname, 'playlist_data.js'), 'utf8');
    
    const start = playlistContent.indexOf('{');
    const end = playlistContent.lastIndexOf('}');
    
    if (start === -1 || end === -1) {
        throw new Error("Could not find object in file");
    }

    const objectString = playlistContent.substring(start, end + 1);
    
    // Evaluate the string to get the object
    const data = eval(`(${objectString})`);
    
    fs.writeFileSync(path.join(__dirname, 'playlist.json'), JSON.stringify(data, null, 2), 'utf8');
    console.log("Successfully wrote playlist.json");
} catch (e) {
    console.error(e);
    process.exit(1);
}
