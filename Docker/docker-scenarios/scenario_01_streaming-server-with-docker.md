# 🎥 Streaming Server with Docker — Complete Guide (macOS, Linux, Windows)

This document shows how to:

✅ Run a live streaming server locally  
✅ Connect OBS Studio for live video  
✅ Share your stream publicly via ngrok  
✅ Host your stream on your own domain using Cloudflare Tunnel

We’ll use **Owncast**, an open-source, self-hosted streaming platform that runs entirely in Docker.

---

# 🚀 1. Run Streaming Server Locally

## ✅ 1.1 Install Docker

---

### macOS

Install Homebrew if you don’t have it:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
````

Then install Docker:

```bash
brew install --cask docker
```

Start Docker Desktop after install.

---

### Linux

#### Debian / Ubuntu:

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

Add your user to the docker group:

```bash
sudo usermod -aG docker $USER
```

Then log out and log back in.

---

#### RHEL / CentOS:

```bash
sudo yum install -y docker
sudo systemctl enable docker
sudo systemctl start docker
```

---

### Windows

* Download Docker Desktop:
  [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

* Install and run Docker Desktop.

✅ Confirm Docker works:

```bash
docker --version
```

---

## ✅ 1.2 Run Owncast

Run Owncast container:

```bash
docker run -d \
  -p 8080:8080 \
  -p 1935:1935 \
  owncast/owncast
```

✅ Owncast will run locally:

* Web page:

  ```
  http://localhost:8080
  ```

* RTMP ingest:

  ```
  rtmp://localhost:1935/live
  ```

---

## ✅ 1.3 Access Admin Panel

Visit:

```
http://localhost:8080/admin
```

Default credentials:

```
Username: admin
Password: abc123
```

Go to:

```
Server Setup → Stream Settings
```

✅ Copy:

* RTMP URL:

  ```
  rtmp://localhost:1935/live
  ```
* Stream Key:
  e.g. `abc123xyz`

---

# 🎥 2. Install OBS Studio

---

## ✅ macOS

Install via Homebrew:

```bash
brew install --cask obs
```

Or download:
[https://obsproject.com/](https://obsproject.com/)

---

## ✅ Linux

For Ubuntu:

```bash
sudo add-apt-repository ppa:obsproject/obs-studio
sudo apt update
sudo apt install obs-studio
```

---

## ✅ Windows

Download and install:
[https://obsproject.com/](https://obsproject.com/)

---

# 🎛️ 3. Configure OBS for Streaming

---

## ✅ Step 1 — Stream Settings

In OBS:

* Go to:

  ```
  Settings → Stream
  ```
* Choose:

  ```
  Service: Custom...
  Server: rtmp://localhost:1935/live
  Stream Key: <your stream key>
  ```

Replace with your actual stream key from Owncast.

---

## ✅ Step 2 — Add Video Sources

In OBS:

✅ **Add Webcam**

* Click ➕ under “Sources.”
* Choose:

  ```
  Video Capture Device
  ```
* Pick your webcam.

---

✅ **Share Your Screen**

* Click ➕ under “Sources.”

  * macOS:

    ```
    macOS Screen Capture
    ```
  * Windows:

    ```
    Display Capture
    ```
  * Linux:

    ```
    Screen Capture (XSHM) or PipeWire
    ```

* Select your display or window.

---

✅ **Play a Video File**

* Click ➕ under “Sources.”
* Choose:

  ```
  Media Source
  ```
* Pick a video file (e.g. mp4).

---

## ✅ Step 3 — Start Streaming

* Click:

  ```
  Start Streaming
  ```

---

## ✅ Step 4 — View Your Stream

Visit:

```
http://localhost:8080
```

✅ You should see your live video!

---

# 🌎 4. Share Your Local Stream Publicly (ngrok)

Perfect for quick demos without cloud servers.

---

## ✅ Step 1 — Install ngrok

---

### macOS

```bash
brew install ngrok/ngrok/ngrok
```

Or download:

[https://ngrok.com/download](https://ngrok.com/download)

---

### Linux

Download the binary from:

[https://ngrok.com/download](https://ngrok.com/download)

Unzip it and move it to `/usr/local/bin`.

Example:

```bash
unzip ngrok-v3-stable-linux-amd64.zip
sudo mv ngrok /usr/local/bin/
```

---

### Windows

Download and install from:

[https://ngrok.com/download](https://ngrok.com/download)

---

## ✅ Step 2 — Authenticate ngrok

Sign up for a free account. Copy your auth token.

Run:

```bash
ngrok config add-authtoken YOUR_TOKEN_HERE
```

---

## ✅ Step 3 — Run ngrok

Run:

```bash
ngrok http 8080
```

✅ ngrok will give you a URL like:

```
https://funny-lion-1234.ngrok.io
```

✅ Share this link → your stream is globally accessible!

---

## 🚫 Limitations

* ngrok shares only **web page traffic (port 8080).**
* RTMP streaming from outside (port 1935) will not work through ngrok.
* Perfect for demo viewing by others.

---

# 🌐 5. Host Streaming on Your Own Domain (Cloudflare Tunnel)

For a professional, permanent solution.

---

## ✅ Step 1 — Prerequisites

✅ You need:

* A domain (e.g. yourdomain.com)
* Cloudflare account managing that domain
* Docker + cloudflared installed

---

## ✅ Step 2 — Install cloudflared

---

### macOS

```bash
brew install cloudflared
```

---

### Linux

Debian/Ubuntu:

```bash
sudo apt install cloudflared
```

Or download binary:

[https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/)

---

### Windows

Download and install:

[https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/)

---

## ✅ Step 3 — Login to Cloudflare

Run:

```bash
cloudflared tunnel login
```

A browser window opens → log in.

---

## ✅ Step 4 — Create a Tunnel

Run:

```bash
cloudflared tunnel create owncast-tunnel
```

Example output:

```
Tunnel credentials written to /Users/koti/.cloudflared/324500d1-4ab0b-a4694083b668.json
```

---

## ✅ Step 5 — Create Config File

Create:

```
/Users/koti/.cloudflared/config.yml
```

Example content:

```yaml
tunnel: owncast-tunnel
credentials-file: /Users/koti/.cloudflared/324500d1-a4694083b668.json

ingress:
  - hostname: stream.yourdomain.com
    service: http://localhost:8080
  - service: http_status:404
```

✅ Replace:

* `stream.yourdomain.com` → your subdomain
* path to your credentials file

---

## ✅ Step 6 — Route DNS

Run:

```bash
cloudflared tunnel route dns owncast-tunnel stream.yourdomain.com
```

✅ This creates a DNS CNAME record:

```
stream.yourdomain.com → <your-tunnel-id>.cfargotunnel.com
```

---

## ✅ Step 7 — Run Tunnel

First run Owncast:

```bash
docker run -d -p 8080:8080 -p 1935:1935 owncast/owncast
```

Then start your tunnel:

```bash
cloudflared tunnel run owncast-tunnel
```

✅ Your stream is live:

```
https://stream.yourdomain.com
```

---

# ⭐ Your One-Liner Workflow

Every time you want to go live publicly:

```bash
docker run -d -p 8080:8080 -p 1935:1935 owncast/owncast
cloudflared tunnel run owncast-tunnel
```

✅ That’s it!

---

# 🎯 Summary

✅ Local streaming server → Owncast in Docker
✅ Stream live with OBS
✅ Share demos via ngrok
✅ Host live streams on your own domain via Cloudflare Tunnel

Enjoy building your streaming empire!

