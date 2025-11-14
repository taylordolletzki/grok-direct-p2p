import os
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

# --- STARTUP DEBUG ---
print("\n=== GROK RELAY STARTUP ===")
print("Loading app.py...")
print("Python path:", os.getcwd())
print("Files in directory:", os.listdir('.'))
# --- END DEBUG ---

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

# --- LAZY SOLANA ---
solana_client = None

def get_solana_client():
    global solana_client
    if solana_client is None:
        print("[LAZY] Initializing Solana client...")
        from solana.rpc.api import Client
        solana_client = Client("https://api.mainnet-beta.solana.com")
    return solana_client

# --- STORAGE ---
manifests = {}

# --- ROUTES ---
@app.route("/")
def health():
    print("[HTTP] Health check requested")
    return jsonify({"status": "grok-relay alive", "track_count": len(manifests)})

@app.route("/publish", methods=["POST"])
def publish():
    data = request.json
    if not data or "track_id" not in data:
        return jsonify({"error": "Invalid data"}), 400
    track_id = data["track_id"]
    manifests[track_id] = data
    print(f"[HTTP] Published track: {track_id}")
    return jsonify({"status": "success"})

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower()
    results = [
        m for m in manifests.values()
        if query in m.get("title", "").lower()
        or any(query in g.lower() for g in m.get("genres", []))
    ]
    print(f"[HTTP] Search query: '{query}' → {len(results)} results")
    return jsonify(results)

# --- WEBSOCKET ---
@socketio.on("request_stream")
def handle_stream(data):
    print(f"[WS] Stream request: {data}")
    track_id = data.get("track_id")
    tx_sig = data.get("tx_signature")

    if track_id not in manifests:
        print(f"[WS] Track not found: {track_id}")
        emit("error", {"msg": "Track not found"})
        return

    manifest = manifests[track_id]
    expected = int(manifest["price_usd_per_play"] * 1_000_000_000)

    if verify_solana_payment(tx_sig, expected):
        stream_url = manifest.get("stream_url", f"https://your-ngrok-url.ngrok.io/{track_id}")
        print(f"[WS] Payment OK → sending stream URL: {stream_url}")
        emit("stream_ready", {"url": stream_url})
    else:
        print(f"[WS] Payment failed for tx: {tx_sig}")
        emit("payment_failed", {"error": "Invalid payment"})

def verify_solana_payment(tx_sig, expected_lamports):
    if not tx_sig:
        return False
    client = get_solana_client()
    try:
        resp = client.get_transaction(tx_sig, encoding="jsonParsed")
        tx = resp.get("result")
        if tx and tx.get("transaction"):
            return True
    except Exception as e:
        print(f"[ERROR] Solana verify failed: {e}")
    return False

# --- RUN ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[RUN] Starting server on 0.0.0.0:{port} with gevent")
    socketio.run(app, host="0.0.0.0", port=port)
