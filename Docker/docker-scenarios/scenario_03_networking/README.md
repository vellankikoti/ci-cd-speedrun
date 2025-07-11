# 🧙‍♂️ Docker Networking Magic — Step-by-Step for Everyone!

## 🥇 What are we doing?
We’re going to run a voting website in Docker, break it in fun ways, and then fix it together! You’ll see how computers talk to each other in containers.

---

## 1️⃣ Step 1: Run the App Without a Database (and see it break!)

1. **Open your terminal.**
2. **Go to the scenario folder:**
   ```bash
   cd Docker/docker-scenarios/scenario_03_networking
   ```
3. **Make all scripts ready to run:**
   ```bash
   chmod +x scripts/*.sh
   ```
4. **Run the first script:**
   ```bash
   ./scripts/run_app_without_db.sh
   ```
5. **Open your web browser and go to:**  
   [http://localhost:5000](http://localhost:5000)
6. **Try to vote!**
   - The page will crash when you click a button.  
   - That’s because the app can’t find its database (Redis)!
   - You’ll see an error in the terminal.

**Lesson:** Apps need their databases to work!

---

## 2️⃣ Step 2: Add the Database, But… Oops! Wrong Network

1. **Stop the old app (the script does this for you).**
2. **Run the next script:**
   ```bash
   ./scripts/run_app_with_db_wrong_network.sh
   ```
3. **Go to [http://localhost:5000](http://localhost:5000) again.**
4. **Try to vote!**
   - Still broken!  
   - The app can’t “see” the database, even though it’s running.

**Lesson:** Containers need to be in the same “network” to talk!

---

## 3️⃣ Step 3: Fix the Network — Make the Magic Happen!

1. **Run the magic fix script:**
   ```bash
   ./scripts/fix_network.sh
   ```
2. **Go to [http://localhost:5000](http://localhost:5000) again.**
3. **Try to vote!**
   - It works! Votes go up!
   - The app and database are now friends in the same network.

**Lesson:** Docker networks are like secret clubhouses. Only members can talk!

---

## 4️⃣ Step 4: Share the Fun — Make Your App Public!

### Option A: Use ngrok (easy way to share)

1. **Install ngrok if you don’t have it:**
   - On Mac: `brew install ngrok/ngrok/ngrok`
   - On Windows: [Download from ngrok.com](https://ngrok.com/download)
2. **Run the script:**
   ```bash
   ./scripts/expose_ngrok.sh
   ```
3. **Copy the public link from the terminal and share it with friends!**

### Option B: Use Cloudflare Tunnel (another way)

1. **Install cloudflared if you don’t have it:**
   - On Mac: `brew install cloudflared`
   - On Windows: [Download from developers.cloudflare.com](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/)
2. **Run the script:**
   ```bash
   ./scripts/expose_cloudflared.sh
   ```
3. **Copy the public link and share!**

---

## 5️⃣ Step 5: Clean Up

When you’re done, clean up everything:

```bash
./scripts/cleanup.sh
```

---

# 🎉 That’s it! You’re a Docker Networking Wizard!

- You saw how apps and databases need to be in the same network.
- You learned how to fix broken connections.
- You even shared your app with the world!

---

## 🧩 Troubleshooting (If you get stuck)

- If a script says “permission denied,” run: `chmod +x scripts/*.sh`
- If you see “port already in use,” run: `./scripts/cleanup.sh` and try again.
- If you want to start over, always run the cleanup script first. 