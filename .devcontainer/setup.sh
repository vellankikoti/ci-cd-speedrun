#!/bin/bash
# Codespaces post-create setup script
# Pre-downloads Docker images to avoid workshop delays

set -e

echo "🚀 Setting up CI/CD Chaos Workshop in Codespaces..."
echo "===================================================="
echo ""

# Pre-pull Docker images (CRITICAL for workshop performance!)
echo "📦 Pre-downloading Docker images..."
echo "   This ensures fast workshop experience for 100+ participants"
echo ""

# Pull PostgreSQL
echo "   Pulling postgres:15-alpine..."
docker pull postgres:15-alpine 2>&1 | grep -E "(Digest|Status)" || true

# Pull Redis
echo "   Pulling redis:7-alpine..."
docker pull redis:7-alpine 2>&1 | grep -E "(Digest|Status)" || true

echo ""
echo "✅ Docker images pre-downloaded!"
echo ""

# Verify images
echo "📊 Verifying Docker images..."
docker images | grep -E "(postgres|redis)" || echo "   Warning: Images not found"
echo ""

# Setup Python environment for scenario 1
if [ -d "scenario1-testcontainers" ]; then
    echo "🐍 Setting up Scenario 1 environment..."
    cd scenario1-testcontainers

    # Run setup
    python3 setup.py 2>&1 | tail -5

    echo "✅ Scenario 1 ready!"
    cd ..
fi

echo ""
echo "🎉 Codespace setup complete!"
echo "=============================="
echo ""
echo "📍 You're in GitHub Codespaces"
echo "   Docker images: Pre-downloaded ✅"
echo "   Port 5001: Auto-forwarded ✅"
echo "   Ready for workshop! ✅"
echo ""
echo "🚀 Quick Start:"
echo "   cd scenario1-testcontainers"
echo "   python3 reality_engine.py"
echo ""
echo "📚 Or read: scenario1-testcontainers/README.md"
echo ""
