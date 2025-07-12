# PiPod

The **PiPod Shuffle** is a minimalist offline MP3 player built with a Raspberry Pi. It automatically plays music files from a local folder and includes basic playback controls — perfect for DIY audio enthusiasts.

---

## 🔧 Features

- 🎵 Plays MP3 files in order or shuffled
- 🔁 Loops your entire playlist forever
- ⏭️ Skip tracks with keyboard input
- 🌟 Save favorite songs
- 🔧 Automatically recovers from frozen audio playback
- 🧠 Works headless (no monitor) or with GUI

---

## 🧰 Requirements

- Raspberry Pi 3B or newer  
- Raspberry Pi OS (Lite or Desktop)  
- Python 3  
- [`mpg123`](https://www.mpg123.de/) (audio player for MP3)  
- MP3 files placed in: `/home/pi/Music/`

Install `mpg123` with:


`sudo apt update
sudo apt install mpg123`
🚀 Setup & Usage
Clone this repo or copy the play_music.py script to your Pi:

`git clone https://github.com/YOUR_USERNAME/pipod-shuffle.git`

Add your MP3 files to the music folder:

`mkdir -p ~/Music
cp your_songs/*.mp3 ~/Music/`
Run the player:

`python3 play_music.py`
🎮 Controls (from terminal)
n → Next song

s → Toggle shuffle

f → Save current song as a favorite

Favorite tracks are saved to /home/pi/favorites.txt and played after the playlist.

⚙️ Optional: Auto-start on Boot (GUI users)
Open the Raspberry menu → Preferences → Session and Startup

Add a new startup entry:

Name: PiPod Shuffle

Command:

`python3 /home/pi/pipod-shuffle/play_music.py &`
