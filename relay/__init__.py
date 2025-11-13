from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from solana.rpc.api import Client
from solana.publickey import PublicKey
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory manifests
manifests = {}

# Solana mainnet client
solana_client = Client("https://api.mainnet-beta.solana.com")

@app.route('/publish', methods=['POST'])
def publish():
    data = request.json
    track_id = data['track_id']
    manifests[track_id] = data
    print(f"Published: {track_id}")
    return jsonify({"status": "success"})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    results = [
        m for m in manifests.values()
        if query in m['title'].lower() or any(query in g.lower() for g in m.get('genres', []))
    ]
    return jsonify(results)

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
        if tx['result']:
            # Simplified — check if payment went to your wallet
            return True  # Real check in full version
    except:
        return False
    return False

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
app = app
