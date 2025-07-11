# 🚀 Scenario 03 — Docker Networking Magic

## 🎯 Scenario Goal

Demonstrate **real-world Docker networking problems** and how to fix them by:

✅ Running a Python Flask **Voting App** (WFO vs WFH)  
✅ Letting workshop attendees vote live via a public URL (ngrok or Cloudflare Tunnel)  
✅ Simulating networking failures:
- Missing database
- Containers in separate networks
✅ Fixing networking issues → **everything magically works!**

This scenario creates an unforgettable **AHA moment** for learners.

---

# ✅ Directory Structure

```

scenario\_03\_networking/
│
├── app/
│     ├── app.py
│     ├── requirements.txt
│     └── Dockerfile
├── scripts/
│     ├── run\_app\_without\_db.sh
│     ├── run\_app\_with\_db\_wrong\_network.sh
│     ├── fix\_network.sh
│     ├── expose\_ngrok.sh
│     ├── expose\_cloudflared.sh
│     └── cleanup.sh
└── scenario\_03\_networking.md

````

---

# ✅ How The Voting App Works

## Flask Voting App

Two buttons:

- ✅ Vote **WFH** (Work From Home)
- ✅ Vote **WFO** (Work From Office)

Votes stored in Redis under keys:

- `votes:wfh`
- `votes:wfo`

✅ Total votes shown live on web page.

---

## app/app.py

```python
from flask import Flask, render_template_string, request
import redis
import os

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

TEMPLATE = """
<h2>Vote for your preference:</h2>
<form method="POST">
    <button name="vote" value="wfh">Vote WFH (Work From Home)</button>
    <button name="vote" value="wfo">Vote WFO (Work From Office)</button>
</form>
<p>WFH Votes: {{ wfh }}</p>
<p>WFO Votes: {{ wfo }}</p>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        vote = request.form["vote"]
        r.incr(f"votes:{vote}")

    wfh = r.get("votes:wfh") or 0
    wfo = r.get("votes:wfo") or 0
    return render_template_string(TEMPLATE, wfh=wfh, wfo=wfo)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
````

---

## app/requirements.txt

```
flask
redis
```

---

## app/Dockerfile

```Dockerfile
FROM python:3.10

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

---

# ✅ Scenario Execution Steps

## ⭐ **STEP 1 — Run App Without Database**

---

### Run Redis (none yet)

→ Not running at all initially.

---

### Build Flask App

```bash
docker build -t vote-app ./app
```

---

### Run Flask App Without Redis

Run without setting `REDIS_HOST`:

```bash
docker run -d --name vote-app -p 5000:5000 vote-app
```

✅ Open:

```
http://localhost:5000
```

---

### Result

* Page loads → first adrenaline spike.
* Click a vote → Flask **crashes.**

✅ Logs show:

```
redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379. Connection refused.
```

---

✅ **Lesson:** Containers can’t magically have databases available!

---

# 🚫 **Error #1 → Missing Database**

**How to Fix:** Run Redis.

---

# ✅ STEP 2 — Run Redis but In Wrong Network

---

### Run Redis

Run Redis **standalone**:

```bash
docker run -d --name redis-server redis:alpine
```

---

### Re-run Flask

```bash
docker rm -f vote-app

docker run -d --name vote-app -p 5000:5000 \
    -e REDIS_HOST=redis-server \
    vote-app
```

---

### Result

✅ App still crashes:

```
redis.exceptions.ConnectionError: Error 111 connecting to redis-server:6379. Name or service not known.
```

---

✅ **Lesson:**

* Containers in separate networks **cannot see each other.**

---

# 🚫 **Error #2 → Separate Networks**

Flask container can’t resolve `redis-server` because:

* Redis is in bridge network.
* Flask is in another isolated network.

---

# ✅ STEP 3 — Fix The Network

---

### Create Custom Network

```bash
docker network create vote-net
```

---

### Run Redis in vote-net

```bash
docker rm -f redis-server

docker run -d --name redis-server \
    --network vote-net \
    redis:alpine
```

---

### Run Flask in vote-net

```bash
docker rm -f vote-app

docker run -d --name vote-app \
    --network vote-net \
    -p 5000:5000 \
    -e REDIS_HOST=redis-server \
    vote-app
```

---

✅ Open:

```
http://localhost:5000
```

Click vote buttons → **Votes increase!**

✅ Votes are now saved → Redis works!

✅ **Lesson:** Networking fixed. Containers communicate successfully.

---

# ✅ STEP 4 — Make It Public!

Let attendees **vote from their laptops!**

---

## Option 1 — Expose Via ngrok

Install ngrok:

```bash
brew install ngrok/ngrok/ngrok
```

Run:

```bash
ngrok http 5000
```

✅ Share public URL like:

```
https://glorious-bear-1234.ngrok.io
```

✅ Audience can vote → **real adrenaline!**

---

## Option 2 — Expose Via Cloudflare Tunnel

Install cloudflared:

```bash
brew install cloudflared
```

Run:

```bash
cloudflared tunnel --url http://localhost:5000
```

✅ Get public URL like:

```
https://vote.mydomain.com
```

✅ Audience votes → **infinite excitement.**

---

# ✅ Clean Up

```bash
docker rm -f vote-app redis-server
docker network rm vote-net
```

---

# ✅ Full Demo Script (Shell)

**scripts/fix\_network.sh**

```bash
#!/bin/bash

# Cleanup
docker rm -f vote-app redis-server
docker network rm vote-net

# Create network
docker network create vote-net

# Run redis
docker run -d --name redis-server --network vote-net redis:alpine

# Build flask app
docker build -t vote-app ./app

# Run flask app
docker run -d --name vote-app \
    --network vote-net \
    -p 5000:5000 \
    -e REDIS_HOST=redis-server \
    vote-app

echo "Vote app is live at http://localhost:5000"
```

---