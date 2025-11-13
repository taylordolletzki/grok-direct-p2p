from flask import Flask, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage
manifests = {}

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
    results = [m for m in manifests.values() if query in str(m).lower()]
    return jsonify(results)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
