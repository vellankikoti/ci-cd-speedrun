#!/usr/bin/env python3
import psutil
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        "status": "unhealthy",
        "step": "step2_fail_resource",
        "message": "Resource exhaustion"
    })

@app.route('/')
def index():
    return jsonify({"message": "Step 2: Resource Failure"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
