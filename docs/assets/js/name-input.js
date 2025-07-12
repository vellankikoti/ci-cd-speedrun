/**
 * 👤 Name Input Component for Certificate Generation
 * Allows users to set their name for certificate generation
 */

class NameInput {
  constructor() {
    this.init();
  }

  init() {
    // Wait for workshop session to be available
    if (typeof workshopSession !== 'undefined') {
      this.createNameInput();
    } else {
      // Wait for workshop session to load
      setTimeout(() => this.init(), 100);
    }
  }

  createNameInput() {
    const mainContent = document.querySelector('.md-content');
    if (!mainContent) return;

    // Check if name input already exists
    if (document.getElementById('name-input-container')) return;

    const nameDiv = document.createElement('div');
    nameDiv.id = 'name-input-container';
    nameDiv.style.cssText = `
      background: #f8f9fa;
      padding: 20px;
      border-radius: 10px;
      border: 2px solid #326CE5;
      margin: 20px 0;
    `;

    const currentName = this.getCurrentName();
    
    nameDiv.innerHTML = `
      <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
        <span style="font-size: 24px;">👤</span>
        <h4 style="margin: 0; color: #326CE5;">Certificate Name</h4>
      </div>
      
      <p style="margin: 0 0 15px 0; color: #666; font-size: 14px;">
        Set your name for the certificate. This will appear on your "Certified Chaos Slayer" certificate.
      </p>
      
      <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
        <input type="text" id="certificate-name" placeholder="Enter your name" value="${currentName}" style="
          padding: 12px;
          border: 2px solid #326CE5;
          border-radius: 8px;
          font-size: 16px;
          flex: 1;
          min-width: 200px;
        ">
        <button onclick="nameInput.saveName()" style="
          background: linear-gradient(135deg, #326CE5, #00ADD8);
          color: white;
          border: none;
          padding: 12px 24px;
          border-radius: 8px;
          font-weight: bold;
          cursor: pointer;
          transition: transform 0.2s;
        " onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
          💾 Save Name
        </button>
      </div>
      
      ${currentName ? `
        <div style="margin-top: 15px; padding: 10px; background: rgba(50, 108, 229, 0.1); border-radius: 5px; font-size: 12px;">
          <strong>Current name:</strong> ${currentName}<br>
          <small>This name will appear on your certificate</small>
        </div>
      ` : ''}
    `;

    // Insert after the first h1 or at the top
    const firstH1 = mainContent.querySelector('h1');
    if (firstH1) {
      firstH1.parentNode.insertBefore(nameDiv, firstH1.nextSibling);
    } else {
      mainContent.insertBefore(nameDiv, mainContent.firstChild);
    }
  }

  getCurrentName() {
    if (!workshopSession || !workshopSession.sessionData) return '';
    return workshopSession.sessionData.name || '';
  }

  saveName() {
    const nameInput = document.getElementById('certificate-name');
    const name = nameInput.value.trim();
    
    if (!name) {
      this.showNotification('Please enter a name for your certificate.', 'warning');
      return;
    }

    if (!workshopSession || !workshopSession.sessionData) {
      this.showNotification('Please start a workshop session first.', 'warning');
      return;
    }

    // Save name to session data
    workshopSession.sessionData.name = name;
    workshopSession.saveSessionData();
    
    this.showNotification('Name saved successfully!', 'success');
    this.updateNameDisplay(name);
  }

  updateNameDisplay(name) {
    const nameDisplay = document.querySelector('#name-input-container div:last-child');
    if (nameDisplay && name) {
      nameDisplay.innerHTML = `
        <strong>Current name:</strong> ${name}<br>
        <small>This name will appear on your certificate</small>
      `;
    }
  }

  showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: ${type === 'success' ? 'linear-gradient(135deg, #28a745, #20c997)' : 
                   type === 'warning' ? 'linear-gradient(135deg, #ffc107, #fd7e14)' : 
                   'linear-gradient(135deg, #dc3545, #fd7e14)'};
      color: white;
      padding: 15px 20px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      z-index: 10000;
      animation: slideIn 0.3s ease-out;
    `;
    notification.innerHTML = `
      <div style="display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 20px;">${type === 'success' ? '✅' : type === 'warning' ? '⚠️' : '❌'}</span>
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
let nameInput;

// Function to initialize name input
function initNameInput() {
  nameInput = new NameInput();
}

// Initialize on certificate page
document.addEventListener('DOMContentLoaded', function() {
  // Only show on certificate page
  if (window.location.pathname.includes('certificate')) {
    initNameInput();
  }
}); 