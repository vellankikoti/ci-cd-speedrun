#!/usr/bin/env python3
"""
🔥 THE REALITY ENGINE 🔥
========================

"If your tests don't face reality, your users will."

A theatrical TestContainers experience that makes the audience *feel*
why production-parity testing matters.

Runtime: 8 minutes
Outcome: Lifelong "aha" moment
"""

import os
import sys
import time
import uuid
import json
import threading
import subprocess
import logging
from datetime import datetime
from collections import defaultdict
from flask import Flask, render_template, jsonify, request, session, Response
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==============================================================================
# PRE-FLIGHT CHECKS
# ==============================================================================

def check_docker():
    """Verify Docker is running and accessible"""
    # First try to find Docker using which/where
    docker_cmd = None
    
    # Try which command first (works in most environments)
    try:
        which_result = subprocess.run(['which', 'docker'], capture_output=True, text=True, timeout=2)
        if which_result.returncode == 0 and which_result.stdout.strip():
            docker_cmd = which_result.stdout.strip()
    except:
        pass
    
    # If which didn't work, try common paths
    if not docker_cmd:
        docker_paths = [
            '/usr/local/bin/docker',  # Codespaces + macOS
            '/usr/bin/docker',         # Linux
            '/opt/homebrew/bin/docker', # macOS ARM
            '/usr/bin/docker.io',      # Some Linux distros
            'docker'                   # Fallback to PATH
        ]
        
        for path in docker_paths:
            if path == 'docker':
                # Try direct command
                try:
                    result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=2)
                    if result.returncode == 0:
                        docker_cmd = 'docker'
                        break
                except:
                    continue
            elif os.path.exists(path):
                docker_cmd = path
                break

    if not docker_cmd:
        print("❌ Docker not found!")
        print()
        in_codespaces = os.getenv('CODESPACES') == 'true'

        if in_codespaces:
            print("💡 FIX: Your Codespace needs Docker installed")
            print()
            print("   Run this Python script for detailed instructions:")
            print("   → python3 check_environment.py")
            print()
            print("   Quick fix: Rebuild your Codespace")
            print("   • Press F1 → 'Codespaces: Rebuild Container'")
        else:
            print("💡 Solutions:")
            print("   • Run: python3 check_environment.py")
            print("   • Install Docker Desktop")
        sys.exit(1)

    # Test Docker
    try:
        result = subprocess.run([docker_cmd, 'ps'], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("❌ Docker not running!")
            print(f"   Path: {docker_cmd}")
            print(f"   Error: {result.stderr}")
            print("\n💡 Solutions:")
            print("   • Codespaces: Docker should auto-start")
            print("   • Local: Start Docker Desktop")
            sys.exit(1)

        logger.info(f"✅ Docker running at {docker_cmd}")
        return True
    except Exception as e:
        print(f"❌ Docker error: {e}")
        sys.exit(1)

def check_port(port=5001):
    """Check if port is available"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('0.0.0.0', port))
        sock.close()
        logger.info(f"✅ Port {port} is available")
        return True
    except OSError:
        print(f"❌ Port {port} is already in use!")
        print(f"\n💡 Solutions:")
        print(f"   • Find process: lsof -i :{port}")
        print(f"   • Kill process: kill -9 <PID>")
        print(f"   • Or change port in code: app.run(port=5002)")
        sys.exit(1)

# Run pre-flight checks
logger.info("🔍 Running pre-flight checks...")
check_docker()
check_port()

# Configure TestContainers
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"

if sys.platform == "win32":
    os.environ["DOCKER_HOST"] = "tcp://localhost:2375"
else:
    os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

# Import dependencies
try:
    from testcontainers.postgres import PostgresContainer
    from testcontainers.redis import RedisContainer
    import psycopg
    from psycopg import IntegrityError
    import redis
    logger.info("✅ All dependencies imported successfully")
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("\n💡 Solution:")
    print("   cd scenario1-testcontainers")
    print("   python3 setup.py")
    print("   source venv/bin/activate")
    print("   pip install -r requirements.txt")
    sys.exit(1)

app = Flask(__name__)
app.secret_key = 'reality-engine-2025'
CORS(app)

# ==============================================================================
# GLOBAL STATE
# ==============================================================================

# Container instances
postgres_container = None
redis_container = None

# Feature toggles (controlled by presenter)
RATE_LIMIT_ENABLED = False
CHAOS_MODE = False

# Event stream for lifecycle visualization
lifecycle_events = []
event_lock = threading.Lock()

# Vote statistics (for leaderboard)
vote_stats = defaultdict(int)

# ==============================================================================
# LIFECYCLE EVENT SYSTEM
# ==============================================================================

def emit_event(event_type, container_name, details=None):
    """Emit lifecycle event for visualization"""
    event = {
        "timestamp": datetime.now().isoformat(),
        "type": event_type,
        "container": container_name,
        "details": details or {},
        "id": str(uuid.uuid4())[:8]
    }

    with event_lock:
        lifecycle_events.append(event)
        # Keep only last 50 events
        if len(lifecycle_events) > 50:
            lifecycle_events.pop(0)

    print(f"📡 EVENT: {event_type} | {container_name} | {details}")

# ==============================================================================
# CONTAINER MANAGEMENT
# ==============================================================================

def get_postgres_container():
    """Get or create PostgreSQL container with lifecycle events and error handling"""
    global postgres_container

    if postgres_container is None:
        try:
            emit_event("starting", "postgres", {"image": "postgres:15-alpine"})
            logger.info("Starting PostgreSQL container...")
            start_time = time.time()

            postgres_container = PostgresContainer("postgres:15-alpine")
            postgres_container.start()

            startup_time = time.time() - start_time
            logger.info(f"PostgreSQL container started in {startup_time:.1f}s")

            emit_event("ready", "postgres", {
                "startup_time": f"{startup_time:.1f}s",
                "port": postgres_container.get_exposed_port(5432)
            })

            # Initialize schema with error handling
            try:
                conn = psycopg.connect(
                    host=postgres_container.get_container_host_ip(),
                    port=postgres_container.get_exposed_port(5432),
                    user=postgres_container.username,
                    password=postgres_container.password,
                    dbname=postgres_container.dbname,
                    connect_timeout=10
                )
                cur = conn.cursor()

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS votes (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(100) UNIQUE NOT NULL,
                        choice VARCHAR(50) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                conn.commit()
                cur.close()
                conn.close()
                logger.info("PostgreSQL schema initialized")
                emit_event("initialized", "postgres", {"schema": "votes table created"})

            except Exception as e:
                logger.error(f"Failed to initialize PostgreSQL schema: {e}")
                emit_event("error", "postgres", {"error": str(e)})
                if postgres_container:
                    postgres_container.stop()
                postgres_container = None
                raise

        except Exception as e:
            logger.error(f"Failed to start PostgreSQL container: {e}")
            emit_event("error", "postgres", {"error": str(e)})
            postgres_container = None
            raise RuntimeError(
                f"Could not start PostgreSQL container: {e}\n"
                "Check Docker is running and has enough resources."
            )

    return postgres_container

def get_redis_container():
    """Get or create Redis container with lifecycle events"""
    global redis_container

    if redis_container is None:
        emit_event("starting", "redis", {"image": "redis:7-alpine"})
        start_time = time.time()

        redis_container = RedisContainer("redis:7-alpine")
        redis_container.start()

        startup_time = time.time() - start_time

        emit_event("ready", "redis", {
            "startup_time": f"{startup_time:.1f}s",
            "port": redis_container.get_exposed_port(6379)
        })

    return redis_container

def kill_redis():
    """Kill Redis container (chaos injection)"""
    global redis_container

    if redis_container:
        emit_event("chaos", "redis", {"action": "killed"})
        redis_container.stop()
        redis_container = None
        emit_event("terminated", "redis", {"reason": "chaos injection"})

def restore_redis():
    """Restore Redis container (recovery)"""
    emit_event("recovering", "redis", {"action": "restart"})
    get_redis_container()
    emit_event("recovered", "redis", {"status": "back online"})

# ==============================================================================
# RATE LIMITING
# ==============================================================================

def check_rate_limit(user_id):
    """Check if user is rate-limited (if enabled)"""
    if not RATE_LIMIT_ENABLED:
        return False, None

    if not redis_container:
        # Redis not available - graceful degradation
        return False, "Redis unavailable (graceful degradation)"

    try:
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        # Check rate limit: max 3 requests per minute
        key = f"ratelimit:{user_id}"
        count = r.incr(key)

        if count == 1:
            r.expire(key, 60)  # 1 minute window

        if count > 3:
            emit_event("rate_limited", "redis", {
                "user_id": user_id[:8],
                "count": count
            })
            return True, f"Rate limited: {count}/3 requests in 1 minute"

        return False, None

    except Exception as e:
        # Redis error - graceful degradation
        emit_event("error", "redis", {"error": str(e)})
        return False, f"Redis error (graceful fallback): {str(e)}"

# ==============================================================================
# ROUTES
# ==============================================================================

@app.route('/')
def index():
    """Main theatrical interface - THE SHOW"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())[:8]

    return render_template('theater.html')

@app.route('/old')
def old_interface():
    """Old reality engine (backup)"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())[:8]

    return render_template('reality_engine.html')

@app.route('/qr')
def qr_page():
    """QR-friendly voting page for phones"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())[:8]

    return render_template('qr_vote.html')

@app.route('/api/vote', methods=['POST'])
def vote():
    """
    Handle votes with:
    - Real database constraints (Postgres)
    - Rate limiting (Redis, if enabled)
    - Lifecycle events
    """
    data = request.json
    choice = data.get('choice')

    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())[:8]

    user_id = session['user_id']

    if not choice:
        return jsonify({
            "status": "error",
            "message": "Please select a choice"
        }), 400

    # Check rate limit (if enabled)
    is_limited, limit_msg = check_rate_limit(user_id)
    if is_limited:
        return jsonify({
            "status": "rate_limited",
            "message": "⏱️ Slow down! Too many requests.",
            "detail": limit_msg,
            "learning": "This is Redis enforcing rate limits - testable with TestContainers!"
        }), 429

    # Get PostgreSQL container
    container = get_postgres_container()

    emit_event("vote_attempt", "postgres", {
        "user_id": user_id[:8],
        "choice": choice
    })

    conn = psycopg.connect(
        host=container.get_container_host_ip(),
        port=container.get_exposed_port(5432),
        user=container.username,
        password=container.password,
        dbname=container.dbname
    )
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
            (user_id, choice)
        )
        conn.commit()

        vote_stats[choice] += 1

        emit_event("vote_success", "postgres", {
            "user_id": user_id[:8],
            "choice": choice,
            "total_votes": sum(vote_stats.values())
        })

        return jsonify({
            "status": "success",
            "message": f"✅ Vote for {choice} recorded!",
            "user_id": user_id[:8] + "...",
            "learning": "Real database constraint = one vote per user",
            "try_again": "Try voting again to see the constraint catch it!"
        })

    except IntegrityError:
        conn.rollback()

        emit_event("vote_blocked", "postgres", {
            "user_id": user_id[:8],
            "choice": choice,
            "reason": "UNIQUE constraint"
        })

        return jsonify({
            "status": "duplicate",
            "message": "🎯 You already voted!",
            "detail": "Real database UNIQUE constraint prevented duplicate",
            "magic_moment": "This is TestContainers magic!",
            "learning": "Mocks would have allowed this. Reality didn't.",
            "demo_note": "Open in incognito to vote as a different user"
        }), 400

    finally:
        cur.close()
        conn.close()

@app.route('/api/stats')
def stats():
    """Get voting statistics (leaderboard)"""
    container = get_postgres_container()

    conn = psycopg.connect(
        host=container.get_container_host_ip(),
        port=container.get_exposed_port(5432),
        user=container.username,
        password=container.password,
        dbname=container.dbname
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT choice, COUNT(*) as count
        FROM votes
        GROUP BY choice
        ORDER BY count DESC
    """)

    results = [{"choice": row[0], "count": row[1]} for row in cur.fetchall()]

    cur.execute("SELECT COUNT(*) FROM votes")
    total = cur.fetchone()[0]

    cur.close()
    conn.close()

    return jsonify({
        "results": results,
        "total_votes": total,
        "rate_limit_enabled": RATE_LIMIT_ENABLED,
        "chaos_mode": CHAOS_MODE
    })

@app.route('/api/events')
def events():
    """Server-Sent Events stream for lifecycle visualization"""
    def generate():
        last_sent = 0
        while True:
            with event_lock:
                events_to_send = lifecycle_events[last_sent:]
                last_sent = len(lifecycle_events)

            for event in events_to_send:
                yield f"data: {json.dumps(event)}\n\n"

            time.sleep(0.5)

    return Response(generate(), mimetype='text/event-stream')

# ==============================================================================
# PRESENTER CONTROLS
# ==============================================================================

@app.route('/api/control/rate-limit', methods=['POST'])
def toggle_rate_limit():
    """Toggle rate limiting (presenter control)"""
    global RATE_LIMIT_ENABLED

    RATE_LIMIT_ENABLED = not RATE_LIMIT_ENABLED

    if RATE_LIMIT_ENABLED:
        # Ensure Redis is running
        get_redis_container()
        emit_event("feature_enabled", "redis", {"feature": "rate_limiting"})
    else:
        emit_event("feature_disabled", "redis", {"feature": "rate_limiting"})

    return jsonify({
        "status": "success",
        "rate_limit_enabled": RATE_LIMIT_ENABLED,
        "message": "Rate limiting " + ("enabled" if RATE_LIMIT_ENABLED else "disabled")
    })

@app.route('/api/control/chaos', methods=['POST'])
def toggle_chaos():
    """Toggle chaos mode (kill/restore Redis)"""
    global CHAOS_MODE

    CHAOS_MODE = not CHAOS_MODE

    if CHAOS_MODE:
        kill_redis()
    else:
        restore_redis()

    return jsonify({
        "status": "success",
        "chaos_mode": CHAOS_MODE,
        "message": "Chaos mode " + ("activated" if CHAOS_MODE else "deactivated")
    })

@app.route('/api/control/reset', methods=['POST'])
def reset():
    """Reset everything (presenter control)"""
    global vote_stats, lifecycle_events

    container = get_postgres_container()

    conn = psycopg.connect(
        host=container.get_container_host_ip(),
        port=container.get_exposed_port(5432),
        user=container.username,
        password=container.password,
        dbname=container.dbname
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM votes")
    conn.commit()
    cur.close()
    conn.close()

    vote_stats.clear()

    with event_lock:
        lifecycle_events.clear()

    emit_event("reset", "system", {"action": "all data cleared"})

    return jsonify({
        "status": "success",
        "message": "🔄 Everything reset! Ready for next demo."
    })

@app.route('/api/containers')
def containers():
    """Get current container status"""
    return jsonify({
        "postgres": {
            "running": postgres_container is not None,
            "port": postgres_container.get_exposed_port(5432) if postgres_container else None
        },
        "redis": {
            "running": redis_container is not None,
            "port": redis_container.get_exposed_port(6379) if redis_container else None
        }
    })

@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "reality_engine": "online",
        "containers": {
            "postgres": postgres_container is not None,
            "redis": redis_container is not None
        },
        "features": {
            "rate_limit": RATE_LIMIT_ENABLED,
            "chaos": CHAOS_MODE
        }
    })

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == '__main__':
    print("\n" + "🔥" * 30)
    print("\n" + " " * 20 + "THE REALITY ENGINE")
    print(" " * 15 + '"If your tests don\'t face reality,')
    print(" " * 18 + 'your users will."')
    print("\n" + "🔥" * 30)

    print("\n📋 Features:")
    print("   ✅ Live voting with QR code support")
    print("   ✅ Real-time lifecycle event stream")
    print("   ✅ Redis rate limiting (toggle on/off)")
    print("   ✅ Chaos injection (kill/restore containers)")
    print("   ✅ Presenter control dashboard")

    print("\n🎯 Endpoints:")
    print("   📊 Main:      http://localhost:5001")
    print("   📱 QR Page:   http://localhost:5001/qr")
    print("   📡 Events:    http://localhost:5001/api/events")

    print("\n🚀 Pre-starting PostgreSQL container...")
    get_postgres_container()

    print("\n✅ Reality Engine online!")
    print("🎬 Ready for your 8-minute show!")
    print("\n" + "🔥" * 30 + "\n")

    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
