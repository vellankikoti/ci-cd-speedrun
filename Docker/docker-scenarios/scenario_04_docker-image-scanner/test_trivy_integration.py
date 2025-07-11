#!/usr/bin/env python3
"""
Test script for Trivy-based Docker Analyzer
Tests the new educational analyzer with real Trivy integration
"""

import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.trivy_analyzer import TrivyEducationalAnalyzer

async def test_trivy_analyzer():
    """Test the Trivy-based educational analyzer"""
    
    print("🐳 Testing Trivy Educational Analyzer")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = TrivyEducationalAnalyzer()
    
    print(f"✅ Trivy available: {analyzer.trivy_available}")
    
    if not analyzer.trivy_available:
        print("❌ Trivy not available. Please install Trivy first.")
        print("   Install with: curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh")
        return
    
    # Test images to analyze
    test_images = [
        "nginx:alpine",
        "python:3.9-slim",
        "node:16-alpine"
    ]
    
    for image_name in test_images:
        print(f"\n🔍 Analyzing {image_name}...")
        
        try:
            # Perform educational analysis
            result = await analyzer.analyze_image_educational(image_name)
            
            print(f"✅ Analysis completed for {result.image_name}")
            print(f"📊 Total vulnerabilities: {result.total_vulnerabilities}")
            print(f"🛡️ Security score: {result.security_score:.1f}")
            print(f"🎓 Learning insights: {len(result.learning_insights)}")
            print(f"📚 Best practices: {len(result.best_practices)}")
            
            # Show some insights
            if result.learning_insights:
                print("\n💡 Learning Insights:")
                for insight in result.learning_insights[:3]:  # Show first 3
                    print(f"   • {insight}")
            
            # Show some best practices
            if result.best_practices:
                print("\n📚 Best Practices:")
                for practice in result.best_practices[:2]:  # Show first 2
                    print(f"   • {practice.title} ({practice.priority})")
            
            # Show vulnerability breakdown
            print(f"\n🔍 Vulnerability Breakdown:")
            print(f"   • Critical: {len(result.critical_vulnerabilities)}")
            print(f"   • High: {len(result.high_vulnerabilities)}")
            print(f"   • Medium: {len(result.medium_vulnerabilities)}")
            print(f"   • Low: {len(result.low_vulnerabilities)}")
            
        except Exception as e:
            print(f"❌ Error analyzing {image_name}: {str(e)}")
    
    print("\n🎉 Test completed!")

async def test_dockerfile_analysis():
    """Test Dockerfile analysis functionality"""
    
    print("\n📄 Testing Dockerfile Analysis")
    print("=" * 50)
    
    # Create a test Dockerfile
    test_dockerfile = """
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Switch to non-root user
USER appuser

# Run the application
CMD ["python", "app.py"]
"""
    
    # Save test Dockerfile
    with open("test_dockerfile", "w") as f:
        f.write(test_dockerfile)
    
    print("✅ Created test Dockerfile")
    
    # Test Dockerfile parsing (this would be part of the app)
    from app import _analyze_dockerfile_content
    
    try:
        insights = await _analyze_dockerfile_content("test_dockerfile")
        print(f"✅ Dockerfile analysis completed")
        print(f"📊 Statistics: {insights.get('statistics', {})}")
        
        if 'insights' in insights:
            print("\n💡 Dockerfile Insights:")
            for insight in insights['insights']:
                print(f"   • {insight}")
        
        if 'recommendations' in insights:
            print("\n📝 Recommendations:")
            for rec in insights['recommendations']:
                print(f"   • {rec}")
                
    except Exception as e:
        print(f"❌ Error analyzing Dockerfile: {str(e)}")
    
    # Clean up
    if os.path.exists("test_dockerfile"):
        os.remove("test_dockerfile")

async def test_api_endpoints():
    """Test the API endpoints"""
    
    print("\n🌐 Testing API Endpoints")
    print("=" * 50)
    
    import requests
    import json
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/test")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data.get('status', 'unknown')}")
            print(f"🔧 Trivy available: {data.get('trivy_available', False)}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
    
    # Test image analysis endpoint
    try:
        payload = {
            "image_name": "nginx:alpine",
            "analysis_type": "comprehensive"
        }
        
        response = requests.post(
            f"{base_url}/api/v1/analyze/image",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Image analysis completed")
            print(f"📊 Security score: {data.get('enterprise_score', 'N/A')}")
            print(f"🔍 Vulnerabilities: {data.get('security_analysis', {}).get('total_vulnerabilities', 0)}")
        else:
            print(f"❌ Image analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Image analysis error: {str(e)}")

def main():
    """Main test function"""
    
    print("🚀 Starting Trivy Educational Analyzer Tests")
    print("=" * 60)
    
    # Run tests
    asyncio.run(test_trivy_analyzer())
    asyncio.run(test_dockerfile_analysis())
    
    # Note: API tests require the server to be running
    print("\n💡 To test API endpoints, start the server first:")
    print("   cd enterprise-docker-analyzer")
    print("   python app.py")
    print("   Then run: python test_trivy_integration.py --api")

if __name__ == "__main__":
    if "--api" in sys.argv:
        asyncio.run(test_api_endpoints())
    else:
        main() 