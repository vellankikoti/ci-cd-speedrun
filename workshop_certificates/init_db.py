#!/usr/bin/env python3
"""
Database initialization script for the CI/CD Chaos Workshop
Creates sample scenarios and admin user
"""

import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workshop_certificates.app import create_app, db
from workshop_certificates.models import User, Scenario, Config

def init_database():
    """Initialize the database with sample data"""
    app = create_app()
    
    with app.app_context():
        print("🗄️  Initializing database...")
        
        # Create sample scenarios
        scenarios = [
            # Setup Phase
            Scenario(
                name="Environment Setup",
                phase="Setup",
                scenario_number=1,
                description="Set up your development environment with Docker, Kubernetes, and Jenkins",
                points=10,
                checkpoint_tag="Setup, Environment, points=10"
            ),
            
            # TestContainers Phase
            Scenario(
                name="PostgreSQL with TestContainers",
                phase="TestContainers",
                scenario_number=1,
                description="Run PostgreSQL tests using TestContainers",
                points=5,
                checkpoint_tag="TestContainers, PostgreSQL, points=5"
            ),
            Scenario(
                name="Redis with TestContainers",
                phase="TestContainers",
                scenario_number=2,
                description="Run Redis tests using TestContainers",
                points=5,
                checkpoint_tag="TestContainers, Redis, points=5"
            ),
            Scenario(
                name="MySQL with TestContainers",
                phase="TestContainers",
                scenario_number=3,
                description="Run MySQL tests using TestContainers",
                points=5,
                checkpoint_tag="TestContainers, MySQL, points=5"
            ),
            
            # Docker Phase
            Scenario(
                name="Docker Build Optimization",
                phase="Docker",
                scenario_number=1,
                description="Optimize Docker build process and reduce image size",
                points=5,
                checkpoint_tag="Docker, Build Optimization, points=5"
            ),
            Scenario(
                name="Multi-stage Docker Builds",
                phase="Docker",
                scenario_number=2,
                description="Create efficient multi-stage Docker builds",
                points=5,
                checkpoint_tag="Docker, Multi-stage, points=5"
            ),
            Scenario(
                name="Docker Security Scanning",
                phase="Docker",
                scenario_number=3,
                description="Scan Docker images for vulnerabilities",
                points=5,
                checkpoint_tag="Docker, Security, points=5"
            ),
            Scenario(
                name="Docker Compose Services",
                phase="Docker",
                scenario_number=4,
                description="Orchestrate multiple services with Docker Compose",
                points=5,
                checkpoint_tag="Docker, Compose, points=5"
            ),
            
            # Jenkins Phase
            Scenario(
                name="Jenkins Pipeline Setup",
                phase="Jenkins",
                scenario_number=1,
                description="Set up a basic Jenkins pipeline",
                points=5,
                checkpoint_tag="Jenkins, Pipeline Setup, points=5"
            ),
            Scenario(
                name="Jenkins Blue-Green Deployment",
                phase="Jenkins",
                scenario_number=2,
                description="Implement blue-green deployment strategy",
                points=5,
                checkpoint_tag="Jenkins, Blue-Green, points=5"
            ),
            Scenario(
                name="Jenkins Security Scanning",
                phase="Jenkins",
                scenario_number=3,
                description="Integrate security scanning in Jenkins pipeline",
                points=5,
                checkpoint_tag="Jenkins, Security, points=5"
            ),
            Scenario(
                name="Jenkins Test Automation",
                phase="Jenkins",
                scenario_number=4,
                description="Automate testing in Jenkins pipeline",
                points=5,
                checkpoint_tag="Jenkins, Test Automation, points=5"
            ),
            Scenario(
                name="Jenkins Monitoring",
                phase="Jenkins",
                scenario_number=5,
                description="Set up monitoring and alerting in Jenkins",
                points=5,
                checkpoint_tag="Jenkins, Monitoring, points=5"
            ),
            
            # Kubernetes Phase
            Scenario(
                name="Kubernetes Deployment",
                phase="Kubernetes",
                scenario_number=1,
                description="Deploy applications to Kubernetes cluster",
                points=10,
                checkpoint_tag="Kubernetes, Deployment, points=10"
            ),
            Scenario(
                name="Kubernetes Auto-scaling",
                phase="Kubernetes",
                scenario_number=2,
                description="Configure horizontal pod autoscaling",
                points=10,
                checkpoint_tag="Kubernetes, Auto-scaling, points=10"
            ),
            Scenario(
                name="Kubernetes Secrets Management",
                phase="Kubernetes",
                scenario_number=3,
                description="Manage secrets and configurations securely",
                points=10,
                checkpoint_tag="Kubernetes, Secrets, points=10"
            ),
        ]
        
        # Add scenarios to database
        for scenario in scenarios:
            existing = Scenario.query.filter_by(checkpoint_tag=scenario.checkpoint_tag).first()
            if not existing:
                db.session.add(scenario)
                print(f"✅ Added scenario: {scenario.phase} - {scenario.name}")
            else:
                print(f"⏭️  Skipped existing scenario: {scenario.phase} - {scenario.name}")
        
        # Create admin user
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@europython.org',
                full_name='Workshop Administrator',
                is_admin=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            print("✅ Created admin user (username: admin, password: admin123)")
        else:
            print("⏭️  Admin user already exists")
        
        # Commit all changes
        db.session.commit()
        print("🎉 Database initialization completed!")
        print("\n📋 Summary:")
        print(f"   • {len(scenarios)} scenarios created")
        print("   • Admin user created")
        print("   • Default configuration set up")
        print("\n🔗 Access URLs:")
        print("   • Main site: http://localhost:5000/")
        print("   • Dashboard: http://localhost:5000/app/")
        print("   • Admin: http://localhost:5000/admin/")

if __name__ == '__main__':
    init_database() 