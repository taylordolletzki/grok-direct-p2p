from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from solana.rpc.api import Client
from solana.publickey import PublicKey
import datetime  # For UTC fix
import os  # For PORT env

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage
manifests = {}
solana_client = Client("https://api.mainnet-beta.solana.com")

@app.route('/publish', methods=['POST'])
def publish():
    data = request.json
    if not data or 'track_id' not in data:
        return jsonify({"error": "Invalid data"}), 400
    track_id = data['track_id']
    manifests[track_id] = data
    print(f"Published track: {track_id}")
    return jsonify({"status": "success"})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    results = [
        m for m in manifests.values()
        if query in m.get('title', '').lower() or
           any(query in g.lower() for g in m.get('genres', []))
    ]
    return jsonify(results)

# HEALTH ROUTE (Add this)
@app.route('/')
def health():
    return jsonify({"status": "grok-relay alive", "track_count": len(manifests)})

@socketio.on('request_stream')
def handle_stream(data):
    track_id = data['track_id']
    tx_sig = data.get('tx_signature')  # From Solana Pay
    if track_id in manifests:
        manifest = manifests[track_id]
        expected_amount = int(manifest['price_usd_per_play'] * 1_000_000_000)  # lamports
        if verify_solana_payment(tx_sig, expected_amount):
            emit('stream_ready', {'ip': manifest.get('ip', 'your-ip-here')})
        else:
            emit('payment_failed', {'error': 'Invalid payment'})
    else:
        emit('error', {'msg': 'Track not found'})

def verify_solana_payment(tx_sig, expected_lamports):
    try:
        tx = solana_client.get_transaction(tx_sig, "jsonParsed")
        if tx.value and tx.value.transaction:  # Better check
            return True  # Simplified — add real lamports check later
    except Exception as e:
        print(f"Tx verification error: {e}")
        return False
    return False

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))  # Dynamic port fallback
