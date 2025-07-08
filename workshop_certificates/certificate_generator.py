import os
from datetime import datetime
from weasyprint import HTML, CSS
from .models import db, Config, User

def generate_certificate_pdf(certificate):
    """Generate a classic university-grade certificate PDF"""
    
    # Get configuration
    config = Config.get_config()
    user = User.query.get(certificate.user_id)
    
    # Create HTML content with classic certificate design
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4 landscape;
                margin: 0;
            }}
            
            body {{
                font-family: 'Times New Roman', serif;
                margin: 0;
                padding: 40px;
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .certificate-container {{
                width: 100%;
                max-width: 1000px;
                background: white;
                border: 8px solid #326CE5;
                border-radius: 20px;
                padding: 60px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                position: relative;
                overflow: hidden;
            }}
            
            .certificate-container::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 8px;
                background: linear-gradient(135deg, #326CE5 0%, #3263D2 100%);
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 40px;
                position: relative;
            }}
            
            .logo-container {{
                width: {config.logo_size}px;
                height: {config.logo_size}px;
                border-radius: 50%;
                background: linear-gradient(135deg, #326CE5 0%, #3263D2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 20px;
                box-shadow: 0 8px 25px rgba(50, 108, 229, 0.3);
                border: 4px solid white;
            }}
            
            .logo-text {{
                color: white;
                font-size: {config.logo_size // 3}px;
                font-weight: bold;
                text-align: center;
                line-height: 1.2;
            }}
            
            .title {{
                font-size: 48px;
                font-weight: bold;
                color: #326CE5;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 2px;
            }}
            
            .subtitle {{
                font-size: 24px;
                color: #3263D2;
                margin-bottom: 20px;
                font-style: italic;
            }}
            
            .content {{
                text-align: center;
                margin: 40px 0;
                line-height: 1.8;
            }}
            
            .certificate-text {{
                font-size: 20px;
                color: #374151;
                margin-bottom: 30px;
                line-height: 1.6;
            }}
            
            .recipient-name {{
                font-size: 36px;
                font-weight: bold;
                color: #326CE5;
                margin: 30px 0;
                text-transform: uppercase;
                letter-spacing: 1px;
                border-bottom: 3px solid #326CE5;
                padding-bottom: 10px;
                display: inline-block;
            }}
            
            .details {{
                display: flex;
                justify-content: space-between;
                margin-top: 50px;
                font-size: 16px;
                color: #6B7280;
            }}
            
            .signature-section {{
                display: flex;
                justify-content: space-between;
                margin-top: 60px;
                align-items: flex-end;
            }}
            
            .signature-box {{
                text-align: center;
                flex: 1;
                margin: 0 20px;
            }}
            
            .signature-line {{
                width: 200px;
                height: 2px;
                background: #326CE5;
                margin: 20px auto 10px;
            }}
            
            .signature-name {{
                font-weight: bold;
                color: #326CE5;
                font-size: 18px;
            }}
            
            .signature-title {{
                color: #6B7280;
                font-size: 14px;
            }}
            
            .certificate-number {{
                position: absolute;
                bottom: 20px;
                right: 20px;
                font-size: 12px;
                color: #9CA3AF;
            }}
            
            .achievement-details {{
                background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                border: 2px solid #326CE5;
                border-radius: 10px;
                padding: 20px;
                margin: 30px 0;
                text-align: center;
            }}
            
            .achievement-title {{
                font-size: 18px;
                font-weight: bold;
                color: #326CE5;
                margin-bottom: 10px;
            }}
            
            .achievement-stats {{
                display: flex;
                justify-content: space-around;
                margin-top: 15px;
            }}
            
            .stat {{
                text-align: center;
            }}
            
            .stat-number {{
                font-size: 24px;
                font-weight: bold;
                color: #326CE5;
            }}
            
            .stat-label {{
                font-size: 14px;
                color: #6B7280;
            }}
            
            .border-pattern {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                pointer-events: none;
            }}
        </style>
    </head>
    <body>
        <div class="certificate-container">
            <div class="border-pattern"></div>
            
            <div class="header">
                <div class="logo-container">
                    <div class="logo-text">🐳⚙️</div>
                </div>
                <div class="title">{config.certificate_title}</div>
                <div class="subtitle">{config.certificate_subtitle}</div>
            </div>
            
            <div class="content">
                <div class="certificate-text">
                    {config.certificate_text.format(full_name=user.full_name)}
                </div>
                
                <div class="recipient-name">{user.full_name}</div>
                
                <div class="achievement-details">
                    <div class="achievement-title">Workshop Achievements</div>
                    <div class="achievement-stats">
                        <div class="stat">
                            <div class="stat-number">{certificate.total_points}</div>
                            <div class="stat-label">Total Points</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">{certificate.completed_scenarios}</div>
                            <div class="stat-label">Scenarios Completed</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">{certificate.generated_at.strftime('%Y')}</div>
                            <div class="stat-label">Year</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="details">
                <div>
                    <strong>Event:</strong> {config.event_name}<br>
                    <strong>Date:</strong> {config.event_date}<br>
                    <strong>Location:</strong> {config.event_location}
                </div>
                <div>
                    <strong>Certificate #:</strong> {certificate.certificate_number}<br>
                    <strong>Issued:</strong> {certificate.generated_at.strftime('%B %d, %Y')}<br>
                    <strong>Valid:</strong> Lifetime
                </div>
            </div>
            
            <div class="signature-section">
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div class="signature-name">Workshop Director</div>
                    <div class="signature-title">EuroPython CI/CD Chaos Workshop</div>
                </div>
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div class="signature-name">Technical Lead</div>
                    <div class="signature-title">Docker & Kubernetes Expert</div>
                </div>
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div class="signature-name">Program Chair</div>
                    <div class="signature-title">EuroPython Conference</div>
                </div>
            </div>
            
            <div class="certificate-number">
                Certificate ID: {certificate.certificate_number}
            </div>
        </div>
    </body>
    </html>
    """
    
    # Generate PDF
    html = HTML(string=html_content)
    css = CSS(string='')
    
    # Ensure upload directory exists
    upload_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate filename
    pdf_filename = f"certificate_{certificate.certificate_number}.pdf"
    pdf_path = os.path.join(upload_dir, pdf_filename)
    
    # Write PDF
    html.write_pdf(pdf_path, stylesheets=[css])
    
    return pdf_filename 