import json
import hashlib
import os
import qrcode
import platform
from datetime import datetime

LIBRARY_FILE = "library.json"
if os.path.exists(LIBRARY_FILE):
    with open(LIBRARY_FILE, "r") as f:
        library = json.load(f)
else:
    library = {}

def save_library():
    with open(LIBRARY_FILE, "w") as f:
        json.dump(library, f, indent=2)

def open_qr(qr_path):
    system = platform.system()
    if system == "Darwin":  # macOS
        os.system(f"open {qr_path}")
    elif system == "Windows":
        os.startfile(qr_path)
    else:  # Linux
        os.system(f"xdg-open {qr_path}")

def add_track():
    print("\n=== ADD NEW TRACK ===")
    file_path = input("Drag your MP3/WAV file here and press Enter: ").strip().strip('"')
    if not os.path.exists(file_path):
        print("File not found!")
        return

    track_id = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()[:32]
    if track_id in library:
        print("Track already exists!")
        return

    title = input("Track title (leave blank for filename): ") or os.path.basename(file_path)
    artist = input("Artist name: ") or "Taylor Dolletzki"
    genres = input("Genres/tags (comma-separated): ")
    bpm = input("BPM (optional): ")
    key = input("Key (optional): ")
    mood = input("Mood (optional): ")

    price_usd = 0.0333  # Your fixed price
    print(f"Price set to ${price_usd} per play")

    splits = []
    while True:
        wallet = input("Co-writer wallet/address (or press Enter to finish): ").strip()
        if not wallet:
            break
        percent = float(input(f"Percentage for {wallet} (e.g. 30): ") or "0")
        splits.append({"wallet": wallet, "percent": percent})

    if not splits:
        splits = [{"wallet": "your_main_wallet", "percent": 100}]

    manifest = {
        "schema": "grok-direct-p2p/v1",
        "track_id": track_id,
        "title": title,
        "artist": artist,
        "genres": [g.strip() for g in genres.split(",") if g.strip()],
        "bpm": bpm,
        "key": key,
        "mood": mood,
        "price_usd_per_play": price_usd,
        "splits": splits,
        "uploaded": datetime.utcnow().isoformat() + "Z",
        "file_path": file_path
    }

    library[track_id] = manifest
    save_library()

    qr_text = f"UP:grokdirect.live/pay?track={track_id}&usd={price_usd}"
    qr = qrcode.make(qr_text)
    qr_path = f"{track_id}_qr.png"
    qr.save(qr_path)
    print(f"\nTrack added! QR saved as {qr_path} – opening now!")
    open_qr(qr_path)
    print(json.dumps(manifest, indent=2))

def edit_track():
    track_id = input("Enter track_id to edit: ")
    if track_id not in library:
        print("Track not found!")
        return
    m = library[track_id]
    print(f"Current price: ${m['price_usd_per_play']}")
    new_price = input("New price per play (or Enter to keep $0.0333): $")
    if new_price.strip():
        m['price_usd_per_play'] = round(float(new_price), 6)
    save_library()
    print("Price updated!")

def delete_track():
    track_id = input("Enter track_id to DELETE forever: ")
    if track_id not in library:
        print("Track not found!")
        return
    confirm = input(f"Type YES to delete {library[track_id]['title']}: ")
    if confirm == "YES":
        del library[track_id]
        save_library()
        print("Track deleted forever.")

def list_tracks():
    print("\n=== YOUR LIBRARY ===")
    for tid, m in library.items():
        print(f"{tid[:8]}... | {m['title']} by {m['artist']} | ${m['price_usd_per_play']} | tags: {', '.join(m['genres'][:3])}")

while True:
    print("\nGrok Direct P2P – v0.2.1")
    print("1. Add new track")
    print("2. Edit price")
    print("3. Delete track")
    print("4. List library")
    print("5. Exit")
    choice = input("Choose: ")
    if choice == "1":
        add_track()
    elif choice == "2":
        edit_track()
    elif choice == "3":
        delete_track()
    elif choice == "4":
        list_tracks()
    elif choice == "5":
        break
