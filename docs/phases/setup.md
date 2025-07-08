# 🛠️ Workshop Setup Guide

<div class="setup-hero">
  <div class="setup-content">
    <h1>Prepare for Chaos: Complete Setup Guide</h1>
    <p class="setup-subtitle">Get your environment battle-ready to defeat the Chaos Agent 🕶️</p>
    <div class="setup-stats">
      <div class="stat-item">
        <span class="stat-number">15-20</span>
        <span class="stat-label">minutes</span>
      </div>
      <div class="stat-item">
        <span class="stat-number">8</span>
        <span class="stat-label">steps</span>
      </div>
      <div class="stat-item">
        <span class="stat-number">100%</span>
        <span class="stat-label">success rate</span>
      </div>
    </div>
  </div>
</div>

---

## 📋 Prerequisites Checklist

<div class="prerequisites-grid">
  <div class="prereq-card">
    <h3>💻 Hardware Requirements</h3>
    <ul>
      <li>Computer with 8GB+ RAM</li>
      <li>10GB+ free disk space</li>
      <li>Internet connection</li>
      <li>Administrator access</li>
    </ul>
  </div>
  
  <div class="prereq-card">
    <h3>🛠️ Software Requirements</h3>
    <ul>
      <li>Python 3.10+</li>
      <li>Docker Desktop</li>
      <li>Kubernetes cluster</li>
      <li>Git</li>
    </ul>
  </div>
  
  <div class="prereq-card">
    <h3>🎯 Workshop Goals</h3>
    <ul>
      <li>Build chaos-resistant pipelines</li>
      <li>Master Testcontainers</li>
      <li>Deploy to Kubernetes</li>
      <li>Defeat the Chaos Agent</li>
    </ul>
  </div>
</div>

---

## 🐍 Step 1: Install Python 3.10+

<div class="step-container">
  <div class="step-header">
    <div class="step-number">1</div>
    <h2>Install Python 3.10+</h2>
    <p>Set up Python for automation and testing</p>
  </div>

  <div class="platform-tabs">
    <div class="tab-content active" id="windows-python">
      <h3>🪟 Windows Installation</h3>
      
      <div class="install-step">
        <h4>1. Download Python</h4>
        <ul>
          <li>Go to <a href="https://python.org/downloads" target="_blank">python.org/downloads</a></li>
          <li>Download Python 3.10 or higher</li>
          <li><strong>Important:</strong> Check "Add Python to PATH" during installation</li>
        </ul>
      </div>
      
      <div class="install-step">
        <h4>2. Verify Installation</h4>
        <div class="code-block">
          <div class="code-header">Command Prompt</div>
          <pre><code>python --version
# Should show: Python 3.10.x or higher</code></pre>
        </div>
      </div>
    </div>

    <div class="tab-content" id="macos-python">
      <h3>🍎 macOS Installation</h3>
      
      <div class="install-step">
        <h4>Option A: Using Homebrew (Recommended)</h4>
        <div class="code-block">
          <div class="code-header">Terminal</div>
          <pre><code># Install Homebrew first if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10</code></pre>
        </div>
      </div>
      
      <div class="install-step">
        <h4>Option B: Download from python.org</h4>
        <ul>
          <li>Visit <a href="https://python.org/downloads" target="_blank">python.org/downloads</a></li>
          <li>Download the macOS installer</li>
          <li>Run the installer</li>
        </ul>
      </div>
      
      <div class="install-step">
        <h4>3. Verify Installation</h4>
        <div class="code-block">
          <div class="code-header">Terminal</div>
          <pre><code>python3 --version
# Should show: Python 3.10.x or higher</code></pre>
        </div>
      </div>
    </div>

    <div class="tab-content" id="linux-python">
      <h3>🐧 Linux Installation</h3>
      
      <div class="install-step">
        <h4>Ubuntu/Debian</h4>
        <div class="code-block">
          <div class="code-header">Terminal</div>
          <pre><code># Update package list
sudo apt update

# Install Python 3.10
sudo apt install python3.10 python3.10-venv python3-pip

# Verify installation
python3.10 --version</code></pre>
        </div>
      </div>
    </div>
  </div>
</div>

---

## 🐳 Step 2: Install Docker Desktop

<div class="step-container">
  <div class="step-header">
    <div class="step-number">2</div>
    <h2>Install Docker Desktop</h2>
    <p>Containerize your applications and run Testcontainers</p>
  </div>

  <div class="platform-tabs">
    <div class="tab-content active" id="windows-docker">
      <h3>🪟 Windows Installation</h3>
      
      <div class="install-step">
        <h4>1. Download Docker Desktop</h4>
        <ul>
          <li>Go to <a href="https://docker.com/products/docker-desktop" target="_blank">docker.com/products/docker-desktop</a></li>
          <li>Download Docker Desktop for Windows</li>
          <li>Run the installer</li>
          <li><strong>Important:</strong> Enable WSL 2 if prompted</li>
        </ul>
      </div>
      
      <div class="install-step">
        <h4>2. Start Docker Desktop</h4>
        <ul>
          <li>Launch Docker Desktop from Start Menu</li>
          <li>Wait for the whale icon to stop animating</li>
          <li>Docker is ready when the icon is static</li>
        </ul>
      </div>
      
      <div class="install-step">
        <h4>3. Verify Installation</h4>
        <div class="code-block">
          <div class="code-header">Command Prompt</div>
          <pre><code>docker --version
docker run hello-world</code></pre>
        </div>
      </div>
    </div>

    <div class="tab-content" id="macos-docker">
      <h3>🍎 macOS Installation</h3>
      
      <div class="install-step">
        <h4>1. Download Docker Desktop</h4>
        <ul>
          <li>Go to <a href="https://docker.com/products/docker-desktop" target="_blank">docker.com/products/docker-desktop</a></li>
          <li>Download Docker Desktop for Mac</li>
          <li>Drag Docker to Applications folder</li>
          <li>Launch Docker Desktop</li>
        </ul>
      </div>
      
      <div class="install-step">
        <h4>2. Verify Installation</h4>
        <div class="code-block">
          <div class="code-header">Terminal</div>
          <pre><code>docker --version
docker run hello-world</code></pre>
        </div>
      </div>
    </div>

    <div class="tab-content" id="linux-docker">
      <h3>🐧 Linux Installation</h3>
      
      <div class="install-step">
        <h4>Install Docker</h4>
        <div class="code-block">
          <div class="code-header">Terminal</div>
          <pre><code># Install Docker using convenience script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (log out and back in)
sudo usermod -aG docker $USER

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version
docker run hello-world</code></pre>
        </div>
      </div>
    </div>
  </div>
</div>

---

## ☸️ Step 3: Choose Your Kubernetes Cluster

<div class="step-container">
  <div class="step-header">
    <div class="step-number">3</div>
    <h2>Install Kubernetes</h2>
    <p>Choose the best option for your system</p>
  </div>

  <div class="k8s-options">
    <div class="k8s-option-card">
      <div class="option-header">
        <h3>🐳 Docker Desktop Kubernetes</h3>
        <span class="difficulty easy">Easiest</span>
      </div>
      <p>Perfect if you already installed Docker Desktop above!</p>
      
      <div class="install-steps">
        <h4>Setup Steps:</h4>
        <ol>
          <li>Open Docker Desktop</li>
          <li>Go to Settings → Kubernetes</li>
          <li>Check "Enable Kubernetes"</li>
          <li>Click "Apply & Restart"</li>
        </ol>
      </div>
      
      <div class="verify-step">
        <h4>Verify Installation:</h4>
        <div class="code-block">
          <div class="code-header">Terminal</div>
          <pre><code>kubectl version --client
kubectl cluster-info</code></pre>
        </div>
      </div>
    </div>

    <div class="k8s-option-card">
      <div class="option-header">
        <h3>🚀 Minikube</h3>
        <span class="difficulty medium">Popular</span>
      </div>
      <p>The most popular local Kubernetes cluster</p>
      
      <div class="install-steps">
        <h4>Install Minikube:</h4>
        
        <div class="platform-install">
          <h5>Windows:</h5>
          <div class="code-block">
            <div class="code-header">Command Prompt</div>
            <pre><code># Using Chocolatey
choco install minikube

# Or download manually from: https://minikube.sigs.k8s.io/docs/start/</code></pre>
          </div>
        </div>
        
        <div class="platform-install">
          <h5>macOS:</h5>
          <div class="code-block">
            <div class="code-header">Terminal</div>
            <pre><code># Using Homebrew
brew install minikube</code></pre>
          </div>
        </div>
        
        <div class="platform-install">
          <h5>Linux:</h5>
          <div class="code-block">
            <div class="code-header">Terminal</div>
            <pre><code># Download and install
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube</code></pre>
          </div>
        </div>
      </div>
      
      <div class="verify-step">
        <h4>Start and Verify:</h4>
        <div class="code-block">
          <div class="code-header">Terminal</div>
          <pre><code>minikube start
kubectl version --client
minikube status</code></pre>
        </div>
      </div>
    </div>

    <div class="k8s-option-card">
      <div class="option-header">
        <h3>🐳 Kind (Kubernetes in Docker)</h3>
        <span class="difficulty advanced">Advanced</span>
      </div>
      <p>Lightweight Kubernetes cluster using Docker</p>
      
      <div class="install-steps">
        <h4>Install Kind:</h4>
        
        <div class="platform-install">
          <h5>Windows:</h5>
          <div class="code-block">
            <div class="code-header">Command Prompt</div>
            <pre><code># Using Chocolatey
choco install kind</code></pre>
          </div>
        </div>
        
        <div class="platform-install">
          <h5>macOS:</h5>
          <div class="code-block">
            <div class="code-header">Terminal</div>
            <pre><code># Using Homebrew
brew install kind</code></pre>
          </div>
        </div>
        
        <div class="platform-install">
          <h5>Linux:</h5>
          <div class="code-block">
            <div class="code-header">Terminal</div>
            <pre><code># Download and install
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind</code></pre>
          </div>
        </div>
      </div>
      
      <div class="verify-step">
        <h4>Create Cluster and Verify:</h4>
        <div class="code-block">
          <div class="code-header">Terminal</div>
          <pre><code>kind create cluster --name chaos-workshop
kubectl version --client
kind get clusters</code></pre>
        </div>
      </div>
    </div>
  </div>
</div>

---

## 🎯 Step 4: Install kubectl (Kubernetes CLI)

<div class="step-container">
  <div class="step-header">
    <div class="step-number">4</div>
    <h2>Install kubectl</h2>
    <p>Command-line tool for Kubernetes</p>
  </div>

  <div class="platform-tabs">
    <div class="tab-content active" id="windows-kubectl">
      <h3>🪟 Windows Installation</h3>
      <div class="code-block">
        <div class="code-header">Command Prompt</div>
        <pre><code># Using Chocolatey
choco install kubernetes-cli

# Or download from: https://kubernetes.io/docs/tasks/tools/install-kubectl/</code></pre>
      </div>
    </div>

    <div class="tab-content" id="macos-kubectl">
      <h3>🍎 macOS Installation</h3>
      <div class="code-block">
        <div class="code-header">Terminal</div>
        <pre><code># Using Homebrew
brew install kubectl

# Or using curl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl</code></pre>
      </div>
    </div>

    <div class="tab-content" id="linux-kubectl">
      <h3>🐧 Linux Installation</h3>
      <div class="code-block">
        <div class="code-header">Terminal</div>
        <pre><code># Download kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/</code></pre>
      </div>
    </div>
  </div>

  <div class="verify-section">
    <h3>Verify kubectl Installation:</h3>
    <div class="code-block">
      <div class="code-header">All Platforms</div>
      <pre><code>kubectl version --client</code></pre>
    </div>
  </div>
</div>

---

## 📦 Step 5: Clone Workshop Repository

<div class="step-container">
  <div class="step-header">
    <div class="step-number">5</div>
    <h2>Get Workshop Code</h2>
    <p>Download the workshop materials</p>
  </div>

  <div class="install-step">
    <h3>1. Install Git (if not already installed)</h3>
    
    <div class="platform-install">
      <h4>Windows:</h4>
      <p>Download from <a href="https://git-scm.com" target="_blank">git-scm.com</a></p>
    </div>
    
    <div class="platform-install">
      <h4>macOS:</h4>
      <div class="code-block">
        <div class="code-header">Terminal</div>
        <pre><code>brew install git</code></pre>
      </div>
    </div>
    
    <div class="platform-install">
      <h4>Linux:</h4>
      <div class="code-block">
        <div class="code-header">Terminal</div>
        <pre><code>sudo apt install git  # Ubuntu/Debian
sudo yum install git  # CentOS/RHEL</code></pre>
      </div>
    </div>
  </div>

  <div class="install-step">
    <h3>2. Clone the workshop repository</h3>
    <div class="code-block">
      <div class="code-header">All Platforms</div>
      <pre><code>git clone https://github.com/vellankikoti/ci-cd-chaos-workshop.git
cd ci-cd-chaos-workshop</code></pre>
    </div>
  </div>
</div>

---

## 🐍 Step 6: Set Up Python Virtual Environment

<div class="step-container">
  <div class="step-header">
    <div class="step-number">6</div>
    <h2>Create Virtual Environment</h2>
    <p>Isolate workshop dependencies</p>
  </div>

  <div class="install-step">
    <h3>1. Create a virtual environment</h3>
    <div class="code-block">
      <div class="code-header">All Platforms</div>
      <pre><code># Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv</code></pre>
    </div>
  </div>

  <div class="install-step">
    <h3>2. Activate the virtual environment</h3>
    
    <div class="platform-activate">
      <h4>Windows:</h4>
      <div class="code-block">
        <div class="code-header">Command Prompt</div>
        <pre><code>venv\Scripts\activate</code></pre>
      </div>
    </div>
    
    <div class="platform-activate">
      <h4>macOS/Linux:</h4>
      <div class="code-block">
        <div class="code-header">Terminal</div>
        <pre><code>source venv/bin/activate</code></pre>
      </div>
    </div>
  </div>

  <div class="install-step">
    <h3>3. Verify activation</h3>
    <div class="code-block">
      <div class="code-header">All Platforms</div>
      <pre><code># You should see (venv) at the start of your prompt
which python  # macOS/Linux
where python  # Windows</code></pre>
    </div>
  </div>
</div>

---

## 📚 Step 7: Install Required Packages

<div class="step-container">
  <div class="step-header">
    <div class="step-number">7</div>
    <h2>Install Dependencies</h2>
    <p>Get all the tools you need for chaos</p>
  </div>

  <div class="install-step">
    <h3>1. Upgrade pip</h3>
    <div class="code-block">
      <div class="code-header">All Platforms</div>
      <pre><code>pip install --upgrade pip</code></pre>
    </div>
  </div>

  <div class="install-step">
    <h3>2. Install workshop dependencies</h3>
    <div class="code-block">
      <div class="code-header">All Platforms</div>
      <pre><code>pip install -r requirements.txt</code></pre>
    </div>
  </div>

  <div class="install-step">
    <h3>3. Install additional packages</h3>
    <div class="code-block">
      <div class="code-header">All Platforms</div>
      <pre><code>pip install docker
pip install kubernetes
pip install jenkins
pip install jinja2
pip install weasyprint
pip install mkdocs
pip install mkdocs-material</code></pre>
    </div>
  </div>

  <div class="install-step">
    <h3>4. Verify installations</h3>
    <div class="code-block">
      <div class="code-header">All Platforms</div>
      <pre><code>python -c "import pytest, testcontainers, docker, kubernetes, fastapi, uvicorn; print('✅ All packages installed successfully!')"</code></pre>
    </div>
  </div>
</div>

---

## 🧪 Step 8: Test Your Setup

<div class="step-container">
  <div class="step-header">
    <div class="step-number">8</div>
    <h2>Verify Everything Works</h2>
    <p>Run tests to ensure your setup is ready</p>
  </div>

  <div class="test-grid">
    <div class="test-card">
      <h3>🐍 Test Python</h3>
      <div class="code-block">
        <div class="code-header">All Platforms</div>
        <pre><code>python --version</code></pre>
      </div>
    </div>

    <div class="test-card">
      <h3>🐳 Test Docker</h3>
      <div class="code-block">
        <div class="code-header">All Platforms</div>
        <pre><code>docker run hello-world</code></pre>
      </div>
    </div>

    <div class="test-card">
      <h3>☸️ Test Kubernetes</h3>
      <div class="code-block">
        <div class="code-header">All Platforms</div>
        <pre><code>kubectl version --client
kubectl cluster-info</code></pre>
      </div>
    </div>

    <div class="test-card">
      <h3>🧪 Test Testcontainers</h3>
      <div class="code-block">
        <div class="code-header">All Platforms</div>
        <pre><code>python -c "
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

# Test Redis container
with DockerContainer('redis:alpine') as redis:
    redis.with_exposed_ports(6379)
    redis.start()
    print('✅ Testcontainers working!')
"</code></pre>
      </div>
    </div>
  </div>
</div>

---

## 🎉 Step 9: You're Ready!

<div class="success-section">
  <div class="success-content">
    <h2>🎊 Congratulations! You're Ready for Chaos!</h2>
    <p>If all tests pass, you're ready to battle the Chaos Agent! 🕶️</p>
    
    <div class="next-steps">
      <h3>🚀 Next Steps:</h3>
      <ol>
        <li>✅ Read the <a href="../index">Workshop Overview</a></li>
        <li>✅ Start with <a href="../phases/testcontainers">Phase 1: Test Mayhem</a></li>
        <li>✅ Prepare to defeat chaos! 🔥</li>
      </ol>
    </div>
  </div>
</div>

---

## 🆘 Troubleshooting

<div class="troubleshooting-section">
  <h2>Common Issues & Solutions</h2>

  <div class="trouble-grid">
    <div class="trouble-card">
      <h3>🐳 Docker not starting</h3>
      <ul>
        <li><strong>Windows:</strong> Make sure WSL 2 is enabled</li>
        <li><strong>macOS:</strong> Check Docker Desktop is running</li>
        <li><strong>Linux:</strong> Run <code>sudo systemctl start docker</code></li>
      </ul>
    </div>

    <div class="trouble-card">
      <h3>☸️ Kubernetes connection issues</h3>
      <ul>
        <li><strong>Minikube:</strong> Run <code>minikube start</code></li>
        <li><strong>Kind:</strong> Run <code>kind create cluster</code></li>
        <li><strong>Docker Desktop:</strong> Enable Kubernetes in settings</li>
      </ul>
    </div>

    <div class="trouble-card">
      <h3>🐍 Python package issues</h3>
      <ul>
        <li>Make sure your virtual environment is activated</li>
        <li>Try: <code>pip install --upgrade pip setuptools wheel</code></li>
        <li>Check Python version: <code>python --version</code></li>
      </ul>
    </div>

    <div class="trouble-card">
      <h3>🔐 Permission errors</h3>
      <ul>
        <li><strong>Windows:</strong> Run as Administrator</li>
        <li><strong>Linux/macOS:</strong> Use <code>sudo</code> where needed</li>
        <li>Check file permissions and ownership</li>
      </ul>
    </div>
  </div>

  <div class="help-section">
    <h3>Still Stuck?</h3>
    <ol>
      <li>Check the <a href="../troubleshooting">Troubleshooting Guide</a></li>
      <li>Ask in the workshop Discord/Slack</li>
      <li>Open an issue on GitHub</li>
    </ol>
  </div>
</div>

---

## 🎯 Quick Verification Checklist

<div class="verification-section">
  <h2>Final Verification</h2>
  <p>Before the workshop starts, make sure you can run:</p>

  <div class="verification-grid">
    <div class="verify-item">
      <h4>✅ Python works</h4>
      <div class="code-block">
        <pre><code>python --version</code></pre>
      </div>
    </div>

    <div class="verify-item">
      <h4>✅ Docker works</h4>
      <div class="code-block">
        <pre><code>docker run hello-world</code></pre>
      </div>
    </div>

    <div class="verify-item">
      <h4>✅ Kubernetes works</h4>
      <div class="code-block">
        <pre><code>kubectl version --client</code></pre>
      </div>
    </div>

    <div class="verify-item">
      <h4>✅ Virtual environment is active</h4>
      <div class="code-block">
        <pre><code>echo $VIRTUAL_ENV  # Should show path to venv</code></pre>
      </div>
    </div>

    <div class="verify-item">
      <h4>✅ Packages are installed</h4>
      <div class="code-block">
        <pre><code>python -c "import pytest, testcontainers, docker, kubernetes, fastapi, uvicorn; print('Ready!')"</code></pre>
      </div>
    </div>
  </div>

  <div class="ready-message">
    <p><strong>If all ✅ pass, you're ready to create some chaos! 🧨</strong></p>
  </div>
</div>

---

<div class="footer-note">
  <p><strong>See you in the workshop! Let's defeat that Chaos Agent together! 🕶️🔥</strong></p>
</div>
