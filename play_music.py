import os
import subprocess
import time
import random
import threading
import termios
import tty
import sys

music_dir = "/home/pi/Music"
favorites_file = "/home/pi/favorites.txt"

playlist = sorted([f for f in os.listdir(music_dir) if f.endswith(".mp3")])
shuffle = False
skip_song = False
favorites = []
current_song = None

TIMEOUT_SECONDS = 30  # Max seconds to allow a song to play before skipping (for freeze recovery)

def play_song(song_path, label=""):
    global skip_song
    print(f"{label}Now playing: {os.path.basename(song_path)}")
    start_time = time.time()
    process = subprocess.Popen(["mpg123", "-q", song_path])
    while process.poll() is None:
        if skip_song:
            process.terminate()
            return
        elapsed = time.time() - start_time
        if elapsed > TIMEOUT_SECONDS:
            print(f"⏰ Timeout reached ({TIMEOUT_SECONDS}s), skipping song.")
            process.terminate()
            return
        time.sleep(0.2)

def load_favorites():
    if os.path.exists(favorites_file):
        with open(favorites_file, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def save_favorite(song):
    if song not in favorites:
        favorites.append(song)
        with open(favorites_file, "a") as f:
            f.write(song + "\n")
        print(f"✅ Saved favorite: {song}")

def keyboard_listener():
    global shuffle, skip_song, current_song
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    try:
        while True:
            key = sys.stdin.read(1).lower()
            if key == 's':
                shuffle = not shuffle
                print("Shuffle mode:", "ON" if shuffle else "OFF")
            elif key == 'n':
                skip_song = True
            elif key == 'f':
                if current_song:
                    save_favorite(current_song)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

threading.Thread(target=keyboard_listener, daemon=True).start()

while True:
    if not playlist:
        print("No MP3 files found. Waiting...")
        time.sleep(10)
        continue

    if shuffle:
        random.shuffle(playlist)

    for song in playlist:
        current_song = song
        skip_song = False
        song_path = os.path.join(music_dir, song)
        play_song(song_path)

    saved_favorites = load_favorites()
    if saved_favorites:
        print("🎵 Playing saved favorites...")
        for fav in saved_favorites:
            if fav in playlist:
                current_song = fav
                skip_song = False
                song_path = os.path.join(music_dir, fav)
                play_song(song_path, label="(Favorite) ")
