from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

manifests = {}

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

@socketio.on('connect_listener')
def connect_listener(data):
    track_id = data.get('track_id')
    if track_id in manifests:
        emit('artist_ip', {'ip': manifests[track_id].get('ip', 'your-ip-here')})
    else:
        emit('error', {'msg': 'Track not found'})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
