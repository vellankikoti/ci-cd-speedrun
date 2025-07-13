#!/usr/bin/env python3
import requests
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        "status": "unhealthy",
        "step": "step1_fail_network",
        "message": "Network connectivity issues"
    })

@app.route('/')
def index():
    return jsonify({"message": "Step 1: Network Failure"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
