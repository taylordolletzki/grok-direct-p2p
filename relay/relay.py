from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# In-memory database for manifests (replace with Meilisearch for scale)
manifests = {}

@app.route('/publish', methods=['POST'])
def publish():
    data = request.json
    track_id = data['track_id']
    manifests[track_id] = data
    return jsonify({"status": "success"})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    # Simple keyword search (upgrade to Meilisearch for advanced)
    results = [m for m in manifests.values() if query.lower() in ' '.join(m['genres']).lower() or query.lower() in m['title'].lower()]
    return jsonify(results)

@socketio.on('connect_listener')
def connect_listener(data):
    track_id = data['track_id']
    if track_id in manifests:
        emit('artist_ip', {'ip': manifests[track_id]['ip']})  # Send artist's IP for P2P
    else:
        emit('error', {'msg': 'Track not found'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)  # Temporary fix for Render; replace with Gunicorn for production
