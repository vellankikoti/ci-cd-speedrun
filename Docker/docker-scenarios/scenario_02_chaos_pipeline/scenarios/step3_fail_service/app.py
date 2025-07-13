#!/usr/bin/env python3
import redis
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        "status": "unhealthy",
        "step": "step3_fail_service",
        "message": "Service dependency failure"
    })

@app.route('/')
def index():
    return jsonify({"message": "Step 3: Service Failure"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
