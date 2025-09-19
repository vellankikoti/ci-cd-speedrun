# 🎥 Streaming Server with Docker

Run a live streaming server locally with Owncast, connect OBS Studio, and share publicly.

## 🚀 Quick Start

### 1. Install Docker

**macOS:**
```bash
brew install --cask docker
```

**Linux:**
```bash
sudo apt update && sudo apt install -y docker.io
sudo systemctl start docker
sudo usermod -aG docker $USER
```

**Windows:**
Download from [docker.com](https://www.docker.com/products/docker-desktop/)

### 2. Run Owncast

```bash
docker run -d -p 8080:8080 -p 1935:1935 owncast/owncast
```

**Access:**
- Web: http://localhost:8080
- Admin: http://localhost:8080/admin (admin/abc123)
- RTMP: rtmp://localhost:1935/live

### 3. Configure OBS Studio

**Stream Settings:**
- Service: Custom...
- Server: `rtmp://localhost:1935/live`
- Stream Key: Get from Owncast admin panel

**Add Sources:**
- Video Capture Device (webcam)
- Display Capture (screen share)
- Media Source (video files)

### 4. Start Streaming

1. Click "Start Streaming" in OBS
2. View at http://localhost:8080


## ⭐ One-Liner Workflow

```bash
# Start streaming server
docker run -d -p 8080:8080 -p 1935:1935 owncast/owncast

# Expose publicly (choose one)
ngrok http 8080                                    # Quick demo
cloudflared tunnel run owncast-tunnel             # Production
```

## 🎯 What You Get

✅ **Local streaming server** - Owncast in Docker  
✅ **Live streaming** - OBS Studio integration  
✅ **Professional setup** - Your own domain streaming  
