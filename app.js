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

// ========================================
// Load Playlists from JSON
// ========================================

async function loadPlaylists() {
    try {
        const response = await fetch('playlists.json');
        const data = await response.json();
        
        // Transform data to match our app structure
        for (const [playlistId, songs] of Object.entries(data)) {
            playlists[playlistId] = {
                title: getPlaylistTitle(playlistId),
                icon: getPlaylistIcon(playlistId),
                gradient: getPlaylistGradient(playlistId),
                tags: getPlaylistTags(playlistId),
                songs: songs.map((song, index) => ({
                    title: song.title,
                    note: 'Bahurani Recommended',
                    duration: '0:00', // Will be updated when loaded
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
        'bahurani-picks': "Bahurani's Picks"
    };
    return titles[id] || id;
}

function getPlaylistIcon(id) {
    const icons = {
        'neet-warrior': 'bi-activity',
        'chef-specials': 'bi-egg-fried',
        'soft-break': 'bi-cup-hot',
        'bahurani-picks': 'bi-heart-fill'
    };
    return icons[id] || 'bi-music-note';
}

function getPlaylistGradient(id) {
    const gradients = {
        'neet-warrior': 'gradient-1',
        'chef-specials': 'gradient-2',
        'soft-break': 'gradient-3',
        'bahurani-picks': 'gradient-4'
    };
    return gradients[id] || 'gradient-1';
}

function getPlaylistTags(id) {
    const tags = {
        'neet-warrior': ['Study', 'Focus', 'Hype'],
        'chef-specials': ['Cooking', 'Soft', 'Love'],
        'soft-break': ['Soft', 'Relax', 'Break'],
        'bahurani-picks': ['Love', 'Special', 'Bahurani']
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
    
    // Update track info
    document.querySelector('.track-name').textContent = song.title;
    document.querySelector('.artist-name').textContent = 'Bahurani Recommended';
    
    // Update cover gradient
    const cover = document.querySelector('.now-playing-cover');
    cover.className = 'now-playing-cover ' + playlist.gradient;
    cover.innerHTML = `<i class="bi ${playlist.icon}"></i>`;
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
    const playBtn = document.querySelector('.control-btn.play-btn i');
    if (playBtn) {
        if (playing) {
            playBtn.classList.remove('bi-play-fill');
            playBtn.classList.add('bi-pause-fill');
        } else {
            playBtn.classList.remove('bi-pause-fill');
            playBtn.classList.add('bi-play-fill');
        }
    }
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
    
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
    
    if (screenName === 'playlist') {
        loadPlaylistView(currentPlaylist);
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
    
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelectorAll('.nav-item')[2].classList.add('active');
}

function loadPlaylistView(playlistId) {
    const playlist = playlists[playlistId];
    if (!playlist) return;
    
    document.getElementById('playlistTitleLarge').textContent = playlist.title;
    
    const coverElement = document.getElementById('playlistCoverLarge');
    coverElement.className = 'playlist-cover-large ' + playlist.gradient;
    coverElement.innerHTML = `<i class="bi ${playlist.icon}"></i>`;
    
    const tagsContainer = document.getElementById('playlistTags');
    tagsContainer.innerHTML = playlist.tags.map(tag => 
        `<span class="tag">${tag}</span>`
    ).join('');
    
    const songListContainer = document.getElementById('songList');
    songListContainer.innerHTML = playlist.songs.map((song, index) => `
        <div class="song-item" onclick="playSong(${index})">
            <div class="song-number">${index + 1}</div>
            <div class="song-info">
                <h6 class="song-title">${song.title}</h6>
                <p class="song-note">${song.note}</p>
            </div>
            <div class="song-duration">${song.duration}</div>
        </div>
    `).join('');
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
    const songItems = document.querySelectorAll('.song-item');
    songItems.forEach((item, index) => {
        if (index === songIndex) {
            item.style.background = 'var(--muted-gold)';
            item.style.color = 'white';
            setTimeout(() => {
                item.style.background = '';
                item.style.color = '';
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
// Theme Switcher
// ========================================

function setTheme(themeName) {
    document.body.className = 'theme-' + themeName;
    localStorage.setItem('saasufyTheme', themeName);
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
    // Load saved theme
    const savedTheme = localStorage.getItem('saasufyTheme');
    if (savedTheme) {
        setTheme(savedTheme);
    }
    
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
    const skipBackBtn = document.querySelectorAll('.control-btn')[0];
    const playBtn = document.querySelector('.control-btn.play-btn');
    const skipForwardBtn = document.querySelectorAll('.control-btn')[2];
    
    if (skipBackBtn) skipBackBtn.addEventListener('click', skipPrevious);
    if (playBtn) playBtn.addEventListener('click', togglePlay);
    if (skipForwardBtn) skipForwardBtn.addEventListener('click', skipNext);
});
