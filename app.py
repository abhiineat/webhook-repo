from flask import Flask, request, jsonify, send_from_directory
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)
print("🚀 Flask app started")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.github_events
collection = db.events
@app.route("/")
def index():
    return "GitHub Webhook Listener is running."
@app.route("/webhook", methods=["POST"])
def webhook():
    event = request.headers.get("X-GitHub-Event")
    payload = request.json

    print("🔔 Webhook received:", event)

    # ✅ Always allow ping
    if event == "ping":
        return jsonify({"msg": "pong"}), 200

    data = None

    if event == "push":
        data = {
            "request_id": payload["head_commit"]["id"],
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": payload["head_commit"]["timestamp"]
        }

    elif event == "pull_request":
        pr = payload["pull_request"]
        action_type = "MERGE" if pr.get("merged") else "PULL_REQUEST"

        data = {
            "request_id": str(pr["id"]),
            "author": pr["user"]["login"],
            "action": action_type,
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": pr["merged_at"] or pr["created_at"]
        }

    if data:
        print("📦 Inserting into MongoDB:", data)
        collection.insert_one(data)

    return jsonify({"status": "ok"}), 200
@app.route("/ui")
def ui():
    return send_from_directory("ui", "index.html")

@app.route("/events", methods=["GET"])
def events():
    events = list(
        collection.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(10)
    )
    return jsonify(events)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

