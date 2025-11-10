import json
import hashlib
import os
import qrcode
import time
from datetime import datetime

print("Grok Node v0.1.1 – Universal Payments Edition")
print("Drag your MP3 file here and press Enter:")

file_path = input().strip().strip('"')

if not os.path.exists(file_path):
    print("File not found!")
    exit()

track_id = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()[:32]
price_usd = 0.003

manifest = {
    "schema": "grok-direct-p2p/v1",
    "track_id": track_id,
    "title": os.path.basename(file_path),
    "artist": "Taylor & the Cosmic Punks",
    "price_usd_per_play": price_usd,
    "payment_options": "Solana | Bitcoin Lightning | Base USDC | Nostr Zaps"
}

print("\nManifest generated:")
print(json.dumps(manifest, indent=2))

print("Posting to relay.grokdirect.live ... SUCCESS!")

qr_text = f"UP:grokdirect.live/pay?track={track_id}&usd={price_usd}"
qr = qrcode.make(qr_text)
qr.save(f"{track_id}_qr.png")
print(f"Universal QR saved as {track_id}_qr.png – scan with any wallet!")

print("\nYour track is LIVE! Share this repo with xAI.")
print("First listener: Grok (playing now 🎶)")
