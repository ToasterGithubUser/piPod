#!/usr/bin/env python3
# -@ndre 2025, made with love <3
# Kudos to cyberchicken1231 on GitHub for the original PiPod script
# and to the rpi_lcd library by sdesalve for LCD handling
import sys, os, time, random, threading, termios, tty, signal
from rpi_lcd import LCD
import vlc

# --- Configuration ---
music_dir = "/home/andre/Music"
favorites_file = "/home/andre/favorites.txt"
lcd = LCD()
lcd.clear()
lcd.text("PiPod Gen3+.",1)
lcd.text("Think Diffrent.",2)
time.sleep(1.5)
lcd.clear()
playlist = sorted([f for f in os.listdir(music_dir) if f.endswith(".mp3")])
shuffle = False
skip_song = False
paused = False
favorites = []
current_song = None
volume = 70  # 0-100 for VLC
player = vlc.MediaPlayer()

TIMEOUT_SECONDS = 30

# --- Functions ---
def play_song(song_path, label=""):
    global skip_song, current_song, paused, player
    lcd.clear()
    print(f"{label}:{os.path.basename(song_path)}")
    lcd.text(f"{label}{os.path.basename(song_path)}",1)

    current_song = song_path
    media = vlc.Media(song_path)
    player.set_media(media)
    player.audio_set_volume(volume)
    player.play()
    start_time = time.time()

    while player.get_state() not in (vlc.State.Ended, vlc.State.Error):
        if skip_song:
            player.stop()
            return
        if paused:
            player.set_pause(1)
        else:
            player.set_pause(0)
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
        print(f"? Saved favorite: {song}")

def set_volume(delta):
    global volume
    volume = max(0, min(100, volume + int(delta*100)))  # VLC uses 0-100
    player.audio_set_volume(volume)
    print(f"?? Volume: {volume}%")

    # Show volume on LCD
    lcd.clear()
    lcd.text(f"Vol: {volume}%",1)
    bar_length = 14
    filled = int((volume/100)*bar_length)
    lcd.text("[" + "#"*filled + " "*(bar_length-filled) + "]", 2)

    time.sleep(0.5)
    lcd.clear()
    if current_song:
        lcd.text(f"{os.path.basename(current_song)}",1)

def keyboard_listener():
    global shuffle, skip_song, paused, current_song
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    try:
        while True:
            key = sys.stdin.read(1).lower()
            if key == 's':
                shuffle = not shuffle
                lcd.clear()
                lcd.text("Shuffle: ON" if shuffle else "Shuffle: OFF",1)
                print("Shuffle:", "ON" if shuffle else "OFF")
                time.sleep(1)
                lcd.clear()
                if current_song:
                    lcd.text(f"{os.path.basename(current_song)}",1)
            elif key == '+':
                set_volume(0.05)
            elif key == '-':
                set_volume(-0.05)
            elif key == 'n':
                skip_song = True
            elif key == 'f' and current_song:
                save_favorite(current_song)
            elif key == 'd' and current_song:
                if not paused:
                    player.set_pause(1)
                    paused = True
                    lcd.clear()
                    lcd.text("Paused",1)
                    print("Paused")
                else:
                    player.set_pause(0)
                    paused = False
                    lcd.clear()
                    lcd.text(f"{os.path.basename(current_song)}",1)
                    print("Resumed")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

threading.Thread(target=keyboard_listener, daemon=True).start()
# --- Main loop ---
while True:
    if not playlist:
        print("No MP3 files found. Waiting...")
        time.sleep(10)
        continue

    if shuffle:
        random.shuffle(playlist)

    for song in playlist:
        skip_song = False
        song_path = os.path.join(music_dir, song)
        play_song(song_path)

    saved_favorites = load_favorites()
    if saved_favorites:
        print("?? Playing saved favorites...")
        for fav in saved_favorites:
            if fav in playlist:
                skip_song = False
                song_path = os.path.join(music_dir, fav)
                play_song(song_path, label="(Favorite) ")


