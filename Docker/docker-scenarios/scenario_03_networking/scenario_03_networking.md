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
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>🏆 Docker Voting App</title>
    <style>
        body {
            background: linear-gradient(135deg, #f8ffae 0%, #43c6ac 100%);
            font-family: 'Segoe UI', 'Arial', sans-serif;
            text-align: center;
            padding: 0;
            margin: 0;
            min-height: 100vh;
        }
        .container {
            margin-top: 60px;
            background: rgba(255,255,255,0.9);
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31,38,135,0.2);
            display: inline-block;
            padding: 40px 60px 30px 60px;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 0.2em;
            color: #2d3a4b;
        }
        h2 {
            color: #43c6ac;
            margin-bottom: 1.5em;
        }
        .vote-btn {
            font-size: 1.5em;
            padding: 20px 40px;
            margin: 20px 30px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: background 0.2s, transform 0.2s;
            box-shadow: 0 2px 8px rgba(67,198,172,0.15);
        }
        .vote-btn.wfh {
            background: linear-gradient(90deg, #f7971e 0%, #ffd200 100%);
            color: #2d3a4b;
        }
        .vote-btn.wfh:hover {
            background: linear-gradient(90deg, #ffd200 0%, #f7971e 100%);
            transform: scale(1.07);
        }
        .vote-btn.wfo {
            background: linear-gradient(90deg, #43c6ac 0%, #191654 100%);
            color: #fff;
        }
        .vote-btn.wfo:hover {
            background: linear-gradient(90deg, #191654 0%, #43c6ac 100%);
            transform: scale(1.07);
        }
        .votes {
            margin-top: 30px;
            display: flex;
            justify-content: center;
            gap: 60px;
        }
        .vote-box {
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 2px 8px rgba(67,198,172,0.10);
            padding: 30px 40px;
            min-width: 160px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .vote-label {
            font-size: 1.2em;
            margin-bottom: 10px;
        }
        .vote-count {
            font-size: 2.5em;
            font-weight: bold;
            color: #43c6ac;
        }
        .emoji {
            font-size: 2.2em;
            margin-bottom: 10px;
        }
        .footer {
            margin-top: 50px;
            color: #2d3a4b;
            font-size: 1.1em;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏆 Docker Voting App</h1>
        <h2>Which do you prefer?</h2>
        <form method="POST">
            <button class="vote-btn wfh" name="vote" value="wfh">🏡 WFH (Work From Home)</button>
            <button class="vote-btn wfo" name="vote" value="wfo">🏢 WFO (Work From Office)</button>
        </form>
        <div class="votes">
            <div class="vote-box">
                <div class="emoji">🏡</div>
                <div class="vote-label">WFH Votes</div>
                <div class="vote-count">{{ wfh }}</div>
            </div>
            <div class="vote-box">
                <div class="emoji">🏢</div>
                <div class="vote-label">WFO Votes</div>
                <div class="vote-count">{{ wfo }}</div>
            </div>
        </div>
    </div>
    <div class="footer">
        Made with ❤️ for the Docker Networking Magic Workshop
    </div>
</body>
</html>
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