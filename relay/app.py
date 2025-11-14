import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
manifests = {}

@app.route("/")
def health():
    print("[HEALTH] Check")
    return jsonify({"status": "grok-relay alive", "track_count": len(manifests)})

@app.route("/publish", methods=["POST"])
def publish():
    data = request.json
    if not data or "track_id" not in data:
        return jsonify({"error": "Invalid data"}), 400
    track_id = data["track_id"]
    manifests[track_id] = data
    print(f"[PUBLISH] Track: {track_id}")
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[START] Server on 0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)
