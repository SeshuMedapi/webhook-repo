from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.github_events
collection = db.events


# ---------------- HOME (UI) ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- WEBHOOK ----------------
@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.json
    event_type = request.headers.get("X-GitHub-Event")

    data = {}

    # PUSH EVENT
    if event_type == "push":
        data = {
            "request_id": payload["after"],
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": payload["ref"].split("/")[-1],
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": datetime.utcnow().strftime("%d %b %Y - %I:%M %p UTC")
        }

    # PULL REQUEST EVENT
    elif event_type == "pull_request":
        pr = payload["pull_request"]

        if payload["action"] == "closed" and pr.get("merged"):
            action_type = "MERGE"
        else:
            action_type = "PULL_REQUEST"

        data = {
            "request_id": str(pr["id"]),
            "author": pr["user"]["login"],
            "action": action_type,
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": datetime.utcnow().strftime("%d %b %Y - %I:%M %p UTC")
        }


    else:
        return jsonify({"message": "Event not handled"}), 200

    collection.insert_one(data)
    return jsonify({"message": "Event stored"}), 200


# ---------------- EVENTS API (UI Polling) ----------------
@app.route("/events")
def get_events():
    events = collection.find().sort("_id", -1).limit(10)

    response = []
    for event in events:
        response.append({
            "author": event["author"],
            "action": event["action"],
            "from_branch": event["from_branch"],
            "to_branch": event["to_branch"],
            "timestamp": event["timestamp"]
        })

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
