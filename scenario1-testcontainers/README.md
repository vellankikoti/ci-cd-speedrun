# 🧪 Scenario 1: TestContainers Magic

> **Real database testing that catches bugs mocks miss**

**Scenario 1 of 8** in the CI/CD Speed Run workshop. Learn how TestContainers provides real database testing that catches bugs that mocks would miss.

---

## 📋 Quick Links

- [GitHub Codespaces Setup](#-github-codespaces-setup-recommended) ⭐ **START HERE**
- [Local Setup](#-local-setup-alternative)
- [How to Validate](#-validation--testing-checklist)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 What You'll Learn

In **10 minutes**, you'll learn:

1. **The Problem**: Why mock databases give false confidence
2. **The Solution**: How TestContainers provides real database testing
3. **The Magic Moment**: See real constraints catch bugs that mocks miss
4. **Best Practices**: Production-ready integration testing

### The Scenario

You're building a voting system where each user can only vote once. With mocks, your tests pass but production allows unlimited votes! TestContainers catches this bug before deployment.

---

## ⚡ GitHub Codespaces Setup (RECOMMENDED)

### Option 1: One-Click Setup (Easiest)

If you're in GitHub Codespaces, everything is already set up! Just run:

```bash
# Navigate to scenario 1
cd scenario1-testcontainers

# Run setup (creates venv, installs dependencies, tests Docker)
python3 setup.py

# Start the application
python3 app.py
```

That's it! Open http://localhost:5001 in your browser.

---

### Option 2: Step-by-Step Setup (If you want to understand each step)

#### Step 1: Open Terminal in Codespaces

Click on **Terminal** → **New Terminal** in VS Code.

#### Step 2: Navigate to Scenario 1

```bash
cd scenario1-testcontainers
```

#### Step 3: Verify Prerequisites

Check Python and Docker are available:

```bash
# Check Python version (should be 3.11+)
python3 --version

# Check Docker is running (should show "CONTAINER ID" header)
docker ps
```

Expected output:
```
Python 3.11+ (or higher)
CONTAINER ID   IMAGE   ...
```

#### Step 4: Run Setup Script

This script creates a virtual environment, installs dependencies, and tests TestContainers:

```bash
python3 setup.py
```

You should see:
```
🧪 Scenario 1: TestContainers Magic - Setup
==================================================
⚡ CI/CD Speed Run - PyCon ES 2025
🐍 Pure Python Setup - Cross Platform

🐍 Checking Python version...
✅ Python 3.X.X - Compatible
🐳 Checking Docker...
✅ Docker found: Docker version X.X.X
✅ Docker is running
✅ All prerequisites met

📦 Creating virtual environment...
✅ Virtual environment created
📚 Installing dependencies...
✅ Dependencies installed successfully

🧪 Testing TestContainers...
✅ TestContainers imports successful
✅ PostgreSQL test successful: PostgreSQL 15.X
✅ TestContainers test passed!

🎉 Setup Complete!
==================================================
✅ All checks passed
✅ Dependencies installed
✅ TestContainers working

🚀 Ready to run Scenario 1!
```

#### Step 5: Start the Application

```bash
python3 app.py
```

You should see:
```
🧪 Scenario 1: TestContainers Magic
==================================================
⚡ CI/CD Speed Run - PyCon ES 2025

🎯 Learning: Real database testing vs mocks
🔧 Technology: Python + PostgreSQL + TestContainers
⏱️  Time: 10 minutes

🚀 Pre-starting PostgreSQL container...
✅ PostgreSQL ready! (startup: 1.4s)
✅ Ready!
📊 App: http://localhost:5001
🎮 Try voting twice to see the magic!
==================================================
```

#### Step 6: Open the Web Interface

In Codespaces, you'll see a popup saying **"Your application running on port 5001 is available"**.

- Click **"Open in Browser"** or **"Open in Preview"**

Alternatively:
- Go to the **PORTS** tab in VS Code
- Find port **5001**
- Click the **globe icon** to open in browser

#### Step 7: Experience the Magic! 🎯

1. **Vote for a language** (Python, JavaScript, Go, or Rust)
2. **Try to vote again** → 🎯 **MAGIC MOMENT!** Real database catches the duplicate!
3. **See the difference** between mock and TestContainers approaches
4. **Explore the metrics** to understand the benefits

---

## 🖥️ Local Setup (Alternative)

### Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop/))
- **Git** (for cloning)

### Setup Steps

```bash
# 1. Clone the repository (if not already cloned)
git clone https://github.com/vellankikoti/ci-cd-speedrun.git
cd ci-cd-speedrun/scenario1-testcontainers

# 2. Run setup
python3 setup.py

# 3. Start the application
python3 app.py

# 4. Open your browser
open http://localhost:5001
```

---

## ✅ Validation & Testing Checklist

### Quick Validation (2 minutes)

Use this checklist to confirm everything is working:

#### ✅ Step 1: Setup Validation

```bash
cd scenario1-testcontainers
python3 setup.py
```

**Expected**:
- ✅ Python version check passes
- ✅ Docker check passes
- ✅ Virtual environment created
- ✅ Dependencies installed
- ✅ TestContainers test passes

**If any step fails**, see [Troubleshooting](#-troubleshooting) below.

---

#### ✅ Step 2: Application Validation

```bash
python3 app.py
```

**Expected**:
- ✅ PostgreSQL container starts (~1-3 seconds)
- ✅ App runs on http://localhost:5001
- ✅ No error messages

**To verify**:
1. You should see "PostgreSQL ready!" message
2. App should say "Running on http://0.0.0.0:5001"

---

#### ✅ Step 3: Web Interface Validation

Open http://localhost:5001 in your browser.

**Expected to see**:
- ✅ Beautiful purple gradient page
- ✅ Title: "🧪 TestContainers Magic"
- ✅ Four voting options (Python, JavaScript, Go, Rust)
- ✅ Submit Vote button
- ✅ Live Results section
- ✅ Mock vs TestContainers Demo section
- ✅ TestContainers Metrics section

---

#### ✅ Step 4: Core Functionality Validation

**Test 1: First Vote**
1. Click on **Python** (or any language)
2. Click **Submit Vote**
3. ✅ You should see: "Vote for Python recorded!"
4. ✅ Results should show: Python: 1

**Test 2: The Magic Moment! 🎯**
1. Try to vote again (click Submit Vote again)
2. ✅ You should see: "You already voted!"
3. ✅ Message should say: "Real database caught duplicate vote (UNIQUE constraint)"
4. ✅ This is the magic moment - TestContainers caught the bug!

**Test 3: Reset and Vote Again**
1. Click **Reset All Votes**
2. Confirm the reset
3. ✅ Results should show 0 votes
4. Vote for a different language
5. ✅ New vote should be recorded

---

#### ✅ Step 5: API Validation

Test the API endpoints:

```bash
# Test health endpoint
curl http://localhost:5001/api/health

# Expected: {"status":"healthy","scenario":1,"database":"connected","testcontainers":"working"}
```

```bash
# Test results endpoint
curl http://localhost:5001/api/results

# Expected: {"results":[...],"total_votes":X,"database":"real PostgreSQL (TestContainers)"}
```

```bash
# Test metrics endpoint
curl http://localhost:5001/api/metrics

# Expected: {"container":{...},"database":{...},"testcontainers_benefits":[...]}
```

---

#### ✅ Step 6: Testing Validation

**Test with Mocks (Shows the Problem)**

```bash
cd scenario1-testcontainers
python3 tests/test_with_mock.py
```

**Expected output**:
```
❌ MOCK DATABASE TESTING - THE PROBLEM
==================================================
📝 Test 1: First vote
   Result: ✅ PASS
   Votes in mock: 1

📝 Test 2: Duplicate vote (should fail in production)
   Result: ✅ PASS
   Votes in mock: 2
   ⚠️  PROBLEM: Mock allows duplicate vote!

📝 Test 3: Multiple duplicates
   Vote 3: ✅ PASS
   Vote 4: ✅ PASS
   Vote 5: ✅ PASS
   Total votes in mock: 5
   ⚠️  PROBLEM: Same user voted 5 times!
```

✅ **This demonstrates the problem**: Mocks allow unlimited votes!

---

**Test with TestContainers (Shows the Solution)**

```bash
python3 tests/test_with_testcontainers.py
```

**Expected output**:
```
✅ TESTCONTAINERS TESTING - THE SOLUTION
==================================================
🚀 Starting real PostgreSQL container...
✅ PostgreSQL ready! (startup: 2.3s)

📝 Test 1: First vote
   Result: ✅ PASS
   Votes in database: 1

📝 Test 2: Duplicate vote (should fail)
   Result: ❌ FAIL
   🎯 MAGIC: Real database caught duplicate vote!
   Votes in database: 1

📝 Test 3: Different user, same choice
   Result: ✅ PASS
   Total votes in database: 2
```

✅ **This demonstrates the solution**: TestContainers prevents duplicate votes!

---

#### ✅ Step 7: Demo Script Validation

```bash
python3 demo.py
```

**Expected**:
- ✅ Shows mock problem demonstration
- ✅ Shows TestContainers solution demonstration
- ✅ Shows side-by-side comparison
- ✅ All with clear output and explanations

---

### Complete Validation Checklist

- [ ] Setup script runs successfully
- [ ] App starts without errors
- [ ] PostgreSQL container starts (~1-3 seconds)
- [ ] Web interface loads at http://localhost:5001
- [ ] Can vote successfully (first time)
- [ ] Duplicate vote is blocked (magic moment! 🎯)
- [ ] Results update in real-time
- [ ] Reset function works
- [ ] Health API endpoint works
- [ ] Results API endpoint works
- [ ] Metrics API endpoint works
- [ ] Mock tests run and show the problem
- [ ] TestContainers tests run and show the solution
- [ ] Demo script runs successfully

**If all items are checked**, Scenario 1 is working perfectly! ✅

---

## 🧪 Additional Testing Options

### Option 1: Run All Tests with pytest

```bash
cd scenario1-testcontainers
source venv/bin/activate  # On Windows: venv\Scripts\activate
pytest tests/ -v
```

### Option 2: Run Interactive Demo

```bash
python3 demo.py
```

This shows a side-by-side comparison of mock vs TestContainers approaches.

### Option 3: Manual Testing

```bash
# Start the app
python3 app.py

# In another terminal, test the API
curl -X POST http://localhost:5001/api/vote \
  -H "Content-Type: application/json" \
  -d '{"choice":"Python"}'

# Try voting again (should fail)
curl -X POST http://localhost:5001/api/vote \
  -H "Content-Type: application/json" \
  -d '{"choice":"Python"}'
```

---

## 🐳 Docker Testing (Optional)

### Build and Run with Docker

```bash
# Build the Docker image
docker build -t scenario1-testcontainers .

# Run the container
docker run -p 5001:5001 -v /var/run/docker.sock:/var/run/docker.sock scenario1-testcontainers

# Open http://localhost:5001
```

**Note**: The `-v /var/run/docker.sock:/var/run/docker.sock` is required for TestContainers to work inside Docker.

---

## 🔧 Troubleshooting

### Issue 1: "Python version not compatible"

**Problem**: Python version is less than 3.11

**Solution**:
```bash
# Check your Python version
python3 --version

# If < 3.11, install Python 3.11+ from:
# https://www.python.org/downloads/
```

---

### Issue 2: "Docker not found or not running"

**Problem**: Docker is not installed or not running

**Solution**:

**For GitHub Codespaces**:
```bash
# Docker should already be installed and running
# Try restarting the Codespace if Docker is not working
```

**For Local Setup**:
```bash
# 1. Install Docker Desktop from:
#    https://www.docker.com/products/docker-desktop/

# 2. Start Docker Desktop

# 3. Verify Docker is running:
docker ps

# Should show "CONTAINER ID" header
```

---

### Issue 3: "Virtual environment already exists"

**Problem**: Setup script finds existing venv

**Solution**:
```bash
# Remove old virtual environment
rm -rf venv

# Run setup again
python3 setup.py
```

---

### Issue 4: "Port 5001 already in use"

**Problem**: Another application is using port 5001

**Solution**:
```bash
# Find what's using port 5001
lsof -i :5001  # macOS/Linux
netstat -ano | findstr :5001  # Windows

# Kill the process or change the port in app.py (line 354):
# app.run(host='0.0.0.0', port=5002, debug=True)
```

---

### Issue 5: "TestContainers connection failed"

**Problem**: TestContainers can't connect to Docker

**Solution**:
```bash
# Check Docker socket permissions
ls -la /var/run/docker.sock

# If permission denied, try:
sudo chmod 666 /var/run/docker.sock  # Linux

# Or run with sudo (not recommended):
sudo python3 app.py
```

---

### Issue 6: "Module not found" errors

**Problem**: Dependencies not installed

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies manually
pip install -r requirements.txt

# Verify installation
pip list | grep flask
pip list | grep testcontainers
pip list | grep psycopg
```

---

### Issue 7: "PostgreSQL container won't start"

**Problem**: Container startup fails

**Solution**:
```bash
# Check Docker logs
docker logs $(docker ps -q -f ancestor=postgres:15-alpine)

# Pull the image manually
docker pull postgres:15-alpine

# Clean up old containers
docker rm -f $(docker ps -aq)

# Try again
python3 app.py
```

---

### Issue 8: "Page not loading in Codespaces"

**Problem**: Can't access http://localhost:5001 in Codespaces

**Solution**:

1. **Check the PORTS tab** in VS Code
2. Make sure port 5001 is listed
3. Click the **globe icon** next to port 5001
4. If not visible, try: **Ports** → **Forward a Port** → Enter `5001`

---

### Issue 9: "Tests failing"

**Problem**: Tests don't pass

**Solution**:
```bash
# Make sure Docker is running
docker ps

# Activate virtual environment
source venv/bin/activate

# Run tests with more verbosity
python3 tests/test_with_testcontainers.py

# Check for specific error messages
```

---

## 📚 Understanding the Code

### File Structure

```
scenario1-testcontainers/
├── app.py                      # Main Flask application
├── demo.py                     # CLI demonstration script
├── run.py                      # One-command runner
├── setup.py                    # Cross-platform setup script
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
├── README.md                   # This file
├── VERIFICATION.md             # Verification report
├── templates/
│   └── voting.html            # Web interface
└── tests/
    ├── test_with_mock.py      # Mock database tests (shows problem)
    └── test_with_testcontainers.py  # Real tests (shows solution)
```

### Key Concepts

#### 1. Mock Database Problem

**test_with_mock.py** demonstrates how mocks can lie:

```python
class MockDatabase:
    def execute(self, query, params=None):
        # Mock ALWAYS allows inserts - no constraint checking!
        self.votes.append({'user_id': params[0], 'choice': params[1]})
        return True  # ❌ Always succeeds, even for duplicates!
```

**Result**: Tests pass, but production allows unlimited votes! 💥

---

#### 2. TestContainers Solution

**test_with_testcontainers.py** shows real database testing:

```python
with PostgresContainer("postgres:15-alpine") as postgres:
    conn = psycopg.connect(...)

    # First vote succeeds
    submit_vote(conn, "user1", "Python")  # ✅

    # Second vote fails - REAL DATABASE CONSTRAINT!
    submit_vote(conn, "user1", "Python")  # ❌ Caught by UNIQUE constraint!
```

**Result**: Test catches the bug before production! ✅

---

#### 3. The Magic Moment 🎯

The **UNIQUE constraint** in the database:

```sql
CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) UNIQUE NOT NULL,  -- 🎯 This catches duplicates!
    choice VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

When you try to vote twice:
- **Mock**: Allows it (bug slips through)
- **TestContainers**: Blocks it (bug caught!)

---

## 🎓 Learning Outcomes

After completing this scenario, you will understand:

### Problems with Mock Databases ❌

1. **No constraint enforcement** - Mocks don't enforce UNIQUE, PRIMARY KEY, etc.
2. **No real SQL behavior** - Mocks don't test actual database logic
3. **False confidence** - Tests pass but production fails
4. **Miss real bugs** - Data integrity issues slip through

### Benefits of TestContainers ✅

1. **Real database constraints** - Actual PostgreSQL with real constraints
2. **Real SQL behavior** - Tests actual database logic and queries
3. **Real confidence** - If tests pass, production will work
4. **Catch real bugs** - Data integrity issues caught before production
5. **Fast startup** - Containers start in ~1-3 seconds
6. **Automatic cleanup** - No manual database setup/teardown

### Best Practices Learned

1. Use TestContainers for integration tests
2. Test with production-like databases
3. Verify constraints work correctly
4. Catch bugs before they reach production
5. Automate database testing

---

## 🚀 Next Steps

After completing Scenario 1:

1. **✅ Mark complete**: Update your progress in the dashboard
2. **🎯 Move to Scenario 2**: Docker Optimization (2.5GB → 150MB)
3. **📖 Explore more**: Try modifying the database schema
4. **🧪 Experiment**: Add new constraints and test them

---

## 📊 Performance Metrics

What you're running:

- **Container**: PostgreSQL 15 Alpine (77 MB)
- **Startup Time**: ~1-3 seconds
- **Memory Usage**: ~50-100 MB
- **Response Time**: <100ms for API calls
- **Test Execution**: ~5-10 seconds

---

## 🤝 Contributing

Found a bug or want to improve this scenario?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📞 Support

Need help?

- **GitHub Issues**: [Create an issue](https://github.com/vellankikoti/ci-cd-speedrun/issues)
- **Email**: vellankikoti@gmail.com
- **Documentation**: This README and [VERIFICATION.md](VERIFICATION.md)

---

## 📝 Additional Resources

### Official Documentation

- [TestContainers Python](https://testcontainers-python.readthedocs.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [psycopg3 Documentation](https://www.psycopg.org/psycopg3/)

### Related Topics

- Integration testing best practices
- Database constraint design
- Docker container management
- CI/CD pipeline testing

---

## 🌟 Key Takeaways

### Remember These Points

1. **Mocks can lie** - They don't test real database behavior
2. **TestContainers tells the truth** - Real database, real constraints
3. **Constraints are your friends** - They prevent data integrity bugs
4. **Test like production** - Use production-like databases in tests
5. **Catch bugs early** - Integration tests catch bugs before deployment

### The Magic Moment 🎯

When the real database catches a duplicate vote that mocks would miss - that's the power of TestContainers!

---

**Ready to experience TestContainers magic? Let's go! 🚀**

**Start here**: [GitHub Codespaces Setup](#-github-codespaces-setup-recommended)

*This scenario demonstrates why real database testing beats mock testing - catch bugs before they reach production!*

---

**Made with ❤️ for PyCon ES 2025**
