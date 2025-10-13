#!/usr/bin/env python3
"""
Scenario 1: TestContainers Magic
Real database testing that catches bugs mocks miss

This scenario demonstrates the power of TestContainers by showing:
1. How mocks can lie and miss real bugs
2. How TestContainers provides real database testing
3. The "magic moment" when a real constraint catches a bug
"""

import os
import sys
import time
import json
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

# Configure TestContainers to use local Docker
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"

# Platform-specific Docker host configuration
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
    """Main voting page"""
    return render_template('voting.html')

@app.route('/api/vote', methods=['POST'])
def vote():
    """Submit a vote - this is where the magic happens!"""
    data = request.json
    choice = data.get('choice')
    user_id = request.remote_addr  # Use IP as user ID for demo
    
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
        # This will fail if user already voted (UNIQUE constraint)
        cur.execute(
            "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
            (user_id, choice)
        )
        conn.commit()
        
        return jsonify({
            "status": "success",
            "message": f"Vote for {choice} recorded!",
            "database": "real PostgreSQL (TestContainers)",
            "magic_moment": "🎯 Real database constraint caught duplicate vote!",
            "learning": "This is why TestContainers beats mocks!"
        })
        
    except IntegrityError as e:
        conn.rollback()
        return jsonify({
            "status": "error",
            "message": "You already voted!",
            "detail": "Real database caught duplicate vote (UNIQUE constraint)",
            "technical": str(e),
            "magic_moment": "🎯 This is the magic moment!",
            "learning": "TestContainers caught a bug that mocks would miss!",
            "database": "real PostgreSQL (TestContainers)"
        }), 400
        
    except Exception as e:
        conn.rollback()
        return jsonify({
            "status": "error",
            "message": f"Database error: {str(e)}",
            "learning": "Real database testing catches real issues!"
        }), 500
        
    finally:
        cur.close()
        conn.close()

@app.route('/api/results')
def results():
    """Get voting results"""
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
        "database": "real PostgreSQL (TestContainers)"
    })

@app.route('/api/metrics')
def metrics():
    """Show TestContainers metrics and benefits"""
    container = get_postgres_container()
    
    return jsonify({
        "container": {
            "image": "postgres:15-alpine",
            "status": "running",
            "size": "77 MB",
            "startup_time": f"{container_start_time:.1f} seconds" if container_start_time else "N/A",
            "connection_url": container.get_connection_url()
        },
        "database": {
            "version": "PostgreSQL 15.4",
            "features": ["ACID", "JSONB", "Window Functions", "Constraints"]
        },
        "testcontainers_benefits": [
            "✅ Real database, not mocks",
            "✅ Catches SQL constraint violations",
            "✅ Tests run in isolation",
            "✅ Automatic cleanup",
            "✅ Same behavior as production",
            "✅ Easy version testing"
        ],
        "bugs_caught": 1,
        "production_outages_prevented": 1,
        "magic_moment": "Real database constraints caught duplicate vote!"
    })

@app.route('/api/demo/with-mock')
def demo_with_mock():
    """Demonstrate problem with mocks"""
    return jsonify({
        "approach": "Mock Database",
        "problem": "Mock passes, but production has bug!",
        "code": """
def test_vote_with_mock():
    mock_db = MockDatabase()
    result = submit_vote(mock_db, "user1", "Python")
    assert result == True  # Test passes!
    
    # But in production:
    # - Duplicate votes aren't prevented
    # - SQL constraints aren't tested
    # - Production breaks! 💥
        """,
        "result": "❌ Test passes but production breaks",
        "lesson": "Mocks can lie. TestContainers tells truth.",
        "why_bad": [
            "Mock doesn't enforce UNIQUE constraints",
            "Mock doesn't test real SQL behavior",
            "Mock doesn't catch data integrity issues",
            "Mock gives false confidence"
        ]
    })

@app.route('/api/demo/with-testcontainers')
def demo_with_testcontainers():
    """Demonstrate TestContainers approach"""
    return jsonify({
        "approach": "TestContainers",
        "benefit": "Real database catches real bugs!",
        "code": """
def test_vote_with_testcontainers():
    with PostgresContainer("postgres:15-alpine") as postgres:
        conn = psycopg.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            dbname=postgres.dbname
        )
        
        # First vote succeeds
        submit_vote(conn, "user1", "Python")
        
        # Second vote fails (UNIQUE constraint)
        with pytest.raises(IntegrityError):
            submit_vote(conn, "user1", "Python")
        
        # Test catches the bug! ✅
        """,
        "result": "✅ Test catches bug before production",
        "lesson": "TestContainers = Production parity",
        "why_good": [
            "Real PostgreSQL with real constraints",
            "Tests actual SQL behavior",
            "Catches data integrity issues",
            "Gives real confidence"
        ]
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

@app.route('/api/reset', methods=['POST'])
def reset_votes():
    """Reset all votes (for demo purposes)"""
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
        "message": "All votes reset!",
        "learning": "TestContainers makes it easy to reset test data"
    })

if __name__ == '__main__':
    print("🧪 Scenario 1: TestContainers Magic")
    print("=" * 50)
    print("⚡ CI/CD Speed Run - PyCon ES 2025")
    print("")
    print("🎯 Learning: Real database testing vs mocks")
    print("🔧 Technology: Python + PostgreSQL + TestContainers")
    print("⏱️  Time: 10 minutes")
    print("")
    
    # Pre-start container for faster first request
    print("🚀 Pre-starting PostgreSQL container...")
    get_postgres_container()
    
    print("✅ Ready!")
    print("📊 App: http://localhost:5001")
    print("🎮 Try voting twice to see the magic!")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5001, debug=True)
