# 🚀 Docker Chaos Pipeline

**Progressive chaos engineering with 5 failure scenarios**

Demonstrate Docker capabilities through real failure scenarios and resilience testing.

## 🚀 Quick Start

```bash
cd Docker/docker-scenarios/scenario_02_chaos_pipeline

# Run automated demo
./demo_simple.sh

# Clean up when done
./cleanup.sh
```

## 📋 What You'll Learn

- **Step 1: Network Failure** - Container can't reach external services
- **Step 2: Resource Failure** - Container runs out of memory/CPU
- **Step 3: Service Failure** - Application crashes and restarts
- **Step 4: Database Failure** - Database connection issues
- **Step 5: Success Scenario** - Everything working perfectly

## 🎯 Demo Scripts

- **`demo_simple.sh`** - Automated demo (recommended)
- **`cleanup.sh`** - Clean up all containers and images

## 🔧 Prerequisites

- Docker installed and running
- ~1GB RAM available
- Ports 8001-8005 available

## 📊 Expected Results

Each step demonstrates:
- **Real failure scenarios** with actual error messages
- **Container behavior** under different stress conditions
- **Resilience patterns** and recovery mechanisms
- **Monitoring and debugging** techniques

## 🧪 Testing

```bash
# Test individual steps
curl http://localhost:8001  # Network failure
curl http://localhost:8002  # Resource failure
curl http://localhost:8003  # Service failure
curl http://localhost:8004  # Database failure
curl http://localhost:8005  # Success
```

## 🎯 Key Concepts

- **Container isolation** and resource limits
- **Network connectivity** and service discovery
- **Health checks** and monitoring
- **Graceful degradation** and error handling
- **Chaos engineering** principles

**Perfect for:** Understanding Docker failures, resilience testing, chaos engineering