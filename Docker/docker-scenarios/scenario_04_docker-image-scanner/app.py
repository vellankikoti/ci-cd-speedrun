#!/usr/bin/env python3
"""
Enterprise Docker Image Analyzer
A comprehensive Docker image analysis platform with real-time insights
"""

from fastapi import FastAPI, Request, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import json
import uuid
from datetime import datetime
from pathlib import Path
import re
import tempfile
import shutil
import zipfile
import tarfile
try:
    import rarfile
    RAR_SUPPORT = True
except ImportError:
    RAR_SUPPORT = False

from core.trivy_analyzer import TrivyEducationalAnalyzer
from models.analysis import AnalysisRequest, AnalysisResult
from utils.docker_utils import DockerUtils

app = FastAPI(
    title="Enterprise Docker Image Analyzer",
    description="Comprehensive Docker image analysis with real-time insights and educational value",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize educational analyzer
trivy_analyzer = TrivyEducationalAnalyzer()
docker_utils = DockerUtils()

# WebSocket connections
active_connections = []

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main dashboard with Docker-themed interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/v1/analyze/image")
async def analyze_image(request: AnalysisRequest):
    """Analyze Docker image with real Trivy data and educational insights"""
    analysis_id = str(uuid.uuid4())
    
    try:
        # Perform comprehensive educational analysis
        analysis_result = await trivy_analyzer.analyze_image_educational(request.image_name)
        
        # Convert to API response format
        response_data = {
            "analysis_id": analysis_id,
            "image_name": request.image_name,
            "status": "completed",
            "timestamp": analysis_result.scan_timestamp.isoformat(),
            
            # Security Analysis (Real Trivy Data)
            "security_analysis": {
                "total_vulnerabilities": analysis_result.total_vulnerabilities,
                "critical_count": len(analysis_result.critical_vulnerabilities),
                "high_count": len(analysis_result.high_vulnerabilities),
                "medium_count": len(analysis_result.medium_vulnerabilities),
                "low_count": len(analysis_result.low_vulnerabilities),
                "security_score": analysis_result.security_score,
                "vulnerabilities": [
                    {
                        "cve_id": v.cve_id,
                        "severity": v.severity,
                        "package_name": v.package_name,
                        "installed_version": v.installed_version,
                        "fixed_version": v.fixed_version,
                        "description": v.description,
                        "cvss_score": v.cvss_score,
                        "published_date": v.published_date,
                        "references": v.references
                    }
                    for v in (analysis_result.critical_vulnerabilities + 
                             analysis_result.high_vulnerabilities + 
                             analysis_result.medium_vulnerabilities + 
                             analysis_result.low_vulnerabilities)
                ],
                "recommendations": analysis_result.actionable_recommendations
            },
            
            # Educational Insights
            "learning_insights": analysis_result.learning_insights,
            
            # Best Practices Analysis
            "best_practices": [
                {
                    "category": bp.category,
                    "title": bp.title,
                    "description": bp.description,
                    "impact": bp.impact,
                    "recommendation": bp.recommendation,
                    "example": bp.example,
                    "priority": bp.priority
                }
                for bp in analysis_result.best_practices
            ],
            
            # Industry Comparison
            "industry_benchmark": analysis_result.industry_comparison,
            
            # Docker Analysis (Real data from image inspection)
            "docker_analysis": await _get_docker_analysis_data(request.image_name),
            
            # Performance Analysis (Real metrics)
            "performance_analysis": await _get_performance_analysis(request.image_name),
            
            # Enterprise Score
            "enterprise_score": analysis_result.security_score
        }
        
        return response_data
        
    except Exception as e:
        return {
            "error": str(e), 
            "analysis_id": analysis_id,
            "status": "failed",
            "timestamp": datetime.utcnow().isoformat()
        }

@app.post("/api/v1/analyze/dockerfile")
async def analyze_dockerfile(file: UploadFile = File(...)):
    """Analyze any uploaded file as a Dockerfile (robust, filename does not matter)"""
    analysis_id = str(uuid.uuid4())
    image_name = f"analyzer-{analysis_id}"
    dockerfile_path = f"uploads/{analysis_id}_Dockerfile"
    try:
        if not file.filename:
            return {"error": "Please upload a file to be used as a Dockerfile.", "analysis_id": analysis_id}
        # Save uploaded file as Dockerfile
        with open(dockerfile_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        # Build image from Dockerfile
        build_success, build_error = await docker_utils.build_image(dockerfile_path, image_name)
        if not build_success:
            return {
                "error": f"Failed to build image from Dockerfile. Details: {build_error}",
                "analysis_id": analysis_id,
                "status": "failed"
            }
        # Ensure image exists
        image_exists = await docker_utils.image_exists(image_name)
        if not image_exists:
            return {
                "error": f"Image '{image_name}' not found after build. Build may have failed.",
                "analysis_id": analysis_id,
                "status": "failed"
            }
        # Analyze the built image
        try:
            analysis_result = await trivy_analyzer.analyze_image_educational(image_name)
        except Exception as e:
            await docker_utils.remove_image(image_name)
            return {
                "error": f"Trivy scan failed: {str(e)}",
                "analysis_id": analysis_id,
                "status": "failed"
            }
        # If no vulnerabilities and score is 100, warn user
        if analysis_result.total_vulnerabilities == 0 or analysis_result.security_score == 100.0:
            await docker_utils.remove_image(image_name)
            return {
                "error": "No vulnerabilities found or scan returned empty. This may indicate a scan or build issue. Please check your Dockerfile and try again.",
                "analysis_id": analysis_id,
                "status": "failed"
            }
        # Parse Dockerfile for additional insights
        dockerfile_insights = await _analyze_dockerfile_content(dockerfile_path)
        # Clean up image after analysis
        await docker_utils.remove_image(image_name)
        # Combine results
        response_data = {
            "analysis_id": analysis_id,
            "image_name": image_name,
            "status": "completed",
            "timestamp": analysis_result.scan_timestamp.isoformat(),
            # Security Analysis (Real Trivy Data)
            "security_analysis": {
                "total_vulnerabilities": analysis_result.total_vulnerabilities,
                "critical_count": len(analysis_result.critical_vulnerabilities),
                "high_count": len(analysis_result.high_vulnerabilities),
                "medium_count": len(analysis_result.medium_vulnerabilities),
                "low_count": len(analysis_result.low_vulnerabilities),
                "security_score": analysis_result.security_score,
                "vulnerabilities": [
                    {
                        "cve_id": v.cve_id,
                        "severity": v.severity,
                        "package_name": v.package_name,
                        "installed_version": v.installed_version,
                        "fixed_version": v.fixed_version,
                        "description": v.description,
                        "cvss_score": v.cvss_score
                    }
                    for v in (analysis_result.critical_vulnerabilities + 
                             analysis_result.high_vulnerabilities + 
                             analysis_result.medium_vulnerabilities + 
                             analysis_result.low_vulnerabilities)
                ],
                "recommendations": analysis_result.actionable_recommendations
            },
            # Dockerfile Analysis
            "dockerfile_analysis": dockerfile_insights,
            # Educational Insights
            "learning_insights": analysis_result.learning_insights + dockerfile_insights.get('insights', []),
            # Best Practices
            "best_practices": [
                {
                    "category": bp.category,
                    "title": bp.title,
                    "description": bp.description,
                    "impact": bp.impact,
                    "recommendation": bp.recommendation,
                    "example": bp.example,
                    "priority": bp.priority
                }
                for bp in analysis_result.best_practices
            ],
            # Industry Comparison
            "industry_benchmark": analysis_result.industry_comparison,
            # Enterprise Score
            "enterprise_score": analysis_result.security_score
        }
        return response_data
    except Exception as e:
        await docker_utils.remove_image(image_name)
        return {
            "error": str(e),
            "analysis_id": analysis_id,
            "status": "failed",
            "timestamp": datetime.utcnow().isoformat()
        }

async def _get_docker_analysis_data(image_name: str) -> dict:
    """Get real Docker analysis data"""
    try:
        image = docker_utils.docker_client.images.get(image_name)
        config = image.attrs.get('Config', {})
        
        return {
            "total_size": image.attrs.get('Size', 0),
            "layer_count": len(image.history()),
            "base_image": image.attrs.get('RepoTags', ['unknown'])[0] if image.attrs.get('RepoTags') else 'unknown',
            "user_configuration": config.get('User', 'root'),
            "exposed_ports": list(config.get('ExposedPorts', {}).keys()),
            "environment_vars": config.get('Env', []),
            "working_dir": config.get('WorkingDir', '/'),
            "entrypoint": config.get('Entrypoint', []),
            "cmd": config.get('Cmd', [])
        }
    except Exception as e:
        return {"error": f"Could not analyze Docker image: {str(e)}"}

async def _get_performance_analysis(image_name: str) -> dict:
    """Get real performance analysis data"""
    try:
        # Get image size
        image = docker_utils.docker_client.images.get(image_name)
        size_mb = image.attrs.get('Size', 0) / (1024 * 1024)
        
        # Performance score based on size
        if size_mb < 100:
            score = 90
        elif size_mb < 300:
            score = 70
        elif size_mb < 500:
            score = 50
        else:
            score = 30
        
        return {
            "image_size_mb": round(size_mb, 2),
            "performance_score": score,
            "recommendations": [
                "Use multi-stage builds to reduce image size",
                "Use .dockerignore to exclude unnecessary files",
                "Consider using alpine-based images"
            ] if size_mb > 300 else ["Image size is reasonable"]
        }
    except Exception as e:
        return {"error": f"Could not analyze performance: {str(e)}"}

async def _analyze_dockerfile_content(dockerfile_path: str) -> dict:
    """Analyze Dockerfile content for educational insights"""
    insights = []
    recommendations = []
    
    try:
        with open(dockerfile_path, 'r') as f:
            lines = f.readlines()
        
        user_config = 'root'
        run_count = 0
        copy_dot = False
        apt_install = False
        multi_stage = False
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            instr = line.split()[0].upper()
            
            if instr == 'USER':
                user_config = line.split()[1] if len(line.split()) > 1 else 'root'
            
            if instr == 'RUN':
                run_count += 1
                if 'apt-get install' in line.lower():
                    apt_install = True
                    if 'clean' not in line.lower():
                        insights.append("🔧 Missing apt-get clean - this increases image size")
                        recommendations.append("Add 'apt-get clean && rm -rf /var/lib/apt/lists/*' after package installation")
            
            if instr == 'COPY' and '. .' in line:
                copy_dot = True
                insights.append("📁 Copying entire context - consider using .dockerignore")
                recommendations.append("Use .dockerignore to exclude unnecessary files")
            
            if instr == 'FROM' and i > 0:
                multi_stage = True
        
        if user_config == 'root':
            insights.append("🔒 Running as root user - security risk")
            recommendations.append("Create a non-root user: RUN groupadd -r appuser && useradd -r -g appuser appuser")
        
        if run_count > 3:
            insights.append("📦 Multiple RUN commands - consider combining to reduce layers")
            recommendations.append("Combine RUN commands to reduce the number of layers")
        
        if not multi_stage:
            insights.append("🏗️ Single-stage build - consider multi-stage for optimization")
            recommendations.append("Use multi-stage builds to reduce final image size")
        
        return {
            "insights": insights,
            "recommendations": recommendations,
            "statistics": {
                "total_instructions": len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
                "run_commands": run_count,
                "user_config": user_config,
                "has_copy_dot": copy_dot,
                "has_apt_install": apt_install,
                "is_multi_stage": multi_stage
            }
        }
        
    except Exception as e:
        return {"error": f"Could not analyze Dockerfile: {str(e)}"}

@app.websocket("/ws/analysis/{analysis_id}")
async def websocket_endpoint(websocket: WebSocket, analysis_id: str):
    """Real-time analysis progress updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Send progress updates
            progress = await get_analysis_progress(analysis_id)
            await websocket.send_json({
                "type": "progress",
                "data": progress
            })
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.get("/api/v1/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """Get analysis result by ID"""
    return await get_analysis_result(analysis_id)

@app.get("/api/v1/compare")
async def compare_images(image1: str, image2: str):
    """Compare two Docker images"""
    try:
        analysis1 = await trivy_analyzer.analyze_image_educational(image1)
        analysis2 = await trivy_analyzer.analyze_image_educational(image2)
        
        return await compare_analyses(analysis1, analysis2)
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/v1/test")
async def test_endpoint():
    """Test endpoint"""
    return {
        "status": "healthy",
        "trivy_available": trivy_analyzer.trivy_available,
        "timestamp": datetime.utcnow().isoformat()
    }

async def get_analysis_progress(analysis_id: str):
    """Get analysis progress"""
    return {
        "analysis_id": analysis_id,
        "progress": 100,
        "status": "completed"
    }

async def get_analysis_result(analysis_id: str):
    """Get analysis result"""
    return {
        "analysis_id": analysis_id,
        "status": "completed"
    }

async def compare_analyses(analysis1, analysis2):
    """Compare two analyses"""
    return {
        "image1": {
            "name": analysis1.image_name,
            "vulnerabilities": analysis1.total_vulnerabilities,
            "security_score": analysis1.security_score
        },
        "image2": {
            "name": analysis2.image_name,
            "vulnerabilities": analysis2.total_vulnerabilities,
            "security_score": analysis2.security_score
        },
        "comparison": {
            "vulnerability_difference": analysis1.total_vulnerabilities - analysis2.total_vulnerabilities,
            "score_difference": analysis1.security_score - analysis2.security_score,
            "recommendation": "Choose the image with fewer vulnerabilities and higher security score"
        }
    }

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 