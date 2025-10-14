# 🚀 GitHub Codespaces Quick Start Guide

This workshop is **optimized for GitHub Codespaces** - zero setup, just code and learn!

## Why Codespaces?

✅ **Zero Setup** - Docker and Python pre-installed
✅ **Works Everywhere** - Browser-based, no local dependencies
✅ **Same Experience** - Everyone has identical environment
✅ **Fast** - No local Docker overhead
✅ **Cloud-Powered** - Use GitHub's infrastructure

---

## 🎯 Quick Start (3 Steps)

### 1️⃣ Open in Codespaces

Click the **Code** button → **Codespaces** → **Create codespace on main**

Or use this URL structure:
```
https://github.com/YOUR-USERNAME/YOUR-REPO/codespaces
```

### 2️⃣ Wait for Setup (30 seconds)

Codespace will automatically:
- ✅ Install Python 3.11
- ✅ Setup Docker-in-Docker
- ✅ Configure development environment

### 3️⃣ Start Learning!

Navigate to any scenario and start:
```bash
cd scenario1-testcontainers
python3 setup.py
source venv/bin/activate
python3 workshop.py
```

---

## 🎬 Pro Tips for Codespaces

### Tip 1: Split Terminals

**Perfect for watching Docker containers:**

1. Open a terminal
2. Click the **Split Terminal** icon (or `Cmd+\`)
3. In left terminal: Run workshop
4. In right terminal: Run container watch

```bash
# Terminal 1 (left)
cd scenario1-testcontainers
python3 workshop.py

# Terminal 2 (right)
cd scenario1-testcontainers
./watch-containers.sh
```

### Tip 2: Docker is Built-In

No need to install Docker! It's automatically available:

```bash
# Verify Docker is running
docker --version
docker ps

# Should show Docker info without errors
```

### Tip 3: Port Forwarding

If a scenario runs a web server, Codespaces automatically forwards ports:
- Look for the **PORTS** tab (next to Terminal)
- Click the **globe icon** to open in browser
- Port visibility is automatically set

### Tip 4: Persist Your Work

Codespaces automatically saves your work:
- All files are saved to your fork
- Commit changes: `git add . && git commit -m "Workshop progress"`
- Push changes: `git push`

### Tip 5: Resource Management

Free tier includes:
- 60 hours/month (Core plan)
- 2 cores, 4GB RAM

**Stop your Codespace when done:**
- Click your avatar → **Your codespaces**
- Stop unused Codespaces to save hours

---

## 🐛 Troubleshooting

### Docker not available?

```bash
# Check Docker daemon
docker ps

# If error, try:
sudo dockerd &
sleep 3
docker ps
```

### Port forwarding not working?

1. Go to **PORTS** tab
2. Find your port (e.g., 5001)
3. Right-click → **Port Visibility** → **Public**
4. Click **globe icon** to open

### Terminal not responsive?

1. Click **Terminal** → **Kill Terminal**
2. Open new terminal: `Ctrl+` ` (backtick)
3. Navigate back to your scenario folder

### Python module errors?

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Should show (venv) in prompt
# If not, run setup again:
python3 setup.py
source venv/bin/activate
```

---

## 📚 Workshop Scenarios

### Scenario 1: TestContainers Magic
```bash
cd scenario1-testcontainers
python3 setup.py
source venv/bin/activate
python3 workshop.py
```

**What you'll learn:**
- Why mocks can lie
- How TestContainers uses real databases
- Production parity in testing

**Duration:** 15 minutes

---

## 💡 Best Practices

### Before Starting

1. ✅ Fork the repository to your GitHub account
2. ✅ Create Codespace from YOUR fork
3. ✅ Verify Docker is running: `docker ps`

### During Workshop

1. ✅ Use split terminals (workshop + docker watch)
2. ✅ Read all output carefully
3. ✅ Press ENTER when YOU'RE ready
4. ✅ Experiment and break things!

### After Workshop

1. ✅ Stop your Codespace to save hours
2. ✅ Commit your changes if you want to save progress
3. ✅ Share what you learned!

---

## 🆚 Codespaces vs Local

| Feature | Codespaces | Local |
|---------|-----------|-------|
| Setup Time | 30 seconds | 10-30 minutes |
| Dependencies | Pre-installed | Manual install |
| Docker | Built-in | Need Docker Desktop |
| Environment | Consistent | Varies |
| Access | Anywhere | Local only |
| Resources | GitHub's | Your machine |

**Recommendation:** Use Codespaces for learning, then use locally for your projects!

---

## 🎓 Learning Path

1. **Start with Scenario 1** (TestContainers) - Foundation
2. **Complete all scenarios** - Progressive learning
3. **Experiment on your own** - Break things safely
4. **Apply to your projects** - Real-world practice

---

## 🔗 Helpful Links

- [GitHub Codespaces Docs](https://docs.github.com/en/codespaces)
- [Codespaces Free Tier](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces)
- [TestContainers Python Docs](https://testcontainers-python.readthedocs.io/)

---

## ❓ FAQ

**Q: Do I need to pay for Codespaces?**
A: Free tier includes 60 hours/month. Enough for this workshop!

**Q: Can I use Codespaces for my own projects?**
A: Yes! Great for development and testing.

**Q: Will my work be saved?**
A: Yes, automatically. Commit to save permanently.

**Q: Can I use this locally instead?**
A: Absolutely! Follow instructions in each scenario's README.

**Q: What if I run out of Codespaces hours?**
A: Switch to local development or wait for monthly reset.

---

## 🎉 Ready to Start?

Choose your scenario and begin:

```bash
# Scenario 1: TestContainers Magic
cd scenario1-testcontainers && python3 setup.py && source venv/bin/activate && python3 workshop.py
```

**Happy Learning! 🚀**
