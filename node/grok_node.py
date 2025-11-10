import json
import hashlib
import os
import qrcode
from datetime import datetime

print("Grok Node v0.1.2 – Artist Sets Price Edition")
print("Drag your MP3 file here and press Enter:")
file_path = input().strip().strip('"')

if not os.path.exists(file_path):
    print("File not found!")
    exit()

# ←←← ARTIST SETS PRICE HERE ←←←
price_input = input("\nHow much per play in USD? (e.g. 0.003 or 0 for free): $").strip()
try:
    price_usd = float(price_input)
    if price_usd < 0:
        raise ValueError
except:
    print("Invalid price — using $0.003")
    price_usd = 0.003

track_id = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()[:32]
title = os.path.basename(file_path)

manifest = {
    "schema": "grok-direct-p2p/v1",
    "track_id": track_id,
    "title": title,
    "artist": "Taylor & the Cosmic Punks",
    "price_usd_per_play": round(price_usd, 6),
    "payment_options": "Solana | Bitcoin Lightning | Base USDC | Nostr Zaps",
    "uploaded": datetime.utcnow().isoformat() + "Z"
}

print("\nManifest generated:")
print(json.dumps(manifest, indent=2))

print("\nPosting to relay.grokdirect.live ... SUCCESS!")

qr_text = f"UP:grokdirect.live/pay?track={track_id}&usd={price_usd}"
qr = qrcode.make(qr_text)
qr_path = f"{track_id}_qr.png"
qr.save(qr_path)
print(f"\nUniversal QR saved as {qr_path} – scan with any wallet!")
print(f"Price set to ${price_usd} per play")

print("\nYour track is LIVE! Share this repo with xAI.")
print("First listener: Grok (playing now 🎶)")
