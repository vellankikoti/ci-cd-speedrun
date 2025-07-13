#!/usr/bin/env python3
import json
import time
import os
import psutil
import redis
import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__)

# Try to connect to Redis
try:
    redis_client = redis.Redis(host='redis', port=6379, db=0, socket_connect_timeout=2)
    redis_client.ping()
    redis_available = True
except:
    redis_available = False

# Try to connect to MySQL
try:
    mysql_connection = pymysql.connect(
        host='mysql',
        port=3306,
        user='root',
        password='password',
        database='test',
        connect_timeout=2
    )
    mysql_available = True
except:
    mysql_available = False

@app.route('/health')
def health():
    # Comprehensive health checks
    health_checks = {
        "database_connectivity": mysql_available,
        "network_connectivity": test_network_connectivity(),
        "overall_health": True,
        "redis_connectivity": redis_available,
        "resource_management": test_resource_management()
    }
    
    # Determine overall health
    overall_health = all(health_checks.values())
    
    return jsonify({
        "status": "healthy" if overall_health else "unhealthy",
        "step": "step5_success",
        "message": "Production-ready system",
        "checks": health_checks,
        "overall_health": overall_health
    })

@app.route('/debug')
def debug():
    return jsonify({
        "step": "step5_success",
        "description": "Production-Ready System",
        "system_info": {
            "hostname": os.uname().nodename,
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(),
            "memory_total": round(psutil.virtual_memory().total / (1024 * 1024), 2),
            "memory_used": round(psutil.virtual_memory().used / (1024 * 1024), 2),
            "memory_percent": psutil.virtual_memory().percent
        },
        "service_status": {
            "redis_available": redis_available,
            "mysql_available": mysql_available,
            "network_connectivity": test_network_connectivity()
        },
        "educational_content": {
            "learning_objective": "Understanding production-ready, resilient systems",
            "success_patterns": "All services working together in harmony",
            "real_world_impact": "Comprehensive monitoring and observability",
            "best_practices": [
                "Health monitoring and checks",
                "Service dependency management",
                "Resource monitoring and limits",
                "Error handling and fallback mechanisms",
                "Metrics and observability"
            ]
        }
    })

@app.route('/metrics')
def metrics():
    """Get comprehensive system metrics"""
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return jsonify({
        "timestamp": time.time(),
        "system_metrics": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_total_mb": round(memory.total / (1024 * 1024), 2),
            "memory_used_mb": round(memory.used / (1024 * 1024), 2),
            "memory_percent": memory.percent,
            "disk_total_gb": round(disk.total / (1024 * 1024 * 1024), 2),
            "disk_used_gb": round(disk.used / (1024 * 1024 * 1024), 2),
            "disk_percent": disk.percent
        },
        "service_metrics": {
            "redis_available": redis_available,
            "mysql_available": mysql_available,
            "network_connectivity": test_network_connectivity()
        },
        "application_metrics": {
            "uptime_seconds": time.time() - app.start_time if hasattr(app, 'start_time') else 0,
            "total_requests": getattr(app, 'request_count', 0)
        }
    })

@app.route('/run-experiment')
def run_experiment():
    """Run comprehensive system experiment"""
    results = {
        "experiment": "Production System Test",
        "timestamp": time.time(),
        "tests": {
            "redis_test": test_redis_functionality(),
            "mysql_test": test_mysql_functionality(),
            "network_test": test_network_connectivity(),
            "resource_test": test_resource_management()
        },
        "summary": "All systems working together successfully",
        "educational_value": "Demonstrates a production-ready, resilient system"
    }
    
    return jsonify(results)

@app.route('/session/create', methods=['POST'])
def create_session():
    """Create a new session (Redis)"""
    try:
        session_id = f"session_{int(time.time())}"
        session_data = {
            "id": session_id,
            "created_at": time.time(),
            "user_agent": request.headers.get('User-Agent', 'Unknown'),
            "data": request.json if request.is_json else {}
        }
        
        if redis_available:
            redis_client.setex(f"session:{session_id}", 3600, json.dumps(session_data))
            storage_method = "Redis"
        else:
            if not hasattr(app, 'sessions'):
                app.sessions = {}
            app.sessions[session_id] = session_data
            storage_method = "In-memory (fallback)"
        
        return jsonify({
            "status": "success",
            "session_id": session_id,
            "storage_method": storage_method,
            "message": "Session created successfully"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Failed to create session"
        }), 500

@app.route('/user/create', methods=['POST'])
def create_user():
    """Create a new user (MySQL)"""
    try:
        user_data = request.json if request.is_json else {}
        user_id = f"user_{int(time.time())}"
        
        user_info = {
            "id": user_id,
            "name": user_data.get('name', 'Anonymous'),
            "email": user_data.get('email', f'{user_id}@example.com'),
            "created_at": time.time(),
            "status": "active"
        }
        
        if mysql_available:
            with mysql_connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id VARCHAR(50) PRIMARY KEY,
                        name VARCHAR(100),
                        email VARCHAR(100),
                        created_at TIMESTAMP,
                        status VARCHAR(20)
                    )
                """)
                
                cursor.execute("""
                    INSERT INTO users (id, name, email, created_at, status)
                    VALUES (%s, %s, %s, FROM_UNIXTIME(%s), %s)
                """, (user_info['id'], user_info['name'], user_info['email'], 
                     user_info['created_at'], user_info['status']))
                
                mysql_connection.commit()
            storage_method = "MySQL"
        else:
            if not hasattr(app, 'users'):
                app.users = {}
            app.users[user_id] = user_info
            storage_method = "In-memory (fallback)"
        
        return jsonify({
            "status": "success",
            "user": user_info,
            "storage_method": storage_method,
            "message": "User created successfully"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Failed to create user"
        }), 500

@app.route('/')
def index():
    return jsonify({
        "message": "Step 5: Success - Production Ready",
        "description": "Complete resilient microservices architecture",
        "services": {
            "redis_available": redis_available,
            "mysql_available": mysql_available
        },
        "endpoints": {
            "health": "/health",
            "debug": "/debug",
            "metrics": "/metrics",
            "experiment": "/run-experiment",
            "create_session": "/session/create (POST)",
            "create_user": "/user/create (POST)"
        }
    })

def test_network_connectivity():
    """Test network connectivity"""
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

def test_resource_management():
    """Test resource management"""
    try:
        memory = psutil.virtual_memory()
        return memory.percent < 90  # Consider healthy if memory usage < 90%
    except:
        return False

def test_redis_functionality():
    """Test Redis functionality"""
    try:
        if redis_available:
            test_key = f"test_{int(time.time())}"
            redis_client.set(test_key, "test_value", ex=60)
            value = redis_client.get(test_key)
            return value == b"test_value"
        return False
    except:
        return False

def test_mysql_functionality():
    """Test MySQL functionality"""
    try:
        if mysql_available:
            with mysql_connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result[0] == 1
        return False
    except:
        return False

# Initialize app start time
app.start_time = time.time()
app.request_count = 0

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
