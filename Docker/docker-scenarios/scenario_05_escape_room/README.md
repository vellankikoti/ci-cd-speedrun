# 🚀 Docker Escape Room Challenge

> **Transform learners from Docker users into Docker HEROES through gamified learning!**

## 🎯 What is this?

The **Docker Escape Room Challenge** is an interactive, gamified learning experience where participants are "kidnapped" by the villain **Dr. NullPointer** and must solve 5 Docker puzzles to escape the "Docker Vault."

## 🧩 The Story

You and your workshop friends have been **kidnapped by Dr. NullPointer, the evil villain of the cloud.** He's locked you inside the **Docker Vault**, a high-security digital prison guarded by containers.

To escape, you must:
- Solve five Docker puzzles
- Discover hidden secrets
- Hack your way through broken networks
- Outsmart containers with memory issues
- Master multi-stage builds to save your digital life!

Fail…and you'll be trapped running endless `hello-world` containers for eternity.

## 🕹️ The Five Puzzles

### 1. The Secret Vault (Volumes)
**Challenge:** Find the secret code hidden in a Docker volume
**Learning:** Volume mounting and data persistence
**Command:** `docker run --rm -v vault-volume:/mnt busybox cat /mnt/secret/code.txt`

### 2. The Broken Bridge (Networking)
**Challenge:** Fix network connectivity between isolated containers
**Learning:** Docker networks and container communication
**Command:** `docker network connect networkA redis-server`

### 3. The Out-of-Memory Monster
**Challenge:** Fix a container that keeps crashing due to memory limits
**Learning:** Resource constraints and limits
**Command:** `docker run -d --memory=512m busybox sh -c "dd if=/dev/zero of=/dev/null bs=1M"`

### 4. Secrets in Plain Sight
**Challenge:** Find environment variables in a running container
**Learning:** Container inspection and debugging
**Command:** `docker inspect container123`

### 5. The Multi-Stage Finale
**Challenge:** Build the smallest possible Docker image (<20MB)
**Learning:** Multi-stage builds and image optimization
**Command:** Create multi-stage Dockerfile and build

## 🚀 Quick Start

### Prerequisites
- Docker installed and running
- Docker Compose (optional, for easy deployment)

### Option 1: Run with Docker Compose (Recommended)

```bash
# Clone and navigate to the project
cd Docker/docker-scenarios/scenario_05_escape_room

# Start the escape room
docker-compose up --build

# Open your browser to http://localhost:5000
```

### Option 2: Run directly with Python

```bash
# Navigate to the webui directory
cd webui

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open your browser to http://localhost:5000
```

### Option 3: Run with Docker

```bash
# Build and run the container
docker build -t escape-room ./webui
docker run -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock escape-room

# Open your browser to http://localhost:5000
```

## 🎮 How to Play

1. **Open the web interface** at `http://localhost:5000`
2. **Read Dr. NullPointer's clues** for each puzzle
3. **Use your terminal** to run real Docker commands
4. **Submit your answers** in the web interface
5. **Progress through all 5 puzzles** to escape!

## 🏆 Game Features

- **Real-time scoring** (+10 points per puzzle, -3 for failed attempts)
- **Progress tracking** with visual progress bar
- **Timer** to add urgency
- **Funny taunts** from Dr. NullPointer for wrong answers
- **Success messages** for correct solutions
- **Confetti celebration** when completing puzzles
- **Final certificate** upon escape

## 🧹 Cleanup

After playing, clean up all Docker resources:

```bash
# Run the cleanup script
./cleanup.sh

# Or manually clean up
docker-compose down
docker system prune -f
```

## 📚 Learning Objectives

By completing the Docker Escape Room Challenge, participants will master:

- ✅ **Docker Volumes** - Data persistence across containers
- ✅ **Docker Networks** - Container communication and isolation
- ✅ **Resource Limits** - Memory and CPU constraints
- ✅ **Container Inspection** - Debugging and troubleshooting
- ✅ **Multi-stage Builds** - Image optimization and size reduction

## 🛠️ Technical Architecture

```
scenario_05_escape_room/
├── webui/                    # Flask web application
│   ├── app.py               # Main game logic
│   ├── templates/           # HTML templates
│   │   ├── escape.html     # Main game interface
│   │   └── complete.html   # Victory screen
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Container configuration
├── puzzles/                # Puzzle setup scripts
│   ├── puzzle1_volume.sh
│   ├── puzzle2_network.sh
│   ├── puzzle3_memory.sh
│   ├── puzzle4_inspect.sh
│   └── puzzle5_multistage/
│       ├── setup.sh
│       ├── main.go
│       └── Dockerfile
├── docker-compose.yml     # Orchestration
├── cleanup.sh            # Resource cleanup
└── README.md            # This file
```

## 🎯 Educational Benefits

- **Hands-on practice** with real Docker commands
- **Problem-solving** in realistic scenarios
- **Gamification** for engagement and retention
- **Humor** to make learning memorable
- **Progressive difficulty** from basic to advanced concepts

## 🔧 Customization

### Adding New Puzzles

1. Add puzzle configuration to `webui/app.py`
2. Create setup script in `puzzles/`
3. Update templates if needed

### Modifying Game Mechanics

- Edit scoring system in `webui/app.py`
- Add new taunts or success messages
- Modify time limits or difficulty

## 🐛 Troubleshooting

### Common Issues

1. **Permission denied on Docker socket**
   ```bash
   sudo chmod 666 /var/run/docker.sock
   ```

2. **Port 5000 already in use**
   ```bash
   # Change port in docker-compose.yml or app.py
   ```

3. **Puzzle setup fails**
   ```bash
   # Check Docker is running
   docker ps
   
   # Run cleanup and try again
   ./cleanup.sh
   ```

### Debug Mode

Run with debug logging:

```bash
FLASK_DEBUG=1 python app.py
```

## 📄 License

This project is part of the CI/CD Chaos Workshop educational materials.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the Docker Escape Room Challenge!

---

**Ready to escape Dr. NullPointer's Docker Vault? Start the challenge now!** 🚀 