# 🐳⚙️ CI/CD Chaos Workshop Certificate System

A comprehensive Flask-based certificate and progress tracking system for the EuroPython CI/CD Chaos Workshop. Features gamified learning, screenshot uploads, and university-grade certificate generation.

## 🎯 Features

### ✨ Core Features
- **Progress Tracking**: Real-time points and scenario completion tracking
- **Screenshot Uploads**: Drag-and-drop interface for proof of completion
- **Certificate Generation**: Classic university-grade PDF certificates
- **Gamified Learning**: Point system with achievements and milestones
- **Admin Panel**: Event configuration and user management
- **Docker/Kubernetes Theme**: Beautiful UI with Docker and Kubernetes colors

### 🏆 Certificate System
- **Classic Design**: University-grade certificate with circular logo
- **Configurable**: Customizable text, logo size, and branding
- **Achievement Stats**: Displays total points and completed scenarios
- **Unique IDs**: Each certificate has a unique identifier
- **PDF Generation**: High-quality PDF output using WeasyPrint

### 📊 Progress Tracking
- **Point System**: 
  - Setup: 10 points
  - TestContainers: 15 points (5 per scenario)
  - Docker: 20 points (5 per scenario)
  - Jenkins: 25 points (5 per scenario)
  - Kubernetes: 30 points (10 per scenario)
- **Eligibility**: 100+ points and 8+ scenarios for certificate
- **Real-time Updates**: Live progress tracking and points calculation

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd workshop_certificates
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file:
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///workshop.db
UPLOAD_FOLDER=uploads
```

### 3. Initialize Database
```bash
python init_db.py
```

### 4. Run the Application
```bash
python -m workshop_certificates.app
```

### 5. Access the System
- **Main Site**: http://localhost:5000/
- **User Dashboard**: http://localhost:5000/app/
- **Admin Panel**: http://localhost:5000/admin/
- **Login**: http://localhost:5000/auth/login

## 🏗️ Architecture

### URL Structure
```
abc.vellanki.in/
├── /                    # MkDocs documentation
├── /docs/              # Workshop documentation
├── /app/               # Interactive app
│   ├── /dashboard      # User progress dashboard
│   ├── /upload         # Screenshot upload
│   ├── /progress       # Detailed progress
│   └── /certificate    # Certificate download
├── /auth/              # Authentication
│   ├── /login          # User login
│   └── /register       # User registration
└── /admin/             # Admin panel
    ├── /config         # Event configuration
    └── /users          # User management
```

### Database Models
- **User**: Workshop participants with authentication
- **Scenario**: Workshop phases and scenarios with points
- **Progress**: User progress tracking per scenario
- **Screenshot**: Uploaded proof of completion
- **Certificate**: Generated certificates with metadata
- **Config**: Event configuration and branding

## 🎨 Design System

### Color Palette
- **Docker Blue**: `#326CE5` (Primary)
- **Kubernetes Blue**: `#3263D2` (Secondary)
- **Light Blue**: `#00ADD8` (Accent)
- **Success Green**: `#10B981` (Progress)
- **Warning Orange**: `#F59E0B` (Alerts)
- **Error Red**: `#EF4444` (Errors)

### Certificate Design
- **Classic Layout**: University-grade certificate design
- **Circular Logo**: Configurable size circular badge
- **Achievement Stats**: Points and completion metrics
- **Professional Typography**: Times New Roman serif fonts
- **Gradient Borders**: Docker/Kubernetes color gradients

## 🔧 Configuration

### Event Configuration
The system is fully configurable through the admin panel:

```python
# Example configuration
config = Config(
    event_name="EuroPython CI/CD Chaos Workshop",
    event_date="2024",
    event_location="Prague, Czech Republic",
    certificate_title="Certificate of Completion",
    certificate_subtitle="CI/CD Chaos Engineering Workshop",
    certificate_text="This is to certify that {full_name} has successfully completed...",
    logo_size=120,
    primary_color="#326CE5",
    secondary_color="#3263D2"
)
```

### Certificate Requirements
- **Minimum Points**: 100 points
- **Minimum Scenarios**: 8 completed scenarios
- **Point Distribution**:
  - Setup: 10 points
  - TestContainers: 15 points
  - Docker: 20 points
  - Jenkins: 25 points
  - Kubernetes: 30 points

## 📱 User Experience

### Registration & Login
1. Users register with username, email, and full name
2. Full name appears on certificate
3. Secure password hashing with Flask-Login

### Progress Tracking
1. Users upload screenshots as proof of completion
2. Points awarded automatically based on scenario
3. Real-time progress updates on dashboard
4. Visual progress indicators and achievements

### Certificate Generation
1. Automatic eligibility checking
2. Classic university-grade PDF design
3. Unique certificate numbers
4. Achievement statistics display
5. Configurable branding and text

## 🛠️ Development

### Project Structure
```
workshop_certificates/
├── app.py              # Flask application factory
├── models.py           # Database models
├── views.py            # Main app views
├── auth.py             # Authentication views
├── certificate_generator.py  # PDF generation
├── init_db.py          # Database initialization
├── requirements.txt    # Dependencies
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   ├── auth/           # Authentication templates
│   └── app/            # App templates
└── uploads/            # File uploads
```

### Key Technologies
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Flask-Login**: Authentication
- **WeasyPrint**: PDF generation
- **Bootstrap 5**: UI framework
- **PostgreSQL**: Production database

## 🚀 Deployment

### Production Setup
1. **Database**: Use PostgreSQL with AWS RDS
2. **Environment**: Set production environment variables
3. **Static Files**: Serve MkDocs build from Flask
4. **Domain**: Configure for `abc.vellanki.in`

### Environment Variables
```bash
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
UPLOAD_FOLDER=/path/to/uploads
FLASK_ENV=production
```

## 🎯 Future Enhancements

### Planned Features
- **Leaderboards**: Global and event-specific rankings
- **Peer Review**: Screenshot verification by peers
- **Analytics**: Detailed progress analytics
- **Badges**: Achievement badges and milestones
- **Social Sharing**: Certificate sharing on social media
- **Mobile App**: Native mobile application

### Integration Possibilities
- **GitHub Integration**: Link GitHub profiles
- **LinkedIn Integration**: Share certificates
- **Slack Integration**: Progress notifications
- **Email Notifications**: Certificate delivery
- **API Access**: RESTful API for external tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **EuroPython**: For hosting the workshop
- **Docker**: For the amazing containerization platform
- **Kubernetes**: For the orchestration capabilities
- **Jenkins**: For the CI/CD automation
- **Testcontainers**: For the testing framework

---

**Built with ❤️ for the Python community** 