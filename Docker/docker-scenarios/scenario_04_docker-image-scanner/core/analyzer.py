#!/usr/bin/env python3
"""
Enterprise Docker Analyzer
Real Docker API integration for comprehensive image analysis
"""

import docker
import asyncio
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class LayerAnalysis:
    """Individual layer analysis result"""
    layer_id: str
    size: int
    commands: List[str]
    efficiency_score: float
    optimization_opportunities: List[str]
    cache_impact: str

@dataclass
class DockerAnalysisResult:
    """Comprehensive Docker analysis result"""
    image_name: str
    total_size: int
    layer_count: int
    layers: List[LayerAnalysis]
    base_image: str
    user_configuration: str
    network_config: Dict[str, Any]
    environment_vars: List[str]
    exposed_ports: List[int]
    volume_mounts: List[str]
    overall_score: float
    recommendations: List[str]

class EnterpriseDockerAnalyzer:
    """Enterprise-grade Docker image analyzer using real Docker API"""
    
    def __init__(self):
        self.docker_client = docker.from_env()
        self.analysis_cache = {}
    
    async def analyze_image_enterprise(self, image_name: str) -> DockerAnalysisResult:
        """
        Comprehensive Docker image analysis using real Docker API
        """
        try:
            # Pull image if not local
            await self._ensure_image_available(image_name)
            
            # Get image object
            image = self.docker_client.images.get(image_name)
            
            # Analyze layers with real data
            layers = await self._analyze_layers_enterprise(image)
            
            # Analyze image configuration
            config_analysis = await self._analyze_image_configuration(image)
            
            # Calculate overall score
            overall_score = await self._calculate_overall_score(layers, config_analysis)
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(layers, config_analysis)
            
            return DockerAnalysisResult(
                image_name=image_name,
                total_size=image.attrs['Size'],
                layer_count=len(layers),
                layers=layers,
                base_image=config_analysis['base_image'],
                user_configuration=config_analysis['user_config'],
                network_config=config_analysis['network_config'],
                environment_vars=config_analysis['env_vars'],
                exposed_ports=config_analysis['exposed_ports'],
                volume_mounts=config_analysis['volume_mounts'],
                overall_score=overall_score,
                recommendations=recommendations
            )
            
        except Exception as e:
            raise Exception(f"Failed to analyze image {image_name}: {str(e)}")
    
    async def _ensure_image_available(self, image_name: str):
        """Ensure image is available locally"""
        try:
            self.docker_client.images.get(image_name)
        except docker.errors.ImageNotFound:
            print(f"Pulling image {image_name}...")
            self.docker_client.images.pull(image_name)
    
    async def _analyze_layers_enterprise(self, image) -> List[LayerAnalysis]:
        """Analyze each layer with real Docker data"""
        layers = []
        
        # Get real layer history
        history = image.history()
        
        for i, layer_info in enumerate(history):
            # Extract real layer data
            layer_analysis = await self._analyze_single_layer(layer_info, i)
            layers.append(layer_analysis)
        
        return layers
    
    async def _analyze_single_layer(self, layer_info, layer_index: int) -> LayerAnalysis:
        """Analyze a single layer with real data"""
        
        # Extract commands from layer history
        commands = self._extract_commands_from_layer(layer_info)
        
        # Calculate efficiency score
        efficiency_score = await self._calculate_layer_efficiency(commands, layer_info)
        
        # Identify optimization opportunities
        optimizations = await self._identify_layer_optimizations(commands, layer_info)
        
        # Calculate cache impact
        cache_impact = await self._calculate_cache_impact(commands, layer_index)
        
        return LayerAnalysis(
            layer_id=layer_info.get('Id', f'layer_{layer_index}'),
            size=layer_info.get('Size', 0),
            commands=commands,
            efficiency_score=efficiency_score,
            optimization_opportunities=optimizations,
            cache_impact=cache_impact
        )
    
    def _extract_commands_from_layer(self, layer_info) -> List[str]:
        """Extract actual commands from layer history"""
        commands = []
        
        # Parse the CreatedBy field which contains the actual command
        created_by = layer_info.get('CreatedBy', '')
        
        # Common Docker commands to look for
        docker_commands = [
            'FROM', 'COPY', 'ADD', 'RUN', 'CMD', 'ENTRYPOINT',
            'ENV', 'EXPOSE', 'VOLUME', 'USER', 'WORKDIR', 'ARG'
        ]
        
        for cmd in docker_commands:
            if cmd in created_by:
                commands.append(created_by.strip())
                break
        
        return commands
    
    async def _calculate_layer_efficiency(self, commands: List[str], layer_info) -> float:
        """Calculate layer efficiency score based on real commands"""
        score = 100.0
        
        for command in commands:
            command_lower = command.lower()
            
            # Efficiency penalties based on real Docker best practices
            if 'copy . .' in command_lower:
                score -= 30  # Copying entire context
            elif 'apt-get install' in command_lower and 'clean' not in command_lower:
                score -= 20  # Missing cleanup
            elif 'rm -rf' in command_lower:
                score -= 10  # Manual cleanup needed
            elif 'wget' in command_lower and 'rm' not in command_lower:
                score -= 15  # Downloaded files not cleaned up
            elif 'curl' in command_lower and 'rm' not in command_lower:
                score -= 15  # Downloaded files not cleaned up
        
        # Size-based efficiency
        layer_size = layer_info.get('Size', 0)
        if layer_size > 100 * 1024 * 1024:  # 100MB
            score -= 20
        elif layer_size > 50 * 1024 * 1024:  # 50MB
            score -= 10
        
        return max(0.0, score)
    
    async def _identify_layer_optimizations(self, commands: List[str], layer_info) -> List[str]:
        """Identify real optimization opportunities"""
        optimizations = []
        
        for command in commands:
            command_lower = command.lower()
            
            if 'copy . .' in command_lower:
                optimizations.append("Use .dockerignore and copy specific files instead of entire context")
            
            if 'apt-get install' in command_lower and 'clean' not in command_lower:
                optimizations.append("Add 'apt-get clean && rm -rf /var/lib/apt/lists/*' to reduce image size")
            
            if 'wget' in command_lower and 'rm' not in command_lower:
                optimizations.append("Remove downloaded files after installation to reduce layer size")
            
            if 'curl' in command_lower and 'rm' not in command_lower:
                optimizations.append("Remove downloaded files after installation to reduce layer size")
        
        return optimizations
    
    async def _calculate_cache_impact(self, commands: List[str], layer_index: int) -> str:
        """Calculate cache impact of layer"""
        if layer_index == 0:
            return "Base layer - always cached"
        
        for command in commands:
            if 'COPY' in command or 'ADD' in command:
                return "High cache impact - changes frequently"
            elif 'RUN' in command:
                return "Medium cache impact - depends on command stability"
        
        return "Low cache impact"
    
    async def _analyze_image_configuration(self, image) -> Dict[str, Any]:
        """Analyze image configuration with real data"""
        config = image.attrs.get('Config', {})
        
        return {
            'base_image': image.attrs.get('RepoTags', ['unknown'])[0] if image.attrs.get('RepoTags') else 'unknown',
            'user_config': config.get('User', 'root'),
            'network_config': config.get('NetworkDisabled', False),
            'env_vars': config.get('Env', []),
            'exposed_ports': list(config.get('ExposedPorts', {}).keys()),
            'volume_mounts': config.get('Volumes', {}),
            'working_dir': config.get('WorkingDir', '/'),
            'entrypoint': config.get('Entrypoint', []),
            'cmd': config.get('Cmd', [])
        }
    
    async def _calculate_overall_score(self, layers: List[LayerAnalysis], config: Dict[str, Any]) -> float:
        """Calculate overall Docker image score"""
        score = 100.0
        
        # Layer efficiency score
        avg_layer_efficiency = sum(layer.efficiency_score for layer in layers) / len(layers)
        score = (score + avg_layer_efficiency) / 2
        
        # Configuration penalties
        if config['user_config'] == 'root':
            score -= 15  # Running as root
        
        if not config['exposed_ports']:
            score -= 5  # No exposed ports (might be intentional)
        
        # Size penalties
        total_size = sum(layer.size for layer in layers)
        if total_size > 500 * 1024 * 1024:  # 500MB
            score -= 20
        elif total_size > 200 * 1024 * 1024:  # 200MB
            score -= 10
        
        return max(0.0, score)
    
    async def _generate_recommendations(self, layers: List[LayerAnalysis], config: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Layer-based recommendations
        for layer in layers:
            recommendations.extend(layer.optimization_opportunities)
        
        # Configuration-based recommendations
        if config['user_config'] == 'root':
            recommendations.append("Create a non-root user for better security")
        
        if len(layers) > 10:
            recommendations.append("Consider multi-stage builds to reduce layer count")
        
        # Size-based recommendations
        total_size = sum(layer.size for layer in layers)
        if total_size > 500 * 1024 * 1024:
            recommendations.append("Consider using Alpine Linux or distroless images to reduce size")
        
        return list(set(recommendations))  # Remove duplicates 