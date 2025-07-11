# 🐳 Enterprise Docker Image Analyzer

A comprehensive, enterprise-grade Docker image analysis platform with real-time insights, security scanning, and industry benchmarking.

## 🎯 Features

### 🔍 **Comprehensive Analysis**
- **Layer-by-layer analysis** using real Docker API
- **Security vulnerability scanning** with Trivy integration
- **Performance benchmarking** with real metrics
- **Industry comparison** against Docker Hub standards

### 🛡️ **Security First**
- Real vulnerability scanning using Trivy
- Root user detection and recommendations
- Sensitive data exposure detection
- Security score calculation

### ⚡ **Performance Optimized**
- Build time analysis
- Startup time measurement
- Memory and CPU usage tracking
- Resource efficiency scoring

### 📊 **Industry Benchmarked**
- Comparison against industry standards
- Best practices recommendations
- Popular image suggestions
- Percentile ranking

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker Engine
- Docker API access

### Installation

1. **Clone and navigate to the project:**
```bash
cd enterprise-docker-analyzer
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Open your browser:**
```
http://localhost:8000
```

## 🎮 Usage

### Web Interface

1. **Image Analysis:**
   - Enter a Docker image name (e.g., `nginx:alpine`)
   - Click "Start Analysis"
   - View comprehensive results

2. **Dockerfile Upload:**
   - Upload your Dockerfile
   - Get instant analysis and recommendations
   - Compare against industry standards

### API Endpoints

#### Analyze Docker Image
```bash
curl -X POST "http://localhost:8000/api/v1/analyze/image" \
  -H "Content-Type: application/json" \
  -d '{"image_name": "nginx:alpine"}'
```

#### Upload Dockerfile
```bash
curl -X POST "http://localhost:8000/api/v1/analyze/dockerfile" \
  -F "file=@your-dockerfile"
```

#### Compare Images
```bash
curl "http://localhost:8000/api/v1/compare?image1=nginx:alpine&image2=nginx:latest"
```

## 🏗️ Architecture

```
enterprise-docker-analyzer/
├── app.py                      # FastAPI application
├── core/                       # Core analysis engines
│   ├── analyzer.py            # Docker layer analyzer
│   ├── security_scanner.py    # Vulnerability scanner
│   ├── performance_analyzer.py # Performance metrics
│   └── industry_benchmarker.py # Industry comparison
├── models/                     # Data models
│   └── analysis.py            # Pydantic models
├── utils/                      # Utilities
│   └── docker_utils.py        # Docker operations
├── static/                     # Frontend assets
│   ├── css/
│   └── js/
├── templates/                  # HTML templates
└── uploads/                    # File uploads
```

## 🔧 Configuration

### Environment Variables
```bash
# Docker API settings
DOCKER_HOST=unix://var/run/docker.sock

# Security scanner settings
TRIVY_ENABLED=true
TRIVY_SEVERITY=CRITICAL,HIGH,MEDIUM,LOW

# Performance settings
PERFORMANCE_TIMEOUT=30
```

### Docker Compose
```yaml
version: '3.8'
services:
  analyzer:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - DOCKER_HOST=unix://var/run/docker.sock
```

## 📊 Analysis Components

### 1. Docker Layer Analyzer
- **Real Docker API integration**
- **Layer-by-layer analysis**
- **Cache impact assessment**
- **Optimization opportunities**

### 2. Security Scanner
- **Trivy vulnerability scanning**
- **Root user detection**
- **Sensitive data exposure**
- **Security score calculation**

### 3. Performance Analyzer
- **Build time measurement**
- **Startup time analysis**
- **Resource usage tracking**
- **Performance benchmarking**

### 4. Industry Benchmarker
- **Docker Hub data integration**
- **Industry standards comparison**
- **Best practices recommendations**
- **Percentile ranking**

## 🎨 UI Features

### Beautiful Docker-Themed Interface
- **Blue and white color scheme**
- **Responsive design**
- **Real-time progress updates**
- **Interactive charts and metrics**

### Interactive Elements
- **Drag and drop file upload**
- **Tab-based navigation**
- **Animated progress bars**
- **Real-time notifications**

## 🔍 Analysis Examples

### Example 1: Nginx Alpine
```bash
# Analysis of nginx:alpine
curl -X POST "http://localhost:8000/api/v1/analyze/image" \
  -H "Content-Type: application/json" \
  -d '{"image_name": "nginx:alpine"}'
```

**Expected Results:**
- ✅ Small image size (~50MB)
- ✅ Few layers (5-6)
- ✅ High security score
- ✅ Fast startup time

### Example 2: Python Application
```bash
# Analysis of custom Python app
curl -X POST "http://localhost:8000/api/v1/analyze/image" \
  -H "Content-Type: application/json" \
  -d '{"image_name": "my-python-app:latest"}'
```

**Analysis Areas:**
- Layer efficiency
- Security vulnerabilities
- Performance metrics
- Industry comparison

## 🛠️ Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Adding New Analyzers
1. Create analyzer in `core/`
2. Implement analysis interface
3. Add to main application
4. Update frontend display

### Extending Security Scanner
```python
# Add custom security checks
class CustomSecurityScanner(SecurityScanner):
    async def custom_check(self, image_name: str):
        # Your custom security logic
        pass
```

## 📈 Metrics and Scoring

### Enterprise Score Calculation
- **Security (40%)**: Vulnerability count, severity, best practices
- **Performance (30%)**: Build time, startup time, resource usage
- **Efficiency (30%)**: Image size, layer count, optimization

### Scoring Ranges
- **90-100**: Outstanding
- **80-89**: Excellent
- **70-79**: Good
- **60-69**: Fair
- **0-59**: Poor

## 🔒 Security Features

### Vulnerability Scanning
- **CVE detection**
- **Severity classification**
- **Remediation recommendations**
- **Real-time updates**

### Best Practices
- **Non-root user enforcement**
- **Minimal attack surface**
- **Secure base images**
- **Secret management**

## 🚀 Deployment

### Docker Deployment
```bash
# Build image
docker build -t enterprise-docker-analyzer .

# Run container
docker run -p 8000:8000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  enterprise-docker-analyzer
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-analyzer
spec:
  replicas: 3
  selector:
    matchLabels:
      app: docker-analyzer
  template:
    metadata:
      labels:
        app: docker-analyzer
    spec:
      containers:
      - name: analyzer
        image: enterprise-docker-analyzer:latest
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: docker-sock
          mountPath: /var/run/docker.sock
      volumes:
      - name: docker-sock
        hostPath:
          path: /var/run/docker.sock
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests**
5. **Submit a pull request**

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- **Docker Community** for inspiration
- **Trivy** for vulnerability scanning
- **FastAPI** for the web framework
- **Font Awesome** for icons

---

**Built with ❤️ for the Docker community** 