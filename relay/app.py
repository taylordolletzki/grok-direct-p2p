import os
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from solana.rpc.api import Client

# -------------------------------------------------
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage
manifests = {}
solana_client = Client("https://api.mainnet-beta.solana.com")
# -------------------------------------------------

@app.route("/")
def health():
    return jsonify({"status": "grok-relay alive", "track_count": len(manifests)})

@app.route("/publish", methods=["POST"])
def publish():
    data = request.json
    if not data or "track_id" not in data:
        return jsonify({"error": "Invalid data"}), 400
    track_id = data["track_id"]
    manifests[track_id] = data
    print(f"Published track: {track_id}")
    return jsonify({"status": "success"})

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower()
    results = [
        m for m in manifests.values()
        if query in m.get("title", "").lower()
        or any(query in g.lower() for g in m.get("genres", []))
    ]
    return jsonify(results)

# -------------------------------------------------
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
        emit("stream_ready", {"ip": manifest.get("ip", "your-ip-here")})
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
        print(f"Tx verification error: {e}")
    return False

# -------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
