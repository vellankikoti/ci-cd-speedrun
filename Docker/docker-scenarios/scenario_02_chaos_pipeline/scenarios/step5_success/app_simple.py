#!/usr/bin/env python3
import json
import time
import os
import psutil
from flask import Flask, jsonify, request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        health_checks = {
            "database_connectivity": True,  # Simulated success
            "network_connectivity": test_network_connectivity(),
            "overall_health": True,
            "redis_connectivity": True,  # Simulated success
            "resource_management": test_resource_management()
        }
        
        overall_health = all(health_checks.values())
        
        logger.info(f"Health check - Overall: {overall_health}, Checks: {health_checks}")
        
        return jsonify({
            "status": "healthy" if overall_health else "unhealthy",
            "step": "step5_success",
            "message": "Production-ready system (simulated)",
            "checks": health_checks,
            "overall_health": overall_health
        })
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return jsonify({
            "status": "error",
            "step": "step5_success",
            "message": f"Health check failed: {str(e)}",
            "checks": {
                "database_connectivity": False,
                "network_connectivity": False,
                "overall_health": False,
                "redis_connectivity": False,
                "resource_management": False
            },
            "overall_health": False
        }), 500

@app.route('/debug')
def debug():
    """Debug information endpoint"""
    try:
        return jsonify({
            "step": "step5_success",
            "description": "Production-Ready System (Simulated)",
            "system_info": {
                "hostname": os.uname().nodename,
                "cpu_count": psutil.cpu_count(),
                "cpu_percent": psutil.cpu_percent(),
                "memory_total": round(psutil.virtual_memory().total / (1024 * 1024), 2),
                "memory_used": round(psutil.virtual_memory().used / (1024 * 1024), 2),
                "memory_percent": psutil.virtual_memory().percent
            },
            "service_status": {
                "redis_available": True,  # Simulated
                "mysql_available": True,  # Simulated
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
    except Exception as e:
        logger.error(f"Debug endpoint error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/metrics')
def metrics():
    """Get comprehensive system metrics"""
    try:
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
                "redis_available": True,  # Simulated
                "mysql_available": True,  # Simulated
                "network_connectivity": test_network_connectivity()
            },
            "application_metrics": {
                "uptime_seconds": time.time() - app.start_time if hasattr(app, 'start_time') else 0,
                "total_requests": getattr(app, 'request_count', 0)
            }
        })
    except Exception as e:
        logger.error(f"Metrics endpoint error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/run-experiment')
def run_experiment():
    """Run comprehensive system experiment"""
    try:
        results = {
            "experiment": "Production System Test (Simulated)",
            "timestamp": time.time(),
            "tests": {
                "redis_test": True,  # Simulated success
                "mysql_test": True,  # Simulated success
                "network_test": test_network_connectivity(),
                "resource_test": test_resource_management()
            },
            "summary": "All systems working together successfully (simulated)",
            "educational_value": "Demonstrates a production-ready, resilient system"
        }
        
        return jsonify(results)
    except Exception as e:
        logger.error(f"Experiment endpoint error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/session/create', methods=['POST'])
def create_session():
    """Create a new session (simulated)"""
    try:
        session_id = f"session_{int(time.time())}"
        session_data = {
            "id": session_id,
            "created_at": time.time(),
            "user_agent": request.headers.get('User-Agent', 'Unknown'),
            "data": request.json if request.is_json else {}
        }
        
        # Simulate session storage
        if not hasattr(app, 'sessions'):
            app.sessions = {}
        app.sessions[session_id] = session_data
        
        return jsonify({
            "status": "success",
            "session_id": session_id,
            "storage_method": "In-memory (simulated)",
            "message": "Session created successfully"
        })
    except Exception as e:
        logger.error(f"Session creation error: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Failed to create session"
        }), 500

@app.route('/user/create', methods=['POST'])
def create_user():
    """Create a new user (simulated)"""
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
        
        # Simulate user storage
        if not hasattr(app, 'users'):
            app.users = {}
        app.users[user_id] = user_info
        
        return jsonify({
            "status": "success",
            "user": user_info,
            "storage_method": "In-memory (simulated)",
            "message": "User created successfully"
        })
    except Exception as e:
        logger.error(f"User creation error: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Failed to create user"
        }), 500

@app.route('/')
def index():
    """Root endpoint"""
    try:
        return jsonify({
            "message": "Step 5: Success - Production Ready (Simulated)",
            "description": "Complete resilient microservices architecture (simulated)",
            "services": {
                "redis_available": True,  # Simulated
                "mysql_available": True   # Simulated
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
    except Exception as e:
        logger.error(f"Index endpoint error: {str(e)}")
        return jsonify({"error": str(e)}), 500

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

# Initialize app start time
app.start_time = time.time()
app.request_count = 0

if __name__ == "__main__":
    logger.info("Starting Flask application...")
    logger.info("Flask app will be available on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
