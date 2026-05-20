# 🎵 MoodTunes — Mood-Based Music Website
Final Year College Project | Python Flask + SQLite + Spotify API

---

## Project Structure

```
moodtunes/
├── app.py              ← Main Flask app (routes)
├── auth.py             ← Login & register logic
├── db_helper.py        ← SQLite database operations
├── mood_map.py         ← 8 moods with Spotify parameters
├── spotify_helper.py   ← Spotify API integration
├── requirements.txt    ← Python dependencies
├── moodtunes.db        ← Created automatically on first run
├── static/
│   └── css/
│       └── style.css   ← All styling
└── templates/
    ├── base.html       ← Shared layout & navbar
    ├── login.html      ← Login page
    ├── register.html   ← Registration page
    ├── index.html      ← Mood selector (home)
    ├── playlist.html   ← Playlist results
    └── history.html    ← User history
```

---

## Setup Instructions

### Step 1 — Install dependencies
```bash
pip install flask spotipy
```

### Step 2 — Run the app
```bash
python app.py
```
Open your browser at: http://127.0.0.1:5000

The database (moodtunes.db) is created automatically on first run.

---

## Spotify API Setup (Optional but recommended)

1. Go to https://developer.spotify.com/dashboard
2. Log in and click "Create App"
3. Copy your Client ID and Client Secret
4. Set them as environment variables:

**Windows:**
```
set SPOTIFY_CLIENT_ID=your_id_here
set SPOTIFY_CLIENT_SECRET=your_secret_here
python app.py
```

**Mac/Linux:**
```
export SPOTIFY_CLIENT_ID=your_id_here
export SPOTIFY_CLIENT_SECRET=your_secret_here
python app.py
```

If no Spotify keys are set, the app runs with built-in mock song data automatically.

---

## Features

- User registration and login with password hashing
- 8 mood types: Happy, Sad, Calm, Energetic, Angry, Romantic, Focused, Sleepy
- Mood detection by button click OR text input (keyword matching)
- Spotify API integration with mock fallback
- Listening history saved per user in SQLite
- Fully responsive dark-themed UI

---

## Technologies Used

| Layer    | Technology                        |
|----------|-----------------------------------|
| Frontend | Flask + Jinja2 HTML templates     |
| Backend  | Python 3, Flask                   |
| Auth     | hashlib (SHA-256 password hashing)|
| Database | SQLite (Python built-in sqlite3)  |
| API      | Spotify Web API (spotipy)         |
