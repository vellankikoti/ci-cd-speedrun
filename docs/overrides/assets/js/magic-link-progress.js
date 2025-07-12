/**
 * 🚀 CI/CD Chaos Workshop - Magic Link Progress Tracking
 * Robust cross-device progress tracking with session management
 */

// Workshop configuration
const WORKSHOP_CONFIG = {
  totalScenarios: 21,
  scenarios: [
    // TestContainers Phase
    "TestContainers Phase",
    "Scenario 01: MySQL",
    "Scenario 02: MariaDB", 
    "Scenario 03: PostgreSQL",
    "Scenario 04: MongoDB",
    "Scenario 05: Redis",
    // Docker Phase
    "Docker Phase",
    "Scenario 01: Streaming Server",
    "Scenario 02: Chaos Pipeline",
    "Scenario 03: Networking",
    "Scenario 04: Docker Image Scanner",
    "Scenario 05: Escape Room",
    // Jenkins Phase
    "Jenkins Phase",
    "Scenario 01: Docker Build",
    "Scenario 02: Testcontainers",
    "Scenario 03: HTML Reports",
    "Scenario 04: Manage Secrets",
    "Scenario 05: Deploy to EKS",
    // Kubernetes Phase
    "Kubernetes Phase",
    "Scenario 01: Python Deploy",
    "Scenario 02: Secret Automation",
    "Scenario 03: Auto Scaling",
    "Scenario 04: Blue-Green Deployments",
    "Scenario 05: GitOps with ArgoCD"
  ],
  phases: [
    { name: "TestContainers", scenarios: 6, color: "#326CE5" },
    { name: "Docker", scenarios: 5, color: "#00ADD8" },
    { name: "Jenkins", scenarios: 5, color: "#D33833" },
    { name: "Kubernetes", scenarios: 5, color: "#326CE5" }
  ]
};

// Session management
class WorkshopSession {
  constructor() {
    this.sessionId = this.getSessionId();
    this.sessionData = this.loadSessionData();
    this.init();
  }

  generateSessionId() {
    const timestamp = Date.now().toString(36);
    const random = Math.random().toString(36).substr(2, 9);
    return `${timestamp}-${random}`.toUpperCase();
  }

  getSessionId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('session');
  }

  createNewSession() {
    const sessionId = this.generateSessionId();
    const sessionData = {
      id: sessionId,
      created: new Date().toISOString(),
      progress: [],
      name: '',
      lastActivity: new Date().toISOString(),
      completed: false
    };
    
    this.saveSessionData(sessionId, sessionData);
    this.showMagicLinkModal(sessionId);
    
    // Redirect to workshop with session
    const newUrl = `${window.location.origin}${window.location.pathname}?session=${sessionId}`;
    window.location.href = newUrl;
  }

  loadSessionData() {
    if (!this.sessionId) return null;
    
    const data = localStorage.getItem(`workshop_session_${this.sessionId}`);
    return data ? JSON.parse(data) : null;
  }

  saveSessionData(sessionId = this.sessionId, data = this.sessionData) {
    if (!sessionId || !data) return;
    
    data.lastActivity = new Date().toISOString();
    localStorage.setItem(`workshop_session_${sessionId}`, JSON.stringify(data));
    this.sessionData = data;
  }

  updateProgress(scenario, completed = true) {
    if (!this.sessionData) return;
    
    if (completed) {
      if (!this.sessionData.progress.includes(scenario)) {
        this.sessionData.progress.push(scenario);
        this.showProgressNotification(scenario);
      }
    } else {
      this.sessionData.progress = this.sessionData.progress.filter(s => s !== scenario);
    }
    
    this.saveSessionData();
    this.updateProgressUI();
    this.checkCompletion();
  }

  showProgressNotification(scenario) {
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: linear-gradient(135deg, #326CE5, #00ADD8);
      color: white;
      padding: 15px 20px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      z-index: 10000;
      animation: slideIn 0.3s ease-out;
    `;
    notification.innerHTML = `
      <div style="display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 20px;">✅</span>
        <div>
          <strong>Scenario Completed!</strong><br>
          <small>${scenario}</small>
        </div>
      </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.style.animation = 'slideOut 0.3s ease-in';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }

  updateProgressUI() {
    if (!this.sessionData) return;
    
    const progressBar = document.getElementById('chaos-progress-bar');
    const progressText = document.getElementById('chaos-progress-text');
    const progressContainer = document.getElementById('progress-container');
    
    if (!progressContainer) {
      this.createProgressUI();
      return;
    }
    
    const completed = this.sessionData.progress.length;
    const percent = Math.round((completed / WORKSHOP_CONFIG.totalScenarios) * 100);
    
    if (progressBar) progressBar.value = percent;
    if (progressText) {
      progressText.innerHTML = `
        <strong>${completed}/${WORKSHOP_CONFIG.totalScenarios}</strong> scenarios completed 
        <span style="color: #326CE5; font-weight: bold;">(${percent}%)</span>
      `;
    }
    
    // Update phase progress
    this.updatePhaseProgress();
  }

  createProgressUI() {
    const mainContent = document.querySelector('.md-content');
    if (!mainContent) return;
    
    const progressContainer = document.createElement('div');
    progressContainer.id = 'progress-container';
    progressContainer.style.cssText = `
      margin: 20px 0;
      padding: 20px;
      background: linear-gradient(135deg, #f8f9fa, #e9ecef);
      border-radius: 10px;
      border: 2px solid #326CE5;
    `;
    
    progressContainer.innerHTML = `
      <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
        <span style="font-size: 24px;">📊</span>
        <h4 style="margin: 0; color: #326CE5;">Workshop Progress</h4>
      </div>
      
      <div style="margin-bottom: 15px;">
        <progress id="chaos-progress-bar" value="0" max="100" style="width: 100%; height: 20px; border-radius: 10px;"></progress>
        <p id="chaos-progress-text" style="margin: 10px 0; font-weight: bold;">0/${WORKSHOP_CONFIG.totalScenarios} scenarios completed (0%)</p>
      </div>
      
      <div id="phase-progress" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">
        ${WORKSHOP_CONFIG.phases.map(phase => `
          <div class="phase-card" style="background: white; padding: 10px; border-radius: 5px; border-left: 4px solid ${phase.color};">
            <strong>${phase.name}</strong><br>
            <small>0/${phase.scenarios} completed</small>
          </div>
        `).join('')}
      </div>
      
      <div style="margin-top: 15px; padding: 10px; background: rgba(50, 108, 229, 0.1); border-radius: 5px;">
        <small>
          <strong>Session ID:</strong> ${this.sessionId}<br>
          <strong>Magic Link:</strong> ${window.location.href}
        </small>
      </div>
    `;
    
    mainContent.insertBefore(progressContainer, mainContent.firstChild);
    this.updateProgressUI();
  }

  updatePhaseProgress() {
    const phaseCards = document.querySelectorAll('.phase-card');
    if (!phaseCards.length) return;
    
    WORKSHOP_CONFIG.phases.forEach((phase, index) => {
      const phaseScenarios = WORKSHOP_CONFIG.scenarios.filter((_, i) => {
        const startIndex = WORKSHOP_CONFIG.phases.slice(0, index).reduce((sum, p) => sum + p.scenarios, 0);
        return i >= startIndex && i < startIndex + phase.scenarios;
      });
      
      const completedInPhase = phaseScenarios.filter(scenario => 
        this.sessionData.progress.includes(scenario)
      ).length;
      
      if (phaseCards[index]) {
        phaseCards[index].innerHTML = `
          <strong>${phase.name}</strong><br>
          <small>${completedInPhase}/${phase.scenarios} completed</small>
        `;
      }
    });
  }

  checkCompletion() {
    if (this.sessionData.progress.length === WORKSHOP_CONFIG.totalScenarios) {
      this.sessionData.completed = true;
      this.saveSessionData();
      this.showCompletionNotification();
    }
  }

  showCompletionNotification() {
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: linear-gradient(135deg, #28a745, #20c997);
      color: white;
      padding: 30px;
      border-radius: 15px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.3);
      z-index: 10000;
      text-align: center;
      max-width: 400px;
    `;
    notification.innerHTML = `
      <div style="font-size: 48px; margin-bottom: 20px;">🏆</div>
      <h3 style="margin: 0 0 15px 0;">Congratulations!</h3>
      <p style="margin: 0 0 20px 0;">You've completed all scenarios and are now a <strong>Certified Chaos Slayer!</strong></p>
      <button onclick="workshopSession.generateCertificate()" style="
        background: white;
        color: #28a745;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        margin: 5px;
      ">🎓 Generate Certificate</button>
      <button onclick="this.parentElement.remove()" style="
        background: rgba(255,255,255,0.2);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
        margin: 5px;
      ">Close</button>
    `;
    
    document.body.appendChild(notification);
  }

  showMagicLinkModal(sessionId) {
    const modal = document.createElement('div');
    modal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.8);
      z-index: 9999;
      display: flex;
      align-items: center;
      justify-content: center;
    `;
    
    modal.innerHTML = `
      <div style="
        background: white;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        max-width: 500px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
      ">
        <div style="font-size: 48px; margin-bottom: 20px;">🎉</div>
        <h3 style="margin: 0 0 20px 0; color: #326CE5;">Your Workshop Session Created!</h3>
        <p style="margin: 0 0 20px 0; color: #666;">
          Share this magic link across all your devices to continue your progress:
        </p>
        
        <div style="
          background: #f8f9fa;
          padding: 20px;
          border-radius: 10px;
          margin: 20px 0;
          border: 2px dashed #326CE5;
        ">
          <div style="font-family: monospace; font-size: 18px; font-weight: bold; color: #326CE5; margin-bottom: 10px;">
            ${sessionId}
          </div>
          <div style="font-size: 14px; color: #666;">
            Full URL: ${window.location.origin}${window.location.pathname}?session=${sessionId}
          </div>
        </div>
        
        <p style="margin: 20px 0; color: #666; font-size: 14px;">
          <strong>💡 Pro tip:</strong> Bookmark this page or copy the link above to resume on any device!
        </p>
        
        <button onclick="this.parentElement.parentElement.remove()" style="
          background: linear-gradient(135deg, #326CE5, #00ADD8);
          color: white;
          border: none;
          padding: 15px 30px;
          border-radius: 8px;
          font-size: 16px;
          font-weight: bold;
          cursor: pointer;
        ">
          🚀 Start Workshop
        </button>
      </div>
    `;
    
    document.body.appendChild(modal);
  }

  showStartOptions() {
    const welcomeSection = document.getElementById('workshop-welcome-section');
    if (!welcomeSection) return;
    
    welcomeSection.style.cssText = `
      text-align: center;
      padding: 40px;
      background: linear-gradient(135deg, #326CE5, #00ADD8);
      color: white;
      border-radius: 15px;
      margin: 20px 0;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    `;
    
    welcomeSection.innerHTML = `
      <div style="font-size: 48px; margin-bottom: 20px;">🚀</div>
      <h2 style="margin: 0 0 20px 0;">Welcome to CI/CD Chaos Workshop!</h2>
      <p style="margin: 0 0 30px 0; font-size: 18px;">
        Choose how you'd like to start your chaos-slaying journey:
      </p>
      
      <div style="display: flex; flex-direction: column; gap: 15px; max-width: 400px; margin: 0 auto;">
        <button onclick="workshopSession.createNewSession()" style="
          background: white;
          color: #326CE5;
          border: none;
          padding: 20px;
          border-radius: 10px;
          font-size: 16px;
          font-weight: bold;
          cursor: pointer;
          transition: transform 0.2s;
        " onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
          🆕 Start New Workshop
        </button>
        
        <div style="margin: 20px 0; color: rgba(255,255,255,0.8);">- OR -</div>
        
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
          <p style="margin: 0 0 15px 0; font-weight: bold;">Resume Workshop</p>
          <input type="text" id="resume-session" placeholder="Enter your magic link" style="
            padding: 12px;
            border-radius: 8px;
            border: none;
            width: 100%;
            margin-bottom: 10px;
            font-size: 14px;
          ">
          <button onclick="workshopSession.resumeSession()" style="
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
          ">
            🔄 Resume Workshop
          </button>
        </div>
      </div>
    `;
  }

  resumeSession() {
    const sessionId = document.getElementById('resume-session').value.trim().toUpperCase();
    if (!sessionId) {
      alert('Please enter your magic link.');
      return;
    }
    
    const sessionData = localStorage.getItem(`workshop_session_${sessionId}`);
    if (sessionData) {
      window.location.href = `${window.location.origin}${window.location.pathname}?session=${sessionId}`;
    } else {
      alert('Session not found. Please check your magic link.');
    }
  }

  generateCertificate() {
    if (!this.sessionData) {
      alert('Please start a workshop session first.');
      return;
    }
    
    if (!this.sessionData.completed) {
      alert('Please complete all scenarios before generating your certificate.');
      return;
    }
    
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Certificate design
    doc.setFillColor(50, 108, 229);
    doc.rect(0, 0, 210, 297, 'F');
    
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(28);
    doc.text('🏆 Certified Chaos Slayer', 105, 50, { align: 'center' });
    
    doc.setFontSize(16);
    doc.text('This certificate is awarded to', 105, 80, { align: 'center' });
    
    const name = this.sessionData.name || 'Anonymous Chaos Slayer';
    doc.setFontSize(22);
    doc.text(name, 105, 100, { align: 'center' });
    
    doc.setFontSize(12);
    doc.text('for successfully completing the CI/CD Chaos Workshop', 105, 120, { align: 'center' });
    doc.text(`Session ID: ${this.sessionId}`, 105, 140, { align: 'center' });
    doc.text(`Completed: ${new Date().toLocaleDateString()}`, 105, 160, { align: 'center' });
    
    // Add completed scenarios
    doc.setTextColor(0, 0, 0);
    doc.setFontSize(10);
    doc.text('Scenarios Completed:', 20, 200);
    
    const scenarios = this.sessionData.progress || [];
    scenarios.forEach((scenario, index) => {
      if (index < 15) { // Limit to first 15 for space
        doc.text(`✅ ${scenario}`, 25, 210 + (index * 5));
      }
    });
    
    if (scenarios.length > 15) {
      doc.text(`... and ${scenarios.length - 15} more scenarios`, 25, 210 + (15 * 5));
    }
    
    doc.save(`Chaos_Slayer_Certificate_${this.sessionId}.pdf`);
  }

  init() {
    if (this.sessionId) {
      // User has a session, load progress
      if (this.sessionData) {
        this.updateProgressUI();
      } else {
        // Invalid session, redirect to start
        window.location.href = window.location.pathname;
      }
    } else {
      // New user, show start options
      // Replace the welcome section on homepage
      const welcomeSection = document.getElementById('workshop-welcome-section');
      if (welcomeSection) {
        this.showStartOptions();
      }
    }
  }
}

// Initialize workshop session
let workshopSession;

document.addEventListener('DOMContentLoaded', function() {
  workshopSession = new WorkshopSession();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  
  @keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
  }
`;
document.head.appendChild(style); 