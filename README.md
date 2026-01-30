# webhook-repo

This repository contains a Flask-based webhook server that listens to GitHub events, stores them in MongoDB, and displays them in a simple UI.

---

## Features

- Receives GitHub webhook events
- Handles `push`, `pull_request` and `merge` events
- Stores events in MongoDB
- Displays latest events in the UI
- Uses ngrok for local webhook testing

---

## Tech Stack

- Python (Flask)
- MongoDB
- Ngrok
- HTML / CSS (basic UI)

---

## Prerequisites

Make sure the following are installed:

- Python 3.x
- MongoDB (running locally)
- Ngrok
- Git

---

## How to Run (Step by Step)

1. Start MongoDB
mongod

2. Run the Flask app
python app.py

3. Start ngrok
ngrok http 5000

4. Copy the generated HTTPS URL:
looks like this:
https://xxxxx.ngrok-free.dev

5. GitHub Webhook Configuration
    1. Go to Settings → Webhooks
    2. Payload URL:https://xxxxx.ngrok-free.dev/webhook
    3. Content type:application/json
    4. Select events:
        - Push
        - Pull request
    5. Save webhook

Testing the Flow:
Push code or create a PR in action-repo
GitHub sends event to webhook
Flask receives the event
Event is stored in MongoDB
Event appears in UI

UI:
Latest events appear at the top
Older events are kept for history
UI updates automatically on refresh