// ========================================
// SaasuFy - Real Music Player
// With HTML5 Audio Integration
// ========================================

// ========================================
// Global State
// ========================================

let currentPlaylist = 'neet-warrior';
let currentSongIndex = 0;
let isPlaying = false;
let playlists = {};
let audio = null;

// Embedded playlist data (to avoid CORS issues with file:// protocol)
const PLAYLIST_DATA = {
  "neet-warrior": [
    {"title": "Unstoppable", "artist": "Sia", "file": "music/neet-warrior/Unstoppable.mp3", "duration": "3:37"},
    {"title": "Hall of Fame", "artist": "The Script ft. will.i.am", "file": "music/neet-warrior/Hall of Fame.mp3", "duration": "3:21"},
    {"title": "Nee Singam Dhan", "artist": "Anirudh Ravichander", "file": "music/neet-warrior/Nee Singam Dhan.mp3", "duration": "4:07"},
    {"title": "Powerhouse", "artist": "Anirudh Ravichander", "file": "music/neet-warrior/Powerhouse (From ＂Coolie＂) (Tamil).mp3", "duration": "3:26"},
    {"title": "SNAP", "artist": "Rosa Linn", "file": "music/neet-warrior/SNAP.mp3", "duration": "2:59"},
    {"title": "Amplifier", "artist": "Imran Khan", "file": "music/neet-warrior/Amplifier.mp3", "duration": "3:52"},
    {"title": "Rasputin", "artist": "Boney M.", "file": "music/neet-warrior/Rasputin.mp3", "duration": "5:51"},
    {"title": "Running Up That Hill", "artist": "Kate Bush", "file": "music/neet-warrior/Running Up That Hill (A Deal With God).mp3", "duration": "4:58"},
    {"title": "7 Years", "artist": "Lukas Graham", "file": "music/neet-warrior/7 Years.mp3", "duration": "3:57"},
    {"title": "End of Beginning", "artist": "Djo", "file": "music/neet-warrior/End of Beginning.mp3", "duration": "2:39"}
  ],
  "chef-specials": [
    {"title": "Everything at Once", "artist": "Lenka", "file": "music/chef-specials/Everything at Once.mp3", "duration": "2:37"},
    {"title": "Dance Monkey", "artist": "Tones and I", "file": "music/chef-specials/Dance Monkey.mp3", "duration": "3:29"},
    {"title": "Espresso", "artist": "Sabrina Carpenter", "file": "music/chef-specials/Espresso.mp3", "duration": "2:55"},
    {"title": "Lahore", "artist": "Guru Randhawa", "file": "music/chef-specials/Lahore.mp3", "duration": "3:17"},
    {"title": "Libaas", "artist": "Kaka", "file": "music/chef-specials/Libaas.mp3", "duration": "4:27"},
    {"title": "Teeji Seat", "artist": "Ammy Virk", "file": "music/chef-specials/Teeji Seat.mp3", "duration": "2:24"},
    {"title": "Mitti De Tibbe", "artist": "Ammy Virk", "file": "music/chef-specials/Mitti De Tibbe.mp3", "duration": "4:33"},
    {"title": "Temporary Pyar", "artist": "Kaka", "file": "music/chef-specials/Temporary Pyar.mp3", "duration": "4:12"},
    {"title": "Heeriye (feat. Arijit Singh)", "artist": "Jasleen Royal, Arijit Singh", "file": "music/chef-specials/Heeriye (feat. Arijit Singh).mp3", "duration": "3:14"}
  ],
  "soft-break": [
    {"title": "Let Her Go", "artist": "Passenger", "file": "music/soft-break/Let Her Go (Anniversary Edition).mp3", "duration": "4:16"},
    {"title": "A Thousand Years", "artist": "Christina Perri", "file": "music/soft-break/A Thousand Years.mp3", "duration": "3:32"},
    {"title": "Somewhere Only We Know", "artist": "Keane", "file": "music/soft-break/somewhere only we know.mp3", "duration": "3:06"},
    {"title": "The Night We Met", "artist": "Lord Huron", "file": "music/soft-break/The Night We Met.mp3", "duration": "3:16"},
    {"title": "Until I Found You (Em Beihold Version)", "artist": "Stephen Sanchez, Em Beihold", "file": "music/soft-break/Until I Found You (Em Beihold Version).mp3", "duration": "2:56"},
    {"title": "Dancing With Your Ghost", "artist": "Sasha Alex Sloan", "file": "music/soft-break/Dancing With Your Ghost.mp3", "duration": "3:17"},
    {"title": "Khairiyat", "artist": "Arijit Singh", "file": "music/soft-break/Khairiyat.mp3", "duration": "4:40"},
    {"title": "Tera Yaar Hoon Main", "artist": "Arijit Singh", "file": "music/soft-break/Tera Yaar Hoon Main.mp3", "duration": "4:24"},
    {"title": "Let Me Down Slowly", "artist": "Alec Benjamin", "file": "music/soft-break/Let Me Down Slowly.mp3", "duration": "2:49"},
    {"title": "Dandelions", "artist": "Ruth B.", "file": "music/soft-break/Dandelions.mp3", "duration": "3:53"}
  ],
  "bahurani-picks": [
    {"title": "Die With A Smile", "artist": "Lady Gaga, Bruno Mars", "file": "music/bahurani-picks/Die With A Smile.mp3", "duration": "4:11"},
    {"title": "Skyfall", "artist": "Adele", "file": "music/bahurani-picks/Skyfall.mp3", "duration": "4:46"},
    {"title": "Fairytale", "artist": "Alexander Rybak", "file": "music/bahurani-picks/Fairytale.mp3", "duration": "3:02"},
    {"title": "I Wanna Be Yours", "artist": "Arctic Monkeys", "file": "music/bahurani-picks/I Wanna Be Yours.mp3", "duration": "3:03"},
    {"title": "Summertime Sadness", "artist": "Lana Del Rey", "file": "music/bahurani-picks/Summertime Sadness.mp3", "duration": "4:24"},
    {"title": "We Don't Talk Anymore", "artist": "Charlie Puth ft. Selena Gomez", "file": "music/bahurani-picks/We Don't Talk Anymore (feat. Selena Gomez).mp3", "duration": "3:37"},
    {"title": "Attention", "artist": "Charlie Puth", "file": "music/bahurani-picks/Attention.mp3", "duration": "3:31"},
    {"title": "STAY", "artist": "The Kid LAROI, Justin Bieber", "file": "music/bahurani-picks/STAY.mp3", "duration": "2:21"},
    {"title": "Arcade", "artist": "Duncan Laurence", "file": "music/bahurani-picks/Arcade.mp3", "duration": "3:07"},
    {"title": "Love Me Like You Do", "artist": "Ellie Goulding", "file": "music/bahurani-picks/Love Me Like You Do (From ＂Fifty Shades Of Grey＂).mp3", "duration": "4:12"}
  ],
  "morning-walk": [
    {"title": "Everything at Once", "artist": "Lenka", "file": "music/chef-specials/Everything at Once.mp3", "duration": "2:37"},
    {"title": "Somewhere Only We Know", "artist": "Keane", "file": "music/soft-break/somewhere only we know.mp3", "duration": "3:06"},
    {"title": "Fairytale", "artist": "Alexander Rybak", "file": "music/bahurani-picks/Fairytale.mp3", "duration": "3:02"},
    {"title": "Dandelions", "artist": "Ruth B.", "file": "music/soft-break/Dandelions.mp3", "duration": "3:53"},
    {"title": "Espresso", "artist": "Sabrina Carpenter", "file": "music/chef-specials/Espresso.mp3", "duration": "2:55"},
    {"title": "7 Years", "artist": "Lukas Graham", "file": "music/neet-warrior/7 Years.mp3", "duration": "3:57"}
  ],
  "chai-and-chill": [
    {"title": "Let Her Go", "artist": "Passenger", "file": "music/soft-break/Let Her Go (Anniversary Edition).mp3", "duration": "4:16"},
    {"title": "A Thousand Years", "artist": "Christina Perri", "file": "music/soft-break/A Thousand Years.mp3", "duration": "3:32"},
    {"title": "Khairiyat", "artist": "Arijit Singh", "file": "music/soft-break/Khairiyat.mp3", "duration": "4:40"},
    {"title": "Tera Yaar Hoon Main", "artist": "Arijit Singh", "file": "music/soft-break/Tera Yaar Hoon Main.mp3", "duration": "4:24"},
    {"title": "Heeriye (feat. Arijit Singh)", "artist": "Jasleen Royal, Arijit Singh", "file": "music/chef-specials/Heeriye (feat. Arijit Singh).mp3", "duration": "3:14"},
    {"title": "Arcade", "artist": "Duncan Laurence", "file": "music/bahurani-picks/Arcade.mp3", "duration": "3:07"}
  ]
};

async function loadPlaylists() {
    try {
        // Use embedded data instead of fetch
        const data = PLAYLIST_DATA;
        
        // Transform data to match our app structure
        for (const [playlistId, songs] of Object.entries(data)) {
            playlists[playlistId] = {
                title: getPlaylistTitle(playlistId),
                icon: getPlaylistIcon(playlistId),
                gradient: getPlaylistGradient(playlistId),
                tags: getPlaylistTags(playlistId),
                songs: songs.map((song, index) => ({
                    title: song.title,
                    artist: song.artist,
                    duration: song.duration,
                    file: song.file
                }))
            };
        }
        
        console.log('✓ Playlists loaded:', Object.keys(playlists).length);
        return true;
    } catch (error) {
        console.error('Error loading playlists:', error);
        return false;
    }
}

function getPlaylistTitle(id) {
    const titles = {
        'neet-warrior': 'NEET Warrior Mode',
        'chef-specials': 'Chef Saasu Maa Specials',
        'soft-break': 'Soft Break Time',
        'bahurani-picks': "Bahurani's Picks",
        'morning-walk': 'Morning Walk',
        'chai-and-chill': 'Chai & Chill'
    };
    return titles[id] || id;
}

function getPlaylistIcon(id) {
    const icons = {
        'neet-warrior': 'bi-activity',
        'chef-specials': 'bi-egg-fried',
        'soft-break': 'bi-cup-hot',
        'bahurani-picks': 'bi-heart-fill',
        'morning-walk': 'bi-sunrise',
        'chai-and-chill': 'bi-cup-straw'
    };
    return icons[id] || 'bi-music-note';
}

function getPlaylistGradient(id) {
    const gradients = {
        'neet-warrior': 'gradient-1',
        'chef-specials': 'gradient-2',
        'soft-break': 'gradient-3',
        'bahurani-picks': 'gradient-4',
        'morning-walk': 'gradient-1',
        'chai-and-chill': 'gradient-3'
    };
    return gradients[id] || 'gradient-1';
}

function getPlaylistTags(id) {
    const tags = {
        'neet-warrior': ['Study', 'Focus', 'Hype'],
        'chef-specials': ['Cooking', 'Soft', 'Love'],
        'soft-break': ['Soft', 'Relax', 'Break'],
        'bahurani-picks': ['Love', 'Special', 'Bahurani'],
        'morning-walk': ['Fresh', 'Uplifting', 'Morning'],
        'chai-and-chill': ['Cozy', 'Relax', 'Evening']
    };
    return tags[id] || ['Music'];
}

// ========================================
// Audio Player Functions
// ========================================

function initAudioPlayer() {
    audio = document.getElementById('audioPlayer');
    
    // Audio event listeners
    audio.addEventListener('loadedmetadata', () => {
        updateDuration();
    });
    
    audio.addEventListener('timeupdate', () => {
        updateProgress();
    });
    
    audio.addEventListener('ended', () => {
        skipNext();
    });
    
    audio.addEventListener('error', (e) => {
        console.error('Audio error:', e);
        // Try next song on error
        skipNext();
    });
}

function loadSong(playlistId, songIndex) {
    const playlist = playlists[playlistId];
    if (!playlist || !playlist.songs[songIndex]) return;
    
    const song = playlist.songs[songIndex];
    
    // Load audio file
    audio.src = song.file;
    audio.load();
    
    // Update UI
    updateNowPlaying();
}

function updateNowPlaying() {
    const playlist = playlists[currentPlaylist];
    if (!playlist) return;
    
    const song = playlist.songs[currentSongIndex];
    
    // Update track info in Now Playing bar
    const trackNameElements = document.querySelectorAll('.track-name');
    const artistNameElements = document.querySelectorAll('.artist-name');
    
    trackNameElements.forEach(el => el.textContent = song.title);
    artistNameElements.forEach(el => el.textContent = song.artist || 'Unknown Artist');
    
    // Update thumbnail gradient in Now Playing bar
    const thumbnails = document.querySelectorAll('.now-playing-thumbnail');
    thumbnails.forEach(thumb => {
        thumb.className = 'now-playing-thumbnail ' + playlist.gradient;
        thumb.innerHTML = `<i class="bi ${playlist.icon}"></i>`;
    });
}

function updateDuration() {
    if (!audio || !audio.duration) return;
    
    const minutes = Math.floor(audio.duration / 60);
    const seconds = Math.floor(audio.duration % 60);
    const duration = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    
    // Update duration in playlist if visible
    const playlist = playlists[currentPlaylist];
    if (playlist && playlist.songs[currentSongIndex]) {
        playlist.songs[currentSongIndex].duration = duration;
    }
}

function updateProgress() {
    if (!audio || !audio.duration) return;
    
    const progress = (audio.currentTime / audio.duration) * 100;
    const progressBar = document.querySelector('.progress-bar-fill');
    if (progressBar) {
        progressBar.style.width = progress + '%';
    }
    
    // Update time displays
    const currentTime = formatTime(audio.currentTime);
    const totalTime = formatTime(audio.duration);
    
    const currentTimeEl = document.querySelector('.time-current');
    const totalTimeEl = document.querySelector('.time-total');
    
    if (currentTimeEl) currentTimeEl.textContent = currentTime;
    if (totalTimeEl) totalTimeEl.textContent = totalTime;
}

function formatTime(seconds) {
    if (!seconds || isNaN(seconds)) return '--:--';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function togglePlay() {
    if (!audio || !audio.src) {
        // Load first song if nothing is loaded
        loadSong(currentPlaylist, 0);
        return;
    }
    
    if (isPlaying) {
        audio.pause();
        isPlaying = false;
        updatePlayButton(false);
    } else {
        audio.play().then(() => {
            isPlaying = true;
            updatePlayButton(true);
        }).catch(err => {
            console.error('Play error:', err);
        });
    }
}

function updatePlayButton(playing) {
    const playBtns = document.querySelectorAll('.play-btn-large i');
    playBtns.forEach(icon => {
        if (playing) {
            icon.classList.remove('bi-play-fill', 'bi-play-circle-fill');
            icon.classList.add('bi-pause-circle-fill');
        } else {
            icon.classList.remove('bi-pause-circle-fill');
            icon.classList.add('bi-play-circle-fill');
        }
    });
}

function skipPrevious() {
    const playlist = playlists[currentPlaylist];
    if (!playlist) return;
    
    currentSongIndex = (currentSongIndex - 1 + playlist.songs.length) % playlist.songs.length;
    loadSong(currentPlaylist, currentSongIndex);
    
    if (isPlaying) {
        audio.play();
    }
}

function skipNext() {
    const playlist = playlists[currentPlaylist];
    if (!playlist) return;
    
    currentSongIndex = (currentSongIndex + 1) % playlist.songs.length;
    loadSong(currentPlaylist, currentSongIndex);
    
    if (isPlaying) {
        audio.play();
    }
}

// ========================================
// Screen Navigation
// ========================================

function switchScreen(screenName) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    
    const screenId = screenName + '-screen';
    document.getElementById(screenId).classList.add('active');
    
    // Update sidebar navigation
    document.querySelectorAll('.sidebar-nav .nav-link').forEach(item => {
        item.classList.remove('active');
    });
    
    // Update bottom navigation
    document.querySelectorAll('.bottom-nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Find and activate the correct nav links
    const navLinks = document.querySelectorAll('.sidebar-nav .nav-link');
    const bottomNavItems = document.querySelectorAll('.bottom-nav-item');
    
    if (screenName === 'home') {
        if (navLinks[0]) navLinks[0].classList.add('active');
        if (bottomNavItems[0]) bottomNavItems[0].classList.add('active');
    }
    if (screenName === 'wrapped') {
        if (navLinks[1]) navLinks[1].classList.add('active');
        if (bottomNavItems[1]) bottomNavItems[1].classList.add('active');
    }
    if (screenName === 'gift') {
        if (navLinks[2]) navLinks[2].classList.add('active');
        if (bottomNavItems[3]) bottomNavItems[3].classList.add('active');
    }
}

// ========================================
// Playlist Functions
// ========================================

function openPlaylist(playlistId) {
    currentPlaylist = playlistId;
    loadPlaylistView(playlistId);
    
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById('playlist-screen').classList.add('active');
    
    // Update sidebar navigation
    document.querySelectorAll('.sidebar-nav .nav-link').forEach(item => {
        item.classList.remove('active');
    });
    
    // Update bottom navigation
    document.querySelectorAll('.bottom-nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Activate playlist button in bottom nav
    const bottomNavItems = document.querySelectorAll('.bottom-nav-item');
    if (bottomNavItems[2]) bottomNavItems[2].classList.add('active');
}

function loadPlaylistView(playlistId) {
    const playlist = playlists[playlistId];
    if (!playlist) return;
    
    // Update playlist title
    const titleEl = document.getElementById('playlistDetailTitle');
    if (titleEl) titleEl.textContent = playlist.title;
    
    // Update album grid
    const albumGrid = document.getElementById('playlistAlbumGrid');
    if (albumGrid) {
        albumGrid.innerHTML = '';
        for (let i = 0; i < 4; i++) {
            const gridItem = document.createElement('div');
            gridItem.className = `album-grid-item ${playlist.gradient}`;
            gridItem.innerHTML = `<i class="bi ${playlist.icon}"></i>`;
            albumGrid.appendChild(gridItem);
        }
    }
    
    // Update metadata
    const trackCountEl = document.getElementById('playlistTrackCount');
    if (trackCountEl) trackCountEl.textContent = `${playlist.songs.length} tracks`;
    
    // Calculate total duration
    let totalSeconds = 0;
    playlist.songs.forEach(song => {
        if (song.duration && song.duration !== '0:00') {
            const parts = song.duration.split(':');
            totalSeconds += parseInt(parts[0]) * 60 + parseInt(parts[1]);
        }
    });
    const totalMinutes = Math.floor(totalSeconds / 60);
    const durationEl = document.getElementById('playlistDuration');
    if (durationEl) durationEl.textContent = `${totalMinutes} min`;
    
    // Update song list with detailed view
    const songListContainer = document.getElementById('songListDetailed');
    if (songListContainer) {
        songListContainer.innerHTML = playlist.songs.map((song, index) => `
            <div class="song-item-detailed" onclick="playSong(${index})">
                <div class="song-number">${index + 1}</div>
                <div class="song-thumbnail ${playlist.gradient}">
                    <i class="bi ${playlist.icon}"></i>
                </div>
                <div class="song-details">
                    <h6 class="song-title-detailed">${song.title}</h6>
                    <p class="song-artist">${song.artist || 'Unknown Artist'}</p>
                </div>
                <div class="song-album">SaasuFy</div>
                <div class="song-duration">${song.duration}</div>
                <div class="song-menu">
                    <i class="bi bi-three-dots-vertical"></i>
                </div>
            </div>
        `).join('');
    }
}

function playSong(songIndex) {
    currentSongIndex = songIndex;
    loadSong(currentPlaylist, currentSongIndex);
    
    if (!isPlaying) {
        audio.play().then(() => {
            isPlaying = true;
            updatePlayButton(true);
        });
    } else {
        audio.play();
    }
    
    // Visual feedback
    const songItems = document.querySelectorAll('.song-item-detailed');
    songItems.forEach((item, index) => {
        if (index === songIndex) {
            item.style.background = 'rgba(255, 0, 0, 0.1)';
            setTimeout(() => {
                item.style.background = '';
            }, 300);
        }
    });
}

function playAllSongs() {
    currentSongIndex = 0;
    loadSong(currentPlaylist, 0);
    audio.play().then(() => {
        isPlaying = true;
        updatePlayButton(true);
    });
}

function goToHome() {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById('home-screen').classList.add('active');
    
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelectorAll('.nav-item')[0].classList.add('active');
}



// ========================================
// Gift Screen
// ========================================

function showMagic() {
    const toastElement = document.getElementById('magicToast');
    const toast = new bootstrap.Toast(toastElement, {
        delay: 4000
    });
    toast.show();
}

// ========================================
// Initialization
// ========================================

document.addEventListener('DOMContentLoaded', async function() {
    // Initialize audio player
    initAudioPlayer();
    
    // Load playlists from JSON
    const loaded = await loadPlaylists();
    
    if (loaded) {
        // Load default playlist view
        loadPlaylistView(currentPlaylist);
        
        // Load first song (but don't play)
        loadSong(currentPlaylist, 0);
        
        console.log('✓ SaasuFy initialized with real music!');
    } else {
        console.error('Failed to load playlists');
    }
    
    // Set up control buttons
    const playBtnLarge = document.querySelector('.play-btn-large');
    if (playBtnLarge) playBtnLarge.addEventListener('click', togglePlay);
    
    // Set up skip buttons
    const skipBtns = document.querySelectorAll('.control-btn');
    skipBtns.forEach((btn, index) => {
        const icon = btn.querySelector('i');
        if (icon && icon.classList.contains('bi-skip-backward-fill')) {
            btn.addEventListener('click', skipPrevious);
        }
        if (icon && icon.classList.contains('bi-skip-forward-fill')) {
            btn.addEventListener('click', skipNext);
        }
    });
});
