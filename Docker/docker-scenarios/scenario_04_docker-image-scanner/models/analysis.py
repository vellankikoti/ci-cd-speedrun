#!/usr/bin/env python3
"""
Analysis Models
Data models for Docker image analysis requests and results
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class AnalysisRequest(BaseModel):
    """Analysis request model"""
    image_name: str
    analysis_type: str = "comprehensive"  # comprehensive, security, performance, industry

class AnalysisResult(BaseModel):
    """Analysis result model"""
    analysis_id: str
    image_name: str
    docker_analysis: Dict[str, Any]
    security_analysis: Dict[str, Any]
    performance_analysis: Dict[str, Any]
    industry_benchmark: Dict[str, Any]
    enterprise_score: float
    timestamp: datetime
    status: str = "completed"
    error: Optional[str] = None

class LayerAnalysisModel(BaseModel):
    """Layer analysis model"""
    layer_id: str
    size: int
    commands: List[str]
    efficiency_score: float
    optimization_opportunities: List[str]
    cache_impact: str

class SecurityAnalysisModel(BaseModel):
    """Security analysis model"""
    vulnerabilities: List[Dict[str, Any]]
    total_vulnerabilities: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    security_score: float
    recommendations: List[str]

class PerformanceAnalysisModel(BaseModel):
    """Performance analysis model"""
    build_time: float
    startup_time: float
    memory_usage: int
    cpu_usage: float
    disk_usage: int
    network_usage: Dict[str, Any]
    score: float
    recommendations: List[str]

class IndustryBenchmarkModel(BaseModel):
    """Industry benchmark model"""
    avg_size: int
    avg_layers: int
    avg_score: float
    best_practices: List[str]
    popular_images: List[str]
    percentile: float
    recommendations: List[str] 