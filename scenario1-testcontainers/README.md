# 🔥 Scenario 1: TestContainers Magic

> **"If your tests don't face reality, your users will."**

An interactive workshop designed for **GitHub Codespaces** where 100+ participants can run simultaneously without Docker image download delays or WiFi congestion.

---

## 🚀 START HERE (GitHub Codespaces - RECOMMENDED)

### Why Codespaces?

✅ **No Docker image downloads** - Pre-downloaded in container
✅ **No WiFi congestion** - No 100 people downloading 500MB images
✅ **No setup time** - Ready in 30 seconds
✅ **Same environment** - Everyone has identical setup
✅ **Just works** - No "it works on my machine"

---

## 📋 Quick Start (3 Steps)

### Step 1: Open in Codespaces (10 seconds)

**Option A: From GitHub UI**
1. Click **Code** button
2. Click **Codespaces** tab
3. Click **Create codespace on main**

**Option B: Direct URL**
```
https://github.com/YOUR-USERNAME/YOUR-REPO/codespaces
```

### Step 2: Wait for Setup (20 seconds)

Codespace automatically:
- ✅ Installs Python 3.11
- ✅ Sets up Docker-in-Docker
- ✅ **Pre-downloads postgres:15-alpine & redis:7-alpine** (NO WiFi delay!)
- ✅ Installs Python dependencies
- ✅ Forwards port 5001

You'll see: `🎉 Codespace setup complete!`

**If you get virtual environment errors:**
```bash
python3 fix_venv.py  # Automatically fixes venv issues
```

### Step 3: Choose Your Experience

```bash
cd scenario1-testcontainers
```

Then pick one:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  🎭 THE SHOW (8 minutes)                                    │
│     For: Live presentation, audience participation         │
│     Run: python3 reality_engine.py                         │
│     URL: Codespaces auto-forwards to browser               │
│                                                             │
│  ────────────────────────────────────────────────────────  │
│                                                             │
│  🎓 THE WORKSHOP (15 minutes)                               │
│     For: Self-paced learning, deep understanding           │
│     Run: python3 workshop.py                               │
│                                                             │
│  ────────────────────────────────────────────────────────  │
│                                                             │
│  🧪 THE TESTS (See the proof)                               │
│     Fantasy: pytest tests/test_fantasy.py -v               │
│     Reality: pytest tests/test_reality.py -v               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 What You'll Learn

1. **Reality beats mocks** - Real databases catch bugs mocks miss
2. **Confidence is a feature** - Disposable infrastructure = zero flake
3. **Resilience is testable** - Prove graceful failure & recovery

**The Core Concept:**

```python
# ❌ Mock - NO constraints
db.insert_vote("user123", "Python")
db.insert_vote("user123", "Python")  # ✅ Passes (BUG!)

# ✅ TestContainers - REAL constraints
with PostgresContainer("postgres:15-alpine") as pg:
    cursor.execute("INSERT ...")  # ✅ First succeeds
    cursor.execute("INSERT ...")  # ❌ BLOCKED! (Caught!)
```

---

## 🎭 The Show: Reality Engine (8-Min Demo)

**Perfect for presenting to an audience in Codespaces**

### Run It

```bash
python3 reality_engine.py
```

**What happens:**
- Codespaces shows popup: "Application available on port 5001"
- Click **Open in Browser** → Dashboard opens
- QR code displayed → Audience scans with phones
- Split screen: Lifecycle events (left) + Voting (right)

### The Experience

| Time | What Happens | Audience Sees |
|------|-------------|---------------|
| 0:00 | Cold open | "Tests were green. Monday: outage." |
| 1:30 | QR voting | Everyone votes on phones → Try twice! |
| 2:00 | Magic moment | "You already voted!" → UNIQUE constraint blocked it |
| 3:30 | Test comparison | Fantasy (lie) vs Reality (truth) |
| 4:30 | Chaos | Kill Redis → System continues → **Resilience!** |
| 7:30 | Mic drop | "If tests don't face reality, users will." |

### Presenter Controls

- **Enable Rate Limit** → Spins up Redis, enforces 3 req/min
- **Inject Chaos** → Kills Redis, shows graceful degradation
- **Reset Everything** → Clean slate for next demo

### QR Code for Audience

**In Codespaces:**
- Dashboard shows QR automatically
- Audience scans → Opens `/qr` page
- Phones hit **real PostgreSQL** with **real UNIQUE constraints**
- Try voting twice → Second vote **BLOCKED!** ← Magic moment

---

## 🎓 The Workshop: Interactive CLI (15-Min Learning)

**Perfect for self-paced deep learning**

### Run It

```bash
python3 workshop.py
```

### What Happens

**Section 1: The Problem (5 min)**
- See mock tests pass with duplicate votes (the lie)

**Section 2: The Magic (5 min)**
- PostgreSQL container starts in <2s (pre-downloaded!)
- Real constraint blocks duplicates (the truth)
- Watch containers in real-time

**Section 3: Comparison (2 min)**
- Side-by-side: Mock vs TestContainers

**Section 4: Hands-On (3 min)**
- Write your own test
- E-commerce SKU uniqueness

### Watch Containers (Optional)

**Open a 2nd terminal:**

```bash
python3 watch_containers.py
```

See containers appear/disappear in real-time!

---

## 🧪 The Tests: Fantasy vs Reality

### Run Both

```bash
# The lie (mocks allow duplicates)
pytest tests/test_fantasy.py -v

# The truth (TestContainers blocks duplicates)
pytest tests/test_reality.py -v

# Compare side-by-side
pytest tests/ -v
```

**Output:**
```
test_fantasy.py::test_duplicate_vote_should_fail ✅ PASSED (LIE!)
test_reality.py::test_duplicate_vote_is_blocked ✅ PASSED (TRUTH!)

Fantasy: 3 passed in 0.01s (all green, all wrong)
Reality: 4 passed in 1.90s (green means proof!)
```

---

## 🏗️ How It Works (Architecture)

```
Your Browser (Codespaces forwarded)
    ↕
Flask App (reality_engine.py)
    ↕
PostgreSQL Container (pre-downloaded!)
    - UNIQUE constraint on user_id
    - Blocks duplicate votes
    - Real production behavior
```

**Key Point:** PostgreSQL image is **pre-downloaded** when Codespace starts. No waiting, no WiFi congestion!

---

## 🔧 Codespaces-Specific Features

### Automatic Port Forwarding

When you run `python3 reality_engine.py`:
1. Codespaces detects port 5001
2. Shows notification: "Application available"
3. Click **Open in Browser** → Dashboard opens
4. Share URL with audience for QR voting

### Pre-Downloaded Docker Images

`.devcontainer/setup.sh` runs on Codespace creation:
```bash
docker pull postgres:15-alpine  # Downloaded once, used by all
docker pull redis:7-alpine      # No WiFi delay during workshop!
```

### Split Terminal Setup

```
┌──────────────────────────────────────────┐
│ Terminal 1    │ Terminal 2               │
│ Workshop      │ Container Monitor        │
│               │                          │
│ $ python3     │ $ python3                │
│   reality_    │   watch_containers.py    │
│   engine.py   │                          │
│               │ 🔍 Live container feed   │
└──────────────────────────────────────────┘
```

---

## 🛠️ All Python Scripts (No Bash!)

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `setup.py` | One-time environment setup | Auto-run by Codespaces |
| `reality_engine.py` | 8-min theatrical demo | Presenting to audience |
| `workshop.py` | 15-min interactive learning | Self-paced exploration |
| `watch_containers.py` | Real-time container monitor | Optional 2nd terminal |
| `cleanup.py` | Remove all containers/cache | Between demos or after workshop |

**No shell scripts = Works everywhere (Windows, Mac, Linux, Codespaces)**

---

## 🧹 Cleanup (After Workshop)

```bash
python3 cleanup.py
```

**What it does:**
- Stops Flask apps
- Removes all TestContainers
- Removes PostgreSQL & Redis containers
- Cleans orphaned networks/volumes
- Clears pytest cache

---

## 📊 Performance in Codespaces

**With Pre-Downloaded Images:**

| Action | Time | Notes |
|--------|------|-------|
| Codespace startup | 30s | One-time setup |
| Image pull | 0s | Already downloaded! |
| PostgreSQL start | 1-2s | Fast! |
| Redis start | 1s | Instant! |
| Workshop runtime | 15min | Smooth experience |

**Why This Matters:**
- **100 participants** × **0 seconds image download** = **No WiFi congestion!**
- Everyone starts at the same time
- No "waiting for Docker" delays
- Professional workshop experience

---

## 🎓 Workshop Flow (For Instructors)

### Before Workshop (5 minutes)

```bash
# 1. Open Codespace
# 2. Verify setup
cd scenario1-testcontainers
docker images | grep postgres  # Should see postgres:15-alpine
docker images | grep redis     # Should see redis:7-alpine

# 3. Test run
python3 reality_engine.py     # Verify it starts
# Ctrl+C to stop

# 4. Ready!
```

### During Workshop (15 minutes)

```bash
# Option A: Live demo
python3 reality_engine.py
# Share Codespaces URL for QR voting
# Run through 8-minute show

# Option B: Self-paced
python3 workshop.py
# Participants follow along
```

### After Workshop (2 minutes)

```bash
# Cleanup
python3 cleanup.py

# Verify clean
docker ps  # Should show nothing
```

---

## 🔧 Troubleshooting (Codespaces)

### Virtual Environment Issues?

**Symptom:** `cannot execute: required file not found` or `pip3: command not found`

**Solution:**
```bash
# Automatic fix
python3 fix_venv.py

# Manual fix
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Port Not Forwarding?

**Solution:**
1. Go to **PORTS** tab (next to Terminal)
2. Find port 5001
3. Right-click → **Port Visibility** → **Public**
4. Click **globe icon** to open

### Containers Not Starting?

**Solution:**
```bash
# Check Docker
docker ps  # Should work (auto-available in Codespaces)

# Check images
docker images | grep postgres  # Should see postgres:15-alpine

# If missing, manually pull
docker pull postgres:15-alpine
```

### QR Code Not Working?

**Solution:**
- QR code uses Codespaces forwarded URL automatically
- Make sure port 5001 is set to **Public** visibility
- Share the URL from PORTS tab with audience

### App Won't Start?

**Solution:**
```bash
# Check if port is in use
lsof -i :5001

# Kill process if needed
pkill -f "python.*app.py"

# Restart
python reality_engine.py
```

---

## 🎯 Key Concepts & Best Practices

### Production Parity

```python
# ❌ Mock: Simulates, doesn't enforce
mock.insert()  # Always succeeds

# ✅ Reality: Same engine as production
cursor.execute("INSERT ...")  # Real constraints!
```

### Hermetic Testing

```python
def test_a():
    with PostgresContainer() as pg:  # Fresh!
        # Isolated, no state pollution

def test_b():
    with PostgresContainer() as pg:  # Fresh again!
        # Each test independent
```

### Fast Enough to Matter

```bash
$ time pytest tests/test_reality.py
# 1.90 seconds total (including container startup!)
# Fast enough for CI, fast enough for local dev
```

---

## 📚 Resources

- **TestContainers Python:** https://testcontainers-python.readthedocs.io/
- **GitHub Codespaces:** https://docs.github.com/en/codespaces
- **Workshop Repository:** [Your GitHub link]

---

## ❓ FAQ

**Q: Why Codespaces instead of local?**
A: For workshops with 100+ participants, Codespaces eliminates:
- Docker image download delays (pre-downloaded)
- WiFi congestion (everyone pulling 500MB images)
- "Works on my machine" issues (identical environments)

**Q: Do I need a GitHub Codespaces subscription?**
A: Free tier includes 60 hours/month (enough for multiple workshops)

**Q: Can I still run locally?**
A: Yes! Just run `python3 setup.py` and follow along. But Codespaces is highly recommended for workshops.

**Q: What if Codespaces is slow?**
A: Unlikely! Images are pre-downloaded. If it happens, check `.devcontainer/setup.sh` ran successfully.

---

## 🎉 The Promise

After this scenario:

✅ You'll never trust mock-only tests
✅ You'll understand production parity viscerally
✅ You'll test with real infrastructure confidently
✅ You'll remember: **"If tests don't face reality, users will."**

---

## 🚀 Ready? Open in Codespaces!

```bash
# In Codespaces terminal
cd scenario1-testcontainers

# Pick your experience
python3 reality_engine.py  # The Show (8 min)
python3 workshop.py        # The Workshop (15 min)
pytest tests/ -v           # The Tests (compare)

# Dive in! 🔥
```

---

## 📁 File Structure

```
scenario1-testcontainers/
├── README.md                 📚 This file (Codespaces-optimized!)
├── reality_engine.py         🎭 8-min show (with pre-flight checks)
├── workshop.py               🎓 15-min workshop
├── tests/
│   ├── test_fantasy.py       ❌ Mocks (the lie)
│   └── test_reality.py       ✅ TestContainers (truth)
├── templates/
│   ├── reality_engine.html   Dashboard
│   └── qr_vote.html          Mobile voting
├── setup.py                  Environment setup
├── requirements.txt          Python dependencies
├── cleanup.py                🧹 Cleanup script (Python!)
└── watch_containers.py       👀 Container monitor (Python!)

../.devcontainer/
├── devcontainer.json         Codespaces config
└── setup.sh                  Pre-download Docker images
```

**All Python. No shell scripts. Works everywhere.** ✨
