# 🚀 Scenario 05 — The Docker Escape Room Challenge

---

## 🎯 Scenario Goal

> Transform learners from Docker users into Docker HEROES through:
>
> ✅ Real-world puzzles
> ✅ Gamification and fun storytelling
> ✅ Live problem-solving
> ✅ Hands-on Docker commands
> ✅ Hilarious and unforgettable learning

---

# 🧩 The Storyline

---

You and your workshop friends have been **kidnapped by Dr. NullPointer, the evil villain of the cloud.**  

He’s locked you inside the **Docker Vault**, a high-security digital prison guarded by containers.

To escape, you must:

- Solve five Docker puzzles
- Discover hidden secrets
- Hack your way through broken networks
- Outsmart containers with memory issues
- Master multi-stage builds to save your digital life!

Fail…and you’ll be trapped running endless `hello-world` containers for eternity.

---

# 🏆 The Escape Flow

---

## ✅ How It Works

- You’ll see a clue in the web browser.
- You’ll have a live shell to run **real Docker commands.**
- Enter your answer in the browser.
- If correct → next door unlocks.
- If wrong → Dr. NullPointer taunts you mercilessly.

---

## ✅ Game Mechanics

✅ **Time challenge:** Solve all puzzles before Dr. NullPointer triggers a CI/CD pipeline apocalypse.  
✅ **Score system:**
- +10 points for each puzzle
- -3 points for failed attempts
✅ **Leaderboards** → bragging rights!
✅ **Funny taunts** → randomized villain insults
✅ **Real consequences:**
- Containers running
- Logs filling up
- Resource exhaustion

---

# 🕹️ The Five Docker Puzzles

---

## ⭐ Puzzle 1 — The Secret Vault (Volumes)

---

### Dr. NullPointer’s Message:

> “Mwahaha! I’ve hidden the **Escape Key** inside a secret volume.  
> It’s buried in:
> ```
> /secret/code.txt
> ```
> Inside a Docker volume called:
> ```
> vault-volume
> ```
> Find it… or you’ll be stuck in `/dev/null` forever.”

---

### What Learners Must Do

Run:

```bash
docker run --rm -v vault-volume:/mnt busybox cat /mnt/secret/code.txt
````

✅ Copy secret code → paste into web UI

---

### Dr. NullPointer Taunts:

* “That’s adorable… you think you can just `docker run` your way out?”
* “Even my cat knows how to mount a volume.”

---

✅ Insight:

> “Volumes persist data across containers. They’re like hidden treasure chests in Docker.”

---

---

## ⭐ Puzzle 2 — The Broken Bridge (Networking)

---

### Dr. NullPointer’s Message:

> “Your precious app can’t talk to its database!
> I’ve trapped them in **different Docker networks.**
> Fix it… or your packets will wander the void!”

---

### Scenario:

* Redis running in `networkA`
* Flask app running in `networkB`

---

### What Learners Must Do

Run:

```bash
docker network connect networkA redis-server
```

✅ Test connectivity:

```bash
docker run --rm --network networkA redis redis-cli -h redis-server ping
```

✅ Enter “PONG” into web UI → unlocks next puzzle

---

### Dr. NullPointer Taunts:

* “Packets? Lost. Like your hopes.”
* “Network errors are my love language.”

---

✅ Insight:

> “Custom Docker networks let containers talk to each other.
> Default bridge networks isolate them unless connected explicitly.”

---

---

## ⭐ Puzzle 3 — The Out-of-Memory Monster

---

### Dr. NullPointer’s Message:

> “Oops… your container **ran out of memory.**
> It keeps crashing with:
>
> ```
> Cannot allocate memory
> ```
>
> Increase its memory limit… or I’ll throttle you!”

---

### What Learners Must Do

Re-run the failing container:

```bash
docker run -d --memory=512m busybox sh -c "dd if=/dev/zero of=/dev/null bs=1M"
```

✅ Check logs:

```bash
docker logs <container_id>
```

✅ Submit confirmation of successful run.

---

### Dr. NullPointer Taunts:

* “Memory? You humans are always running out of it.”
* “OOM Killer is my best friend.”

---

✅ Insight:

> “Docker lets you set memory and CPU limits.
> It’s like giving containers strict lunch money.”

---

---

## ⭐ Puzzle 4 — Secrets in Plain Sight

---

### Dr. NullPointer’s Message:

> “I’ve hidden my evil flag as an **environment variable** inside a running container:
>
> ```
> SECRET_FLAG=escape_docker
> ```
>
> Find it… or your logs will overflow!”

---

### What Learners Must Do

Run:

```bash
docker inspect container123
```

✅ Locate environment variable:

```
SECRET_FLAG=escape_docker
```

✅ Submit “escape\_docker” in web UI.

---

### Dr. NullPointer Taunts:

* “Nice try. I’ve hidden secrets deeper than your debugging skills.”
* “Inspect me all you want. You’ll never escape.”

---

✅ Insight:

> “`docker inspect` reveals a container’s secrets:
> environment variables, mount paths, networks, and more.”

---

---

## ⭐ Puzzle 5 — The Multi-Stage Finale

---

### Dr. NullPointer’s Message:

> “Final door awaits!
> Your challenge:
>
> * Build the smallest possible Docker image for a Go app.
> * Must be under 20MB.
>
> Fail… and I’ll flood your CI logs forever!”

---

### What Learners Must Do

Craft this Dockerfile:

```Dockerfile
FROM golang:1.20 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp .

FROM scratch
COPY --from=builder /app/myapp /myapp
ENTRYPOINT ["/myapp"]
```

✅ Build:

```bash
docker build -t escape-final .
```

✅ Submit image size via:

```bash
docker images escape-final
```

✅ Must be under 20MB → win the game

---

### Dr. NullPointer Taunts:

* “A big-size image is a slow image.”
* “Multi-stage builds? Cute. Let’s see if you can actually do it.”

---

✅ Insight:

> “Multi-stage builds keep images tiny by copying only what you need into a clean runtime image.”

---

# 💻 Web UI Design

---

## Main Game Screen

```
-------------------------------------------
|    DOCKER ESCAPE ROOM CHALLENGE         |
-------------------------------------------
| Puzzle 1 Clue:                          |
| "Find the secret code in vault-volume." |
|                                         |
| [ Enter Your Answer Here ] [ SUBMIT ]   |
-------------------------------------------
| Progress: [####------] 2/5              |
| Score: 20 points                        |
| Time Left: 6m 45s                       |
-------------------------------------------
```

✅ After each puzzle:

* Confetti animation
* Funny villain insults or praises
* Progress bar fills

---

## Game Over Screen

```
-------------------------------------------
|      YOU ESCAPED THE DOCKER VAULT!      |
|                                         |
|   Your Final Score: 47/50               |
|   Time Taken: 8m 23s                    |
|                                         |
| "Congratulations. You are now a true    |
|  Docker Grandmaster."                   |
|                                         |
| [ View Leaderboard ] [ Play Again ]     |
-------------------------------------------
```

---

# 🔥 Random Dr. NullPointer Quotes

✅ Keep things funny and unforgettable:

* “`docker run`? More like `docker ruin`.”
* “Volumes… they’re the dark matter of containers.”
* “I hope you like inspecting things. Because you’re going to be stuck inspecting this vault forever.”

---

# ✅ Benefits for Learners

✅ Master:

* volumes
* networking
* secrets
* resource limits
* multi-stage builds

✅ Get real hands-on practice
✅ Experience Docker like a **puzzle-adventure**
✅ Walk away with:

> “I know how to troubleshoot and solve Docker problems in real life.”

✅ **Adrenaline. Laughter. Lifetime memory.**

---

# ✅ Implementation Blueprint

---

## Folder Structure

```
scenario_05_escape_room/
│
├── webui/
│     ├── app.py
│     ├── templates/
│     │      └── escape.html
│     └── static/
│            └── js/
│
├── puzzles/
│     ├── puzzle1_volume.sh
│     ├── puzzle2_network.sh
│     ├── puzzle3_memory.sh
│     ├── puzzle4_inspect.sh
│     └── puzzle5_multistage/
│            ├── Dockerfile
│            ├── main.go
│
└── docker-compose.yml
```

---

## Puzzle Shell Scripts

Each script:

* Sets up puzzle
* Prints puzzle clue
* Prepares containers

Example puzzle1\_volume.sh:

```bash
#!/bin/bash
docker volume create vault-volume
docker run --rm -v vault-volume:/mnt busybox sh -c "echo 'escape123' > /mnt/secret/code.txt"
```

---

## Web UI

* Flask-based
* Renders puzzle clues
* Accepts answer submissions
* Tracks:

  * progress
  * score
  * time left
* Randomly selects villain taunts

---

## Cleanup Script

```bash
docker volume rm vault-volume
docker network rm networkA networkB
docker rm -f container123 app db
docker rmi escape-final
```

---
