/**
 * 📊 Scenario Progress Tracking Component
 * Easy-to-use progress tracking for individual scenarios
 */

class ScenarioProgress {
  constructor(scenarioName) {
    this.scenarioName = scenarioName;
    this.init();
  }

  init() {
    // Wait for workshop session to be available
    if (typeof workshopSession !== 'undefined') {
      this.createProgressButton();
    } else {
      // Wait for workshop session to load
      setTimeout(() => this.init(), 100);
    }
  }

  createProgressButton() {
    const mainContent = document.querySelector('.md-content');
    if (!mainContent) return;

    // Check if button already exists
    if (document.getElementById('scenario-progress-button')) return;

    // Only show on scenario/phase pages (not home or overview)
    const pageTitle = mainContent.querySelector('h1');
    if (!pageTitle) return;
    const scenarioName = pageTitle.textContent.trim();
    const skipTitles = [
      'Home', 'Setup', 'TestContainers Phase', 'Docker Phase', 'Jenkins Phase', 'Kubernetes Phase',
      'Certificate', 'Welcome to the Ultimate CI/CD Chaos Experience'
    ];
    if (skipTitles.some(t => scenarioName.includes(t))) return;

    const progressDiv = document.createElement('div');
    progressDiv.id = 'scenario-progress-container';
    progressDiv.style.cssText = `
      background: linear-gradient(135deg, #326CE5, #00ADD8);
      color: white;
      padding: 20px;
      border-radius: 10px;
      margin: 40px 0 0 0;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      z-index: 100;
      text-align: center;
    `;

    const isCompleted = this.isScenarioCompleted();
    
    progressDiv.innerHTML = `
      <div style=\"display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 10px;\">
        <span style=\"font-size: 24px;\">${isCompleted ? '✅' : '🎯'}</span>
        <h4 style=\"margin: 0; font-size: 18px;\">${this.scenarioName}</h4>
      </div>
      <div style=\"margin-bottom: 10px;\">
        <small style=\"opacity: 0.9;\">${isCompleted ? 'Scenario completed!' : 'Mark as completed when done'}</small>
      </div>
      <button id=\"scenario-progress-button\" onclick=\"scenarioProgress.toggleCompletion()\" style=\"
        background: ${isCompleted ? '#28a745' : 'white'};
        color: ${isCompleted ? 'white' : '#326CE5'};
        border: none;
        padding: 14px 32px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-top: 10px;
      \" onmouseover=\"this.style.transform='scale(1.02)'\" onmouseout=\"this.style.transform='scale(1)'\">
        ${isCompleted ? '✅ Completed' : '🎯 Mark Complete'}
      </button>
      <div style=\"margin-top: 15px; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 5px; font-size: 12px;\">
        <strong>Session:</strong> ${workshopSession.sessionId}<br>
        <strong>Progress:</strong> ${workshopSession.sessionData.progress.length}/${WORKSHOP_CONFIG.totalScenarios} scenarios
      </div>
    `;

    // Insert at the end of the main content
    mainContent.appendChild(progressDiv);
  }

  isScenarioCompleted() {
    if (!workshopSession || !workshopSession.sessionData) return false;
    return workshopSession.sessionData.progress.includes(this.scenarioName);
  }

  toggleCompletion() {
    if (!workshopSession || !workshopSession.sessionData) {
      this.showNoSessionAlert();
      return;
    }

    const isCompleted = this.isScenarioCompleted();
    
    if (isCompleted) {
      // Unmark as completed
      workshopSession.updateProgress(this.scenarioName, false);
      this.updateButtonState(false);
      this.showNotification('Scenario unmarked as completed', 'info');
    } else {
      // Mark as completed
      workshopSession.updateProgress(this.scenarioName, true);
      this.updateButtonState(true);
      this.showNotification('Scenario marked as completed!', 'success');
    }
  }

  updateButtonState(completed) {
    const button = document.getElementById('scenario-progress-button');
    if (!button) return;

    button.style.background = completed ? '#28a745' : 'white';
    button.style.color = completed ? 'white' : '#326CE5';
    button.textContent = completed ? '✅ Completed' : '🎯 Mark Complete';

    // Update the icon in the container
    const icon = button.parentElement.parentElement.querySelector('span');
    if (icon) {
      icon.textContent = completed ? '✅' : '🎯';
    }

    // Update the status text
    const statusText = button.parentElement.parentElement.querySelector('small');
    if (statusText) {
      statusText.textContent = completed ? 'Scenario completed!' : 'Mark as completed when done';
    }
  }

  showNoSessionAlert() {
    const alert = document.createElement('div');
    alert.style.cssText = `
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: white;
      padding: 30px;
      border-radius: 15px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.3);
      z-index: 10000;
      text-align: center;
      max-width: 400px;
      border: 2px solid #dc3545;
    `;
    
    alert.innerHTML = `
      <div style=\"font-size: 48px; margin-bottom: 20px;\">⚠️</div>
      <h3 style=\"margin: 0 0 15px 0; color: #dc3545;\">No Active Session</h3>
      <p style=\"margin: 0 0 20px 0; color: #666;\">
        You need to start a workshop session to track your progress.
      </p>
      <button onclick=\"workshopSession.createNewSession()\" style=\"
        background: linear-gradient(135deg, #326CE5, #00ADD8);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        margin: 5px;
      \">🚀 Start Workshop Session</button>
      <button onclick=\"this.parentElement.remove()\" style=\"
        background: #6c757d;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
        margin: 5px;
      \">Close</button>
    `;
    
    document.body.appendChild(alert);
  }

  showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: ${type === 'success' ? 'linear-gradient(135deg, #28a745, #20c997)' : 
                   type === 'info' ? 'linear-gradient(135deg, #17a2b8, #6f42c1)' : 
                   'linear-gradient(135deg, #dc3545, #fd7e14)'};
      color: white;
      padding: 15px 20px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      z-index: 10000;
      animation: slideIn 0.3s ease-out;
    `;
    notification.innerHTML = `
      <div style=\"display: flex; align-items: center; gap: 10px;\">
        <span style=\"font-size: 20px;\">${type === 'success' ? '✅' : type === 'info' ? 'ℹ️' : '⚠️'}</span>
        <div>
          <strong>${message}</strong>
        </div>
      </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.style.animation = 'slideOut 0.3s ease-in';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }
}

// Global variable for easy access
let scenarioProgress;

// Function to initialize scenario progress tracking
function initScenarioProgress(scenarioName) {
  scenarioProgress = new ScenarioProgress(scenarioName);
}

// Auto-detect scenario name from page title
document.addEventListener('DOMContentLoaded', function() {
  const pageTitle = document.querySelector('h1');
  if (pageTitle && pageTitle.textContent) {
    const scenarioName = pageTitle.textContent.trim();
    // Only initialize for actual scenario pages (not main pages)
    if (scenarioName && !scenarioName.includes('Home') && !scenarioName.includes('Setup')) {
      initScenarioProgress(scenarioName);
    }
  }
}); 