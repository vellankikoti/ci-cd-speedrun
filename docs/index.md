# 🐙 CI/CD Chaos Workshop

<div class="workshop-hero">
  <div class="hero-content">
    <h1>Master CI/CD Chaos with Python, Kubernetes & Docker</h1>
    <p class="hero-subtitle">Build bulletproof pipelines that survive real-world chaos</p>
    <div class="hero-buttons">
      <a href="phases/setup.md" class="workshop-button">🚀 Start Your Journey</a>
      <a href="#workshop-overview" class="workshop-button secondary">📖 Learn More</a>
    </div>
  </div>
</div>

---

## 🎯 Workshop Overview

Welcome to the **CI/CD Chaos Workshop** — where we don't just build software, we break it, fix it, and make it better than ever. You'll learn to build pipelines that survive real-world chaos!

<div class="workshop-highlights">
  <div class="highlight-card">
    <h3>🐍 Python Automation</h3>
    <p>Write powerful automation scripts that glue your entire CI/CD pipeline together</p>
  </div>
  <div class="highlight-card">
    <h3>🐳 Docker Mastery</h3>
    <p>Build lean, secure containers that deploy anywhere, anytime</p>
  </div>
  <div class="highlight-card">
    <h3>☸️ Kubernetes Deployment</h3>
    <p>Deploy with confidence using auto-scaling and chaos-resistant architectures</p>
  </div>
  <div class="highlight-card">
    <h3>🧪 Testcontainers</h3>
    <p>Test against real databases and services in isolated containers</p>
  </div>
</div>

---

## 🗺️ Your Journey Through Chaos

<div class="journey-map">
  <div class="phase-card" onclick="window.location.href='phases/setup.md'">
    <div class="phase-number">1</div>
    <h3>🛠️ Setup & Prerequisites</h3>
    <p>Get your environment ready for chaos</p>
    <ul>
      <li>Python 3.10+ setup</li>
      <li>Docker Desktop configuration</li>
      <li>Kubernetes cluster (Minikube/Kind)</li>
      <li>Virtual environment setup</li>
    </ul>
    <div class="phase-action">
      <a href="phases/setup.md" class="phase-button">Start Setup →</a>
    </div>
  </div>

  <div class="phase-card" onclick="window.location.href='phases/testcontainers.md'">
    <div class="phase-number">2</div>
    <h3>🧪 Testcontainers Mastery</h3>
    <p>Build bulletproof database tests</p>
    <ul>
      <li>PostgreSQL, MySQL, Redis testing</li>
      <li>Chaos scenarios with containers</li>
      <li>HTML test reports</li>
      <li>Real-world failure simulation</li>
    </ul>
    <div class="phase-action">
      <a href="phases/testcontainers.md" class="phase-button">Learn Testing →</a>
    </div>
  </div>

  <div class="phase-card" onclick="window.location.href='phases/docker.md'">
    <div class="phase-number">3</div>
    <h3>🐳 Docker Optimization</h3>
    <p>Create lean, secure container images</p>
    <ul>
      <li>Multi-stage builds</li>
      <li>Image size optimization</li>
      <li>Security scanning</li>
      <li>Version management</li>
    </ul>
    <div class="phase-action">
      <a href="phases/docker.md" class="phase-button">Optimize Images →</a>
    </div>
  </div>

  <div class="phase-card" onclick="window.location.href='phases/jenkins.md'">
    <div class="phase-number">4</div>
    <h3>🤖 Jenkins Pipeline Chaos</h3>
    <p>Build resilient CI/CD pipelines</p>
    <ul>
      <li>Docker build automation</li>
      <li>Testcontainers integration</li>
      <li>HTML report generation</li>
      <li>Secret management</li>
    </ul>
    <div class="phase-action">
      <a href="phases/jenkins.md" class="phase-button">Build Pipelines →</a>
    </div>
  </div>

  <div class="phase-card" onclick="window.location.href='phases/k8s.md'">
    <div class="phase-number">5</div>
    <h3>☸️ Kubernetes Deployment</h3>
    <p>Deploy with auto-scaling and chaos resistance</p>
    <ul>
      <li>Auto-scaling with HPA</li>
      <li>Health checks and probes</li>
      <li>Chaos engineering experiments</li>
      <li>Blue-green deployments</li>
    </ul>
    <div class="phase-action">
      <a href="phases/k8s.md" class="phase-button">Deploy to K8s →</a>
    </div>
  </div>
</div>

---

## 🧪 Database Testing Scenarios

<div class="scenario-grid">
  <div class="scenario-card">
    <h4>🐘 PostgreSQL Testing</h4>
    <p>Test against real PostgreSQL databases with connection failure scenarios</p>
    <a href="testcontainers/postgres.md" class="scenario-link">Learn PostgreSQL →</a>
  </div>
  
  <div class="scenario-card">
    <h4>🐬 MySQL Testing</h4>
    <p>Master MySQL integration testing with chaos simulation</p>
    <a href="testcontainers/mysql.md" class="scenario-link">Learn MySQL →</a>
  </div>
  
  <div class="scenario-card">
    <h4>🗄️ MariaDB Testing</h4>
    <p>Test MariaDB compatibility and character set handling</p>
    <a href="testcontainers/mariadb.md" class="scenario-link">Learn MariaDB →</a>
  </div>
  
  <div class="scenario-card">
    <h4>🍃 MongoDB Testing</h4>
    <p>Test document operations and large dataset handling</p>
    <a href="testcontainers/mongodb.md" class="scenario-link">Learn MongoDB →</a>
  </div>
  
  <div class="scenario-card">
    <h4>🔴 Redis Testing</h4>
    <p>Test caching operations and memory pressure scenarios</p>
    <a href="testcontainers/redis.md" class="scenario-link">Learn Redis →</a>
  </div>
</div>

---

## 🤖 Jenkins Pipeline Scenarios

<div class="pipeline-grid">
  <div class="pipeline-card">
    <h4>🐳 Docker Build Chaos</h4>
    <p>Build Docker images with simulated failures and optimizations</p>
    <a href="jenkins/scenario_01_docker_build.md" class="pipeline-link">Docker Builds →</a>
  </div>
  
  <div class="pipeline-card">
    <h4>🧪 Testcontainers Integration</h4>
    <p>Run database tests in Jenkins with chaos scenarios</p>
    <a href="jenkins/scenario_02_testcontainers.md" class="pipeline-link">Test Integration →</a>
  </div>
  
  <div class="pipeline-card">
    <h4>📊 HTML Report Generation</h4>
    <p>Generate beautiful HTML reports for stakeholders</p>
    <a href="jenkins/scenario_03_html_reports.md" class="pipeline-link">Report Generation →</a>
  </div>
  
  <div class="pipeline-card">
    <h4>🔐 Secret Management</h4>
    <p>Secure secret handling with Gitleaks integration</p>
    <a href="jenkins/scenario_04_manage_secrets.md" class="pipeline-link">Secret Security →</a>
  </div>
  
  <div class="pipeline-card">
    <h4>☸️ EKS Deployment</h4>
    <p>Deploy to AWS EKS with monitoring and rollback</p>
    <a href="jenkins/scenario_05_deploy_eks.md" class="pipeline-link">EKS Deployment →</a>
  </div>
</div>

---

## 🎓 Certificate of Chaos

<div class="certificate-section">
  <div class="certificate-content">
    <h3>🏆 Become a Certified Chaos Slayer</h3>
    <p>Complete all phases and receive your personalized certificate of achievement</p>
    <ul>
      <li>✅ Custom PDF Certificate</li>
      <li>✅ Live demos for your portfolio</li>
      <li>✅ Confidence in Python DevOps</li>
      <li>✅ Docker and Kubernetes mastery</li>
      <li>✅ Chaos engineering expertise</li>
    </ul>
    <a href="certificate.md" class="certificate-button">Learn About Certificates →</a>
  </div>
</div>

---

## 🧭 Why This Workshop Exists

<div class="why-workshop">
  <div class="problem-section">
    <h3>❌ The Problem</h3>
    <p>Most workshops teach:</p>
    <blockquote>"Here's how to build a perfect pipeline."</blockquote>
    <p>But real life looks like this:</p>
    <ul>
      <li>🚨 Servers crash unexpectedly</li>
      <li>💾 Databases fail under load</li>
      <li>🐳 Docker images bloat over time</li>
      <li>🌐 Networks hang and timeout</li>
      <li>🧪 Tests mysteriously fail in CI</li>
    </ul>
  </div>
  
  <div class="solution-section">
    <h3>✅ Our Solution</h3>
    <p>This workshop prepares you for <strong>the real world</strong> by:</p>
    <ul>
      <li>🎯 Deliberately causing chaos</li>
      <li>🛠️ Teaching you how to handle it</li>
      <li>💪 Making you look like a hero</li>
      <li>🚀 Building confidence through experience</li>
    </ul>
  </div>
</div>

---

## 🚀 Ready to Start?

<div class="cta-section">
  <h2>Let's Create Some Chaos! 🔥</h2>
  <p>Choose your starting point:</p>
  
  <div class="cta-buttons">
    <a href="phases/setup.md" class="cta-button primary">
      <span class="button-icon">🚀</span>
      <span class="button-text">
        <strong>Start Setup</strong>
        <small>Get your environment ready</small>
      </span>
    </a>
    
    <a href="phases/testcontainers.md" class="cta-button secondary">
      <span class="button-icon">🧪</span>
      <span class="button-text">
        <strong>Begin Testing</strong>
        <small>Learn Testcontainers first</small>
      </span>
    </a>
    
    <a href="phases/docker.md" class="cta-button secondary">
      <span class="button-icon">🐳</span>
      <span class="button-text">
        <strong>Docker Mastery</strong>
        <small>Optimize your containers</small>
      </span>
    </a>
  </div>
  
  <p class="cta-note">💡 <strong>Pro Tip:</strong> Follow the phases in order for the best learning experience!</p>
</div>

---

<div class="footer-note">
  <p><strong>Remember:</strong> Chaos Agent 🕶️ is watching. Are you ready to defeat them?</p>
</div>
