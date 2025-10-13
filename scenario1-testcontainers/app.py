#!/usr/bin/env python3
"""
Scenario 1: TestContainers Magic - Interactive Learning Experience
===================================================================

A clean, intuitive demo that guides users through:
1. The Problem: How mocks can lie
2. The Magic: TestContainers catches bugs
3. The Solution: Real database testing
"""

import os
import sys
import time
import uuid
from datetime import datetime
from flask import Flask, render_template, jsonify, request, session
from flask_cors import CORS

# Configure TestContainers
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"

if sys.platform == "win32":
    os.environ["DOCKER_HOST"] = "tcp://localhost:2375"
else:
    os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

try:
    from testcontainers.postgres import PostgresContainer
    import psycopg
    from psycopg import IntegrityError
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg[binary]")
    sys.exit(1)

app = Flask(__name__)
app.secret_key = 'testcontainers-magic-demo-2025'
CORS(app)

# Global container instance
postgres_container = None
container_start_time = None

def get_postgres_container():
    """Get or create PostgreSQL container"""
    global postgres_container, container_start_time

    if postgres_container is None:
        print("🚀 Starting PostgreSQL container...")
        start_time = time.time()

        postgres_container = PostgresContainer("postgres:15-alpine")
        postgres_container.start()

        container_start_time = time.time() - start_time

        # Initialize database schema
        conn = psycopg.connect(
            host=postgres_container.get_container_host_ip(),
            port=postgres_container.get_exposed_port(5432),
            user=postgres_container.username,
            password=postgres_container.password,
            dbname=postgres_container.dbname
        )
        cur = conn.cursor()

        # Create votes table with UNIQUE constraint
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

        print(f"✅ PostgreSQL ready! (startup: {container_start_time:.1f}s)")

    return postgres_container

@app.route('/')
def index():
    """Main interactive demo page"""
    # Generate session ID if not exists
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())[:8]

    return render_template('demo_interactive.html')

@app.route('/api/scenario/<scenario_name>', methods=['POST'])
def run_scenario(scenario_name):
    """Run a specific scenario"""

    if scenario_name == 'mock':
        return run_mock_scenario()
    elif scenario_name == 'testcontainers':
        return run_testcontainers_scenario()
    else:
        return jsonify({"status": "error", "message": "Unknown scenario"}), 400

def run_mock_scenario():
    """Scenario 1: Show how mocks fail"""
    # Simulate mock database (no constraints)
    mock_votes = []

    # First vote - succeeds
    mock_votes.append({"user": "user1", "choice": "Python"})

    # Second vote (duplicate) - also succeeds! (BUG!)
    mock_votes.append({"user": "user1", "choice": "Python"})

    # Third vote (duplicate) - also succeeds! (BUG!)
    mock_votes.append({"user": "user1", "choice": "Python"})

    return jsonify({
        "status": "success",
        "scenario": "mock",
        "title": "❌ Mock Database (The Problem)",
        "steps": [
            {
                "step": 1,
                "action": "User votes for Python",
                "result": "✅ Vote recorded",
                "votes_count": 1,
                "status": "success"
            },
            {
                "step": 2,
                "action": "Same user votes again for Python",
                "result": "✅ Vote recorded (BUG!)",
                "votes_count": 2,
                "status": "bug",
                "explanation": "Mock allows duplicate! No constraint enforcement."
            },
            {
                "step": 3,
                "action": "Same user votes AGAIN for Python",
                "result": "✅ Vote recorded (BUG!)",
                "votes_count": 3,
                "status": "bug",
                "explanation": "Mock allows unlimited duplicates!"
            }
        ],
        "total_votes": len(mock_votes),
        "problem": "Mock database allows unlimited votes from same user!",
        "impact": "🚨 In production: Users can vote multiple times, breaking the business logic",
        "lesson": "Mocks can lie - they don't test real database behavior"
    })

def run_testcontainers_scenario():
    """Scenario 2: Show how TestContainers catches bugs"""
    container = get_postgres_container()

    # Use a test user ID for this scenario
    test_user_id = "demo_user_" + str(int(time.time()))

    conn = psycopg.connect(
        host=container.get_container_host_ip(),
        port=container.get_exposed_port(5432),
        user=container.username,
        password=container.password,
        dbname=container.dbname
    )

    steps = []

    # Step 1: First vote - should succeed
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
            (test_user_id, "Python")
        )
        conn.commit()
        cur.close()

        steps.append({
            "step": 1,
            "action": "User votes for Python",
            "result": "✅ Vote recorded",
            "votes_count": 1,
            "status": "success"
        })
    except Exception as e:
        steps.append({
            "step": 1,
            "action": "User votes for Python",
            "result": f"❌ Error: {str(e)}",
            "status": "error"
        })

    # Step 2: Second vote (duplicate) - should FAIL
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
            (test_user_id, "Python")
        )
        conn.commit()
        cur.close()

        steps.append({
            "step": 2,
            "action": "Same user tries to vote again",
            "result": "✅ Vote recorded (This shouldn't happen!)",
            "status": "unexpected"
        })
    except IntegrityError as e:
        conn.rollback()
        steps.append({
            "step": 2,
            "action": "Same user tries to vote again",
            "result": "❌ BLOCKED by database constraint!",
            "votes_count": 1,
            "status": "caught",
            "explanation": "🎯 MAGIC MOMENT! Real database caught the duplicate vote!",
            "constraint": "UNIQUE constraint on user_id"
        })

    # Step 3: Try one more time
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
            (test_user_id, "Python")
        )
        conn.commit()
        cur.close()

        steps.append({
            "step": 3,
            "action": "Same user tries AGAIN",
            "result": "✅ Vote recorded (This shouldn't happen!)",
            "status": "unexpected"
        })
    except IntegrityError:
        conn.rollback()
        steps.append({
            "step": 3,
            "action": "Same user tries AGAIN",
            "result": "❌ BLOCKED again!",
            "votes_count": 1,
            "status": "caught",
            "explanation": "Real constraints prevent ALL duplicates!"
        })

    # Get actual vote count
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM votes WHERE user_id = %s", (test_user_id,))
    actual_votes = cur.fetchone()[0]
    cur.close()
    conn.close()

    return jsonify({
        "status": "success",
        "scenario": "testcontainers",
        "title": "✅ TestContainers (The Solution)",
        "steps": steps,
        "total_votes": actual_votes,
        "solution": "TestContainers uses REAL PostgreSQL with REAL constraints!",
        "impact": "✅ In production: Only one vote per user, business logic protected",
        "lesson": "TestContainers catches bugs that mocks would miss",
        "magic": "🎯 The UNIQUE constraint prevented duplicate votes!"
    })

@app.route('/api/vote', methods=['POST'])
def vote():
    """Interactive voting for hands-on testing"""
    data = request.json
    choice = data.get('choice')

    # Generate unique user ID for each vote attempt (for demo purposes)
    # In real app, this would be actual user authentication
    user_id = session.get('user_id', str(uuid.uuid4())[:8])

    if not choice:
        return jsonify({
            "status": "error",
            "message": "Please select a choice"
        }), 400

    container = get_postgres_container()
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

        return jsonify({
            "status": "success",
            "message": f"✅ Vote for {choice} recorded!",
            "user_id": user_id,
            "note": "Try voting again to see the constraint in action!"
        })

    except IntegrityError:
        conn.rollback()
        return jsonify({
            "status": "error",
            "message": "🎯 You already voted!",
            "detail": "Real database UNIQUE constraint prevented duplicate",
            "magic_moment": "This is TestContainers magic!",
            "user_id": user_id
        }), 400

    finally:
        cur.close()
        conn.close()

@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset votes and generate new session"""
    # Generate new session ID
    session['user_id'] = str(uuid.uuid4())[:8]

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

    return jsonify({
        "status": "success",
        "message": "All votes cleared! You can vote again.",
        "new_user_id": session['user_id']
    })

@app.route('/api/results')
def results():
    """Get current voting results"""
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
        "total_votes": total
    })

@app.route('/api/health')
def health():
    """Health check"""
    try:
        container = get_postgres_container()
        conn = psycopg.connect(
            host=container.get_container_host_ip(),
            port=container.get_exposed_port(5432),
            user=container.username,
            password=container.password,
            dbname=container.dbname
        )
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        conn.close()

        return jsonify({
            "status": "healthy",
            "scenario": 1,
            "database": "connected",
            "testcontainers": "working"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("🧪 Scenario 1: TestContainers Magic - Interactive Demo")
    print("=" * 60)
    print("⚡ CI/CD Speed Run - PyCon ES 2025")
    print("")
    print("🎯 Learning: Real database testing vs mocks")
    print("🎮 Interactive: Guided scenarios with visual feedback")
    print("⏱️  Time: 10 minutes")
    print("")

    # Pre-start container
    print("🚀 Pre-starting PostgreSQL container...")
    get_postgres_container()

    print("✅ Ready!")
    print("📊 App: http://localhost:5001")
    print("🎮 Follow the guided scenarios to see the magic!")
    print("=" * 60)

    app.run(host='0.0.0.0', port=5001, debug=True)
