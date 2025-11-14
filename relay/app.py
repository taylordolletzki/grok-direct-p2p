import os
print("=== DEBUG: os imported ===")

try:
    from flask import Flask, request, jsonify
    print("=== DEBUG: Flask imported ===")
except Exception as e:
    print(f"=== DEBUG: Flask import error: {e} ===")

app = Flask(__name__)
print("=== DEBUG: Flask app created ===")

manifests = {}

@app.route("/")
def health():
    print("=== DEBUG: Health route called ===")
    return jsonify({"status": "grok-relay alive", "track_count": len(manifests)})

@app.route("/publish", methods=["POST"])
def publish():
    print("=== DEBUG: Publish route called ===")
    data = request.json
    if not data or "track_id" not in data:
        return jsonify({"error": "Invalid data"}), 400
    track_id = data["track_id"]
    manifests[track_id] = data
    print(f"=== DEBUG: Track published: {track_id} ===")
    return jsonify({"status": "success"})

@app.route("/search", methods=["GET"])
def search():
    print("=== DEBUG: Search route called ===")
    query = request.args.get("q", "").lower()
    results = [
        m for m in manifests.values()
        if query in m.get("title", "").lower()
        or any(query in g.lower() for g in m.get("genres", []))
    ]
    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"=== DEBUG: Starting server on 0.0.0.0:{port} ===")
    app.run(host="0.0.0.0", port=port)
