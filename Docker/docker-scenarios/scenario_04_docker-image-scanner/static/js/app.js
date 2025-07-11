// Enterprise Docker Analyzer - Frontend JavaScript

class DockerAnalyzer {
    constructor() {
        this.currentAnalysis = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Tab navigation
        this.initializeTabNavigation();
        
        // Image analysis
        document.getElementById('analyzeBtn').addEventListener('click', () => this.analyzeImage());
        
        // Dockerfile upload
        const fileInput = document.getElementById('dockerfileInput');
        fileInput.addEventListener('change', (e) => this.handleFileUpload(e.target.files[0]));
        
        // Compare images
        document.getElementById('compareBtn').addEventListener('click', () => this.compareImages());
        
        // Real-time updates
        this.initializeWebSocket();
    }

    initializeTabNavigation() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.getAttribute('data-tab');
                
                // Remove active class from all buttons and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked button and corresponding content
                button.classList.add('active');
                document.getElementById(`${targetTab}-tab`).classList.add('active');
            });
        });
    }

    async analyzeImage() {
        const imageName = document.getElementById('imageName').value.trim();
        
        if (!imageName) {
            this.showNotification('Please enter an image name', 'error');
            return;
        }

        try {
            this.showProgress();
            this.updateStatus('🔍 Analyzing Docker image with Trivy...');
            
            const response = await fetch('/api/v1/analyze/image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    image_name: imageName,
                    analysis_type: 'comprehensive'
                })
            });

            const result = await response.json();
            
            if (response.ok && !result.error) {
                this.displayEducationalResults(result);
                this.showNotification('✅ Analysis completed successfully!', 'success');
            } else {
                this.displayError(result.error || 'Analysis failed');
                this.showNotification(result.error || 'Analysis failed', 'error');
            }
        } catch (error) {
            this.displayError('Analysis failed: ' + error.message);
            this.showNotification('Analysis failed: ' + error.message, 'error');
        } finally {
            this.hideProgress();
        }
    }

    async handleFileUpload(file) {
        if (!file) return;
        
        if (!file.name.toLowerCase().includes('dockerfile')) {
            this.showNotification('Please select a Dockerfile', 'error');
            return;
        }

        try {
            this.showProgress();
            this.updateStatus('🔍 Building and analyzing Dockerfile...');
            
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch('/api/v1/analyze/dockerfile', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok && !result.error) {
                this.displayEducationalResults(result);
                this.showNotification('✅ Dockerfile analysis completed!', 'success');
            } else {
                this.displayError(result.error || 'Dockerfile analysis failed');
                this.showNotification(result.error || 'Dockerfile analysis failed', 'error');
            }
        } catch (error) {
            this.displayError('Upload failed: ' + error.message);
            this.showNotification('Upload failed: ' + error.message, 'error');
        } finally {
            this.hideProgress();
        }
    }

    displayEducationalResults(result) {
        this.currentAnalysis = result;
        
        // Update main dashboard
        this.updateDashboard(result);
        
        // Update detailed analysis cards
        this.updateAnalysisCards(result);
        
        // Show educational insights
        this.displayLearningInsights(result);
        
        // Show best practices
        this.displayBestPractices(result);
        
        // Show industry comparison
        this.displayIndustryComparison(result);
        
        // Show detailed vulnerabilities
        this.displayVulnerabilities(result);
        
        // Update progress and status
        this.updateStatus('✅ Analysis completed successfully!');
        this.hideProgress();
    }

    updateDashboard(result) {
        const dashboard = document.getElementById('dashboard');
        
        const securityScore = result.security_analysis?.security_score || 0;
        const totalVulns = result.security_analysis?.total_vulnerabilities || 0;
        const criticalVulns = result.security_analysis?.critical_count || 0;
        const highVulns = result.security_analysis?.high_count || 0;
        
        dashboard.innerHTML = `
            <div class="dashboard-header">
                <h2>🐳 Docker Image Analysis: ${result.image_name}</h2>
                <div class="analysis-timestamp">📅 ${new Date(result.timestamp).toLocaleString()}</div>
            </div>
            
            <div class="dashboard-metrics">
                <div class="metric-card ${this.getSecurityScoreClass(securityScore)}">
                    <div class="metric-icon">🛡️</div>
                    <div class="metric-value">${securityScore.toFixed(1)}</div>
                    <div class="metric-label">Security Score</div>
                </div>
                
                <div class="metric-card ${criticalVulns > 0 ? 'critical' : 'success'}">
                    <div class="metric-icon">🚨</div>
                    <div class="metric-value">${criticalVulns}</div>
                    <div class="metric-label">Critical Vulnerabilities</div>
                </div>
                
                <div class="metric-card ${highVulns > 0 ? 'warning' : 'success'}">
                    <div class="metric-icon">⚠️</div>
                    <div class="metric-value">${highVulns}</div>
                    <div class="metric-label">High Vulnerabilities</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-icon">📊</div>
                    <div class="metric-value">${totalVulns}</div>
                    <div class="metric-label">Total Vulnerabilities</div>
                </div>
            </div>
        `;
    }

    displayLearningInsights(result) {
        const insightsContainer = document.getElementById('learningInsights');
        const insights = result.learning_insights || [];
        
        if (insights.length === 0) {
            insightsContainer.innerHTML = '<p>🎉 No significant issues found! Your image follows good practices.</p>';
            return;
        }
        
        insightsContainer.innerHTML = `
            <h3>🎓 Learning Insights</h3>
            <div class="insights-list">
                ${insights.map(insight => `
                    <div class="insight-item">
                        <div class="insight-icon">${this.getInsightIcon(insight)}</div>
                        <div class="insight-text">${insight}</div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    displayBestPractices(result) {
        const practicesContainer = document.getElementById('bestPractices');
        const practices = result.best_practices || [];
        
        if (practices.length === 0) {
            practicesContainer.innerHTML = '<p>✅ Your image follows Docker best practices!</p>';
            return;
        }
        
        practicesContainer.innerHTML = `
            <h3>📚 Best Practices Analysis</h3>
            <div class="practices-list">
                ${practices.map(practice => `
                    <div class="practice-item ${practice.priority.toLowerCase()}">
                        <div class="practice-header">
                            <span class="practice-category">${practice.category}</span>
                            <span class="practice-priority ${practice.priority.toLowerCase()}">${practice.priority}</span>
                        </div>
                        <h4>${practice.title}</h4>
                        <p class="practice-description">${practice.description}</p>
                        <div class="practice-impact">
                            <strong>Impact:</strong> ${practice.impact}
                        </div>
                        <div class="practice-recommendation">
                            <strong>Recommendation:</strong> ${practice.recommendation}
                        </div>
                        ${practice.example ? `
                            <div class="practice-example">
                                <strong>Example:</strong>
                                <pre><code>${practice.example}</code></pre>
                            </div>
                        ` : ''}
                    </div>
                `).join('')}
            </div>
        `;
    }

    displayIndustryComparison(result) {
        const comparisonContainer = document.getElementById('industryComparison');
        const comparison = result.industry_benchmark || {};
        
        if (!comparison.total_vulnerabilities) {
            comparisonContainer.innerHTML = '<p>📊 Industry comparison data not available</p>';
            return;
        }
        
        const current = comparison.total_vulnerabilities.current;
        const average = comparison.total_vulnerabilities.industry_avg;
        const percentile = comparison.total_vulnerabilities.percentile;
        
        comparisonContainer.innerHTML = `
            <h3>📊 Industry Comparison</h3>
            <div class="comparison-metrics">
                <div class="comparison-item">
                    <div class="comparison-label">Your Vulnerabilities</div>
                    <div class="comparison-value">${current}</div>
                </div>
                <div class="comparison-item">
                    <div class="comparison-label">Industry Average</div>
                    <div class="comparison-value">${average.toFixed(1)}</div>
                </div>
                <div class="comparison-item">
                    <div class="comparison-label">Percentile</div>
                    <div class="comparison-value">${percentile}</div>
                </div>
            </div>
            
            <div class="comparison-recommendations">
                <h4>Industry Recommendations:</h4>
                <ul>
                    ${(comparison.recommendations || []).map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    displayVulnerabilities(result) {
        const vulnContainer = document.getElementById('vulnerabilities');
        const vulnerabilities = result.security_analysis?.vulnerabilities || [];
        
        if (vulnerabilities.length === 0) {
            vulnContainer.innerHTML = '<p>🎉 No vulnerabilities found!</p>';
            return;
        }
        
        // Group by severity
        const critical = vulnerabilities.filter(v => v.severity === 'CRITICAL');
        const high = vulnerabilities.filter(v => v.severity === 'HIGH');
        const medium = vulnerabilities.filter(v => v.severity === 'MEDIUM');
        const low = vulnerabilities.filter(v => v.severity === 'LOW');
        
        vulnContainer.innerHTML = `
            <h3>🔍 Vulnerability Details</h3>
            
            ${critical.length > 0 ? `
                <div class="vuln-section critical">
                    <h4>🚨 Critical Vulnerabilities (${critical.length})</h4>
                    ${this.renderVulnerabilityList(critical)}
                </div>
            ` : ''}
            
            ${high.length > 0 ? `
                <div class="vuln-section high">
                    <h4>⚠️ High Vulnerabilities (${high.length})</h4>
                    ${this.renderVulnerabilityList(high)}
                </div>
            ` : ''}
            
            ${medium.length > 0 ? `
                <div class="vuln-section medium">
                    <h4>🔶 Medium Vulnerabilities (${medium.length})</h4>
                    ${this.renderVulnerabilityList(medium)}
                </div>
            ` : ''}
            
            ${low.length > 0 ? `
                <div class="vuln-section low">
                    <h4>📝 Low Vulnerabilities (${low.length})</h4>
                    ${this.renderVulnerabilityList(low)}
                </div>
            ` : ''}
        `;
    }

    renderVulnerabilityList(vulnerabilities) {
        return `
            <div class="vulnerability-list">
                ${vulnerabilities.map(vuln => `
                    <div class="vulnerability-item">
                        <div class="vuln-header">
                            <span class="vuln-cve">${vuln.cve_id}</span>
                            <span class="vuln-severity ${vuln.severity.toLowerCase()}">${vuln.severity}</span>
                        </div>
                        <div class="vuln-package">
                            <strong>Package:</strong> ${vuln.package_name} (${vuln.installed_version})
                        </div>
                        ${vuln.fixed_version ? `
                            <div class="vuln-fix">
                                <strong>Fixed in:</strong> ${vuln.fixed_version}
                            </div>
                        ` : ''}
                        <div class="vuln-description">
                            ${vuln.description}
                        </div>
                        ${vuln.cvss_score > 0 ? `
                            <div class="vuln-cvss">
                                <strong>CVSS Score:</strong> ${vuln.cvss_score.toFixed(1)}
                            </div>
                        ` : ''}
                    </div>
                `).join('')}
            </div>
        `;
    }

    updateAnalysisCards(result) {
        // Docker Analysis
        this.updateDockerAnalysis(result.docker_analysis);
        
        // Security Analysis
        this.updateSecurityAnalysis(result.security_analysis);
        
        // Performance Analysis
        this.updatePerformanceAnalysis(result.performance_analysis);
    }

    updateDockerAnalysis(analysis) {
        const container = document.getElementById('dockerAnalysis');
        if (!analysis || analysis.error) {
            container.innerHTML = '<p>Could not analyze Docker configuration</p>';
            return;
        }
        
        const sizeMB = analysis.total_size ? `${(analysis.total_size / (1024 * 1024)).toFixed(1)} MB` : 'Unknown';
        
        container.innerHTML = `
            <div class="metric"><strong>Image Size:</strong> ${sizeMB}</div>
            <div class="metric"><strong>Layer Count:</strong> ${analysis.layer_count || 'Unknown'}</div>
            <div class="metric"><strong>Base Image:</strong> ${analysis.base_image || 'Unknown'}</div>
            <div class="metric"><strong>User:</strong> ${analysis.user_configuration || 'Unknown'}</div>
            <div class="metric"><strong>Exposed Ports:</strong> ${(analysis.exposed_ports && analysis.exposed_ports.length) || 0}</div>
            <div class="metric"><strong>Environment Variables:</strong> ${(analysis.environment_vars && analysis.environment_vars.length) || 0}</div>
        `;
    }

    updateSecurityAnalysis(analysis) {
        const container = document.getElementById('securityAnalysis');
        if (!analysis) {
            container.innerHTML = '<p>No security analysis available</p>';
            return;
        }

        container.innerHTML = `
            <div class="metric"><strong>Total Vulnerabilities:</strong> ${analysis.total_vulnerabilities || 0}</div>
            <div class="metric"><strong>Critical:</strong> ${analysis.critical_count || 0}</div>
            <div class="metric"><strong>High:</strong> ${analysis.high_count || 0}</div>
            <div class="metric"><strong>Medium:</strong> ${analysis.medium_count || 0}</div>
            <div class="metric"><strong>Low:</strong> ${analysis.low_count || 0}</div>
            <div class="metric"><strong>Security Score:</strong> ${analysis.security_score?.toFixed(1) || 'N/A'}</div>
        `;
    }

    updatePerformanceAnalysis(analysis) {
        const container = document.getElementById('performanceAnalysis');
        if (!analysis || analysis.error) {
            container.innerHTML = '<p>Could not analyze performance</p>';
            return;
        }
        
        container.innerHTML = `
            <div class="metric"><strong>Image Size:</strong> ${analysis.image_size_mb || 'Unknown'} MB</div>
            <div class="metric"><strong>Performance Score:</strong> ${analysis.performance_score || 'N/A'}</div>
            <div class="metric"><strong>Recommendations:</strong> ${(analysis.recommendations && analysis.recommendations.length) || 0}</div>
        `;
    }

    getSecurityScoreClass(score) {
        if (score >= 80) return 'success';
        if (score >= 60) return 'warning';
        return 'critical';
    }

    getInsightIcon(insight) {
        if (insight.includes('🚨')) return '🚨';
        if (insight.includes('⚠️')) return '⚠️';
        if (insight.includes('🔧')) return '🔧';
        if (insight.includes('📁')) return '📁';
        if (insight.includes('🔒')) return '🔒';
        if (insight.includes('📦')) return '📦';
        if (insight.includes('🏗️')) return '🏗️';
        if (insight.includes('📊')) return '📊';
        return '💡';
    }

    async compareImages() {
        const image1 = document.getElementById('compareImage1').value.trim();
        const image2 = document.getElementById('compareImage2').value.trim();
        
        if (!image1 || !image2) {
            this.showNotification('Please enter both image names', 'error');
            return;
        }
        
        try {
            this.showProgress();
            this.updateStatus('🔍 Comparing images...');
            
            const response = await fetch(`/api/v1/compare?image1=${encodeURIComponent(image1)}&image2=${encodeURIComponent(image2)}`);
            const result = await response.json();
            
            if (response.ok) {
                this.displayComparison(result);
                this.showNotification('✅ Comparison completed!', 'success');
            } else {
                this.showNotification(result.error || 'Comparison failed', 'error');
            }
        } catch (error) {
            this.showNotification('Comparison failed: ' + error.message, 'error');
        } finally {
            this.hideProgress();
        }
    }

    displayComparison(result) {
        const comparisonContainer = document.getElementById('comparisonResults');
        
        comparisonContainer.innerHTML = `
            <h3>📊 Image Comparison</h3>
            <div class="comparison-grid">
                <div class="comparison-item">
                    <h4>${result.image1.name}</h4>
                    <div class="metric">Vulnerabilities: ${result.image1.vulnerabilities}</div>
                    <div class="metric">Security Score: ${result.image1.security_score.toFixed(1)}</div>
                </div>
                <div class="comparison-item">
                    <h4>${result.image2.name}</h4>
                    <div class="metric">Vulnerabilities: ${result.image2.vulnerabilities}</div>
                    <div class="metric">Security Score: ${result.image2.security_score.toFixed(1)}</div>
                </div>
            </div>
            <div class="comparison-recommendation">
                <strong>Recommendation:</strong> ${result.comparison.recommendation}
            </div>
        `;
    }

    showProgress() {
        document.getElementById('progress').style.display = 'block';
        document.getElementById('analyzeBtn').disabled = true;
    }

    hideProgress() {
        document.getElementById('progress').style.display = 'none';
        document.getElementById('analyzeBtn').disabled = false;
    }

    updateStatus(message) {
        const statusElement = document.getElementById('status');
        if (statusElement) {
            statusElement.textContent = message;
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    initializeWebSocket() {
        // WebSocket implementation for real-time updates
        // This would be implemented for live progress updates
    }

    displayError(message) {
        // Hide all result sections
        document.getElementById('dashboard').innerHTML = '';
        document.getElementById('learningInsights').innerHTML = '';
        document.getElementById('bestPractices').innerHTML = '';
        document.getElementById('industryComparison').innerHTML = '';
        document.getElementById('dockerAnalysis').innerHTML = '';
        document.getElementById('securityAnalysis').innerHTML = '';
        document.getElementById('performanceAnalysis').innerHTML = '';
        document.getElementById('vulnerabilities').innerHTML = '';
        document.getElementById('comparisonResults').innerHTML = '';
        // Show error in dashboard
        document.getElementById('dashboard').innerHTML = `<div class="error-message"><strong>❌ Error:</strong> ${message}</div>`;
        this.updateStatus('❌ Error: ' + message);
    }
}

// Initialize the analyzer when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new DockerAnalyzer();
}); 