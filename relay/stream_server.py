import eventlet
eventlet.monkey_patch()  # First: Safe after Solana loaded in app.py

from flask import Flask
from flask_socketio import SocketIO, emit
import sys
sys.path.insert(0, '.')  # Ensure app.py is importable
from app import manifests, solana_client  # Import shared storage/client

# Eventlet WebSocket server
stream_app = Flask(__name__)
socketio = SocketIO(stream_app, cors_allowed_origins="*", async_mode="eventlet")

@socketio.on("request_stream")
def handle_stream(data):
    track_id = data.get("track_id")
    tx_sig = data.get("tx_signature")

    if track_id not in manifests:
        emit("error", {"msg": "Track not found"})
        return

    manifest = manifests[track_id]
    expected = int(manifest["price_usd_per_play"] * 1_000_000_000)  # lamports

    if verify_solana_payment(tx_sig, expected):
        stream_url = manifest.get("stream_url", f"https://your-ngrok-url.ngrok.io/{track_id}")
        emit("stream_ready", {"url": stream_url})
    else:
        emit("payment_failed", {"error": "Invalid payment"})

def verify_solana_payment(tx_sig, expected_lamports):
    if not tx_sig:
        return False
    try:
        resp = solana_client.get_transaction(tx_sig, encoding="jsonParsed")
        tx = resp.get("result")
        if tx and tx.get("transaction"):
            return True
    except Exception as e:
        print(f"[STREAM] Tx verification error: {e}")
    return False

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[STREAM] WebSocket server live on port {port}")
    socketio.run(stream_app, host="0.0.0.0", port=port)
