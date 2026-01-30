# GitHub Webhook Activity Tracker

This project captures GitHub repository activities using **GitHub Webhooks**, stores minimal structured data in **MongoDB**, and displays recent repository activity on a **clean, auto-updating UI**.

It is built as part of a developer assessment to demonstrate backend integration, webhook handling, data modeling, and UI polling.

---

## 🚀 Live Demo

* **Webhook Receiver & API**:
  [https://webhook-repo-lwi7.onrender.com](https://webhook-repo-lwi7.onrender.com)

* **UI (Activity Feed)**:
  [https://webhook-repo-lwi7.onrender.com/ui](https://webhook-repo-lwi7.onrender.com/ui)

---

## 📌 Repositories

* **action-repo** (GitHub events source):
  Triggers GitHub events like Push, Pull Request, and Merge.

* **webhook-repo** (this repository):
  Flask-based webhook receiver, MongoDB persistence, and UI.

---

## 🧠 Architecture Overview

```
GitHub (action-repo)
     │
     │  Webhook Events (Push / PR / Merge)
     ▼
Flask Webhook Receiver (webhook-repo)
     │
     │  Minimal Event Data
     ▼
MongoDB (github_events.events)
     │
     │  Poll every 15 seconds
     ▼
UI (HTML + JS)
```

---

## ⚙️ Tech Stack

* **Backend**: Flask (Python)
* **Database**: MongoDB
* **Frontend**: HTML, CSS, Vanilla JavaScript
* **Deployment**: Render
* **Integration**: GitHub Webhooks

---

## 📂 MongoDB Schema

Only the **minimum required data** is stored, as per the problem statement.

```json
{
  "request_id": "string",
  "author": "string",
  "action": "PUSH | PULL_REQUEST | MERGE",
  "from_branch": "string | null",
  "to_branch": "string",
  "timestamp": "ISO-8601 UTC string"
}
```

---

## 🔔 Supported GitHub Events

### ✅ Push

**Format:**
`{author} pushed to {to_branch} on {timestamp}`

**Example:**
`abhiineat pushed to main on 29th January 2026 - 1:55 PM UTC`

---

### ✅ Pull Request

**Format:**
`{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}`

---

### ⭐ Merge (Bonus)

**Format:**
`{author} merged branch {from_branch} to {to_branch} on {timestamp}`

Merge events are detected when:

```json
pull_request.merged == true
```

---

## 🔄 Application Flow

1. A developer performs an action (push / PR / merge) on **action-repo**
2. GitHub sends a webhook payload to `/webhook`
3. Flask parses the event and extracts minimal required fields
4. Data is stored in MongoDB
5. UI polls `/events` every **15 seconds**
6. Latest activity is rendered in a clean feed

---

## 🖥️ UI Details

* Polls backend every **15 seconds**
* No WebSockets (as per requirement)
* Minimal and readable design
* Human-readable event messages

---

## 🧪 Testing

### Local Testing

```bash
python app.py
```

Trigger events by pushing or opening PRs on `action-repo`.

### MongoDB Verification

```bash
mongosh
use github_events
db.events.find().pretty()
```

---

## 🌐 Deployment Notes

* Flask app is deployed on **Render**
* Server binds to `0.0.0.0` and uses the platform-provided `PORT`
* MongoDB connection is provided via environment variables

---

## 💡 Design Decisions

* **Polling instead of sockets**: matches assessment requirement
* **Minimal schema**: avoids storing unnecessary GitHub payload data
* **Separate repos**: clean separation of concerns
* **Plain HTML UI**: lightweight, fast, and easy to reason about

---

