from flask import Flask, request, jsonify
from kubernetes import client, config
import os
import random
import time
import threading

app = Flask(__name__)

NAMESPACE = os.environ.get('K8S_NAMESPACE', 'scaling-challenge')
BLUE_DEPLOY = 'blue-deployment'
GREEN_DEPLOY = 'green-deployment'

# Load K8s config (in-cluster or local)
try:
    config.load_incluster_config()
except:
    config.load_kube_config()
apps_v1 = client.AppsV1Api()
core_v1 = client.CoreV1Api()

# Track deployment state
deployment_state = {
    'current_strategy': 'blue-green',
    'blue_pods': 5,
    'green_pods': 5,
    'last_deployment_time': None
}

# Initialize deployments if they don't exist
def ensure_deployments_exist():
    try:
        # Check if blue deployment exists and has replicas
        blue_deploy = apps_v1.read_namespaced_deployment(BLUE_DEPLOY, NAMESPACE)
        if blue_deploy.spec.replicas == 0:
            # Reset to 5 replicas if it's at 0
            apps_v1.patch_namespaced_deployment_scale(BLUE_DEPLOY, NAMESPACE, {'spec': {'replicas': 5}})
            deployment_state['blue_pods'] = 5
    except Exception as e:
        print(f"Blue deployment not found or error: {e}")
    
    try:
        # Check if green deployment exists and has replicas
        green_deploy = apps_v1.read_namespaced_deployment(GREEN_DEPLOY, NAMESPACE)
        if green_deploy.spec.replicas == 0:
            # Reset to 5 replicas if it's at 0
            apps_v1.patch_namespaced_deployment_scale(GREEN_DEPLOY, NAMESPACE, {'spec': {'replicas': 5}})
            deployment_state['green_pods'] = 5
    except Exception as e:
        print(f"Green deployment not found or error: {e}")

# Ensure deployments exist on startup
ensure_deployments_exist()

@app.route('/api/pods')
def get_pods():
    pods = []
    try:
        # Get all pods with app=demo-app label (includes blue, green, backend, frontend)
        k8s_pods = core_v1.list_namespaced_pod(NAMESPACE, label_selector='app=demo-app')
        
        for pod in k8s_pods.items:
            version = pod.metadata.labels.get('version', 'unknown')
            name = pod.metadata.name
            status = pod.status.phase
            
            # Only include blue and green pods for the demo
            if version in ['blue', 'green']:
                # Enhanced health simulation
                annotations = pod.metadata.annotations or {}
                if annotations.get('chaos/kill') == 'true':
                    health = 'unhealthy'
                elif status == 'Pending':
                    health = 'pending'
                elif status == 'Running':
                    # 95% healthy for running pods
                    health = 'healthy' if random.random() > 0.05 else 'unhealthy'
                else:
                    health = 'unhealthy'
                
                pods.append({
                    'name': name,
                    'version': version,
                    'health': health,
                    'status': status,
                    'created': pod.metadata.creation_timestamp.isoformat() if pod.metadata.creation_timestamp else None
                })
    except Exception as e:
        print(f"Error getting pods: {e}")
        # Fallback to simulated pods if K8s is not available
        pods = generate_simulated_pods()
    
    return jsonify(pods)

def generate_simulated_pods():
    """Generate simulated pods for demo purposes"""
    pods = []
    blue_count = deployment_state['blue_pods']
    green_count = deployment_state['green_pods']
    
    for i in range(blue_count):
        pods.append({
            'name': f'blue-pod-{i+1}',
            'version': 'blue',
            'health': 'healthy' if random.random() > 0.1 else 'unhealthy',
            'status': 'Running',
            'created': time.time()
        })
    
    for i in range(green_count):
        pods.append({
            'name': f'green-pod-{i+1}',
            'version': 'green',
            'health': 'healthy' if random.random() > 0.1 else 'unhealthy',
            'status': 'Running',
            'created': time.time()
        })
    
    return pods

@app.route('/api/deploy', methods=['POST'])
def deploy():
    data = request.json
    strategy = data.get('strategy', 'blue-green')
    
    try:
        if strategy == 'blue-green':
            # Switch all pods to green
            deployment_state['blue_pods'] = 0
            deployment_state['green_pods'] = 10
            deployment_state['current_strategy'] = 'blue-green'
            
            # Scale actual deployments
            apps_v1.patch_namespaced_deployment_scale(
                BLUE_DEPLOY, NAMESPACE, 
                {'spec': {'replicas': 0}}
            )
            apps_v1.patch_namespaced_deployment_scale(
                GREEN_DEPLOY, NAMESPACE, 
                {'spec': {'replicas': 10}}
            )
            
        elif strategy == 'rollout':
            # Progressive rollout: gradually replace blue with green
            deployment_state['blue_pods'] = 3
            deployment_state['green_pods'] = 7
            deployment_state['current_strategy'] = 'rollout'
            
            # Scale actual deployments
            apps_v1.patch_namespaced_deployment_scale(
                BLUE_DEPLOY, NAMESPACE, 
                {'spec': {'replicas': 3}}
            )
            apps_v1.patch_namespaced_deployment_scale(
                GREEN_DEPLOY, NAMESPACE, 
                {'spec': {'replicas': 7}}
            )
            
        elif strategy == 'canary':
            # Canary: small percentage of green pods
            deployment_state['blue_pods'] = 8
            deployment_state['green_pods'] = 2
            deployment_state['current_strategy'] = 'canary'
            
            # Scale actual deployments
            apps_v1.patch_namespaced_deployment_scale(
                BLUE_DEPLOY, NAMESPACE, 
                {'spec': {'replicas': 8}}
            )
            apps_v1.patch_namespaced_deployment_scale(
                GREEN_DEPLOY, NAMESPACE, 
                {'spec': {'replicas': 2}}
            )
            
        deployment_state['last_deployment_time'] = time.time()
            
        return jsonify({
            'status': 'success',
            'strategy': strategy,
            'blue_pods': deployment_state['blue_pods'],
            'green_pods': deployment_state['green_pods']
        })
        
    except Exception as e:
        print(f"Error in deploy: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/rollout', methods=['POST'])
def rollout():
    data = request.json
    percent = int(data.get('percent', 100))
    total = 10  # For demo, assume 10 pods
    green_count = int(total * percent / 100)
    blue_count = total - green_count
    
    try:
        # Update deployment state
        deployment_state['blue_pods'] = blue_count
        deployment_state['green_pods'] = green_count
        deployment_state['current_strategy'] = 'rollout'
        deployment_state['last_deployment_time'] = time.time()
        
        # Patch deployments
        apps_v1.patch_namespaced_deployment_scale(BLUE_DEPLOY, NAMESPACE, {'spec': {'replicas': blue_count}})
        apps_v1.patch_namespaced_deployment_scale(GREEN_DEPLOY, NAMESPACE, {'spec': {'replicas': green_count}})
        return jsonify({'status': 'ok', 'blue': blue_count, 'green': green_count})
    except Exception as e:
        print(f"Error in rollout: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/kill-pod', methods=['POST'])
def kill_pod():
    data = request.json
    pod_name = data.get('name')
    if not pod_name:
        return jsonify({'error': 'No pod name provided'}), 400
    
    try:
        # Actually delete the pod - Kubernetes will recreate it automatically
        print(f"Deleting pod: {pod_name}")
        core_v1.delete_namespaced_pod(pod_name, NAMESPACE)
        
        return jsonify({'status': 'killed', 'pod': pod_name})
    except Exception as e:
        print(f"Error killing pod: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def get_status():
    """Get current deployment status"""
    try:
        # Get actual deployment status
        blue_deploy = apps_v1.read_namespaced_deployment(BLUE_DEPLOY, NAMESPACE)
        green_deploy = apps_v1.read_namespaced_deployment(GREEN_DEPLOY, NAMESPACE)
        
        return jsonify({
            'current_strategy': deployment_state['current_strategy'],
            'blue_pods': blue_deploy.spec.replicas,
            'green_pods': green_deploy.spec.replicas,
            'last_deployment_time': deployment_state['last_deployment_time']
        })
    except Exception as e:
        print(f"Error getting status: {e}")
        return jsonify({
            'current_strategy': deployment_state['current_strategy'],
            'blue_pods': deployment_state['blue_pods'],
            'green_pods': deployment_state['green_pods'],
            'last_deployment_time': deployment_state['last_deployment_time']
        })

@app.route('/api/reset', methods=['POST'])
def reset_deployment():
    """Reset to initial state: 5 blue, 5 green"""
    try:
        deployment_state['blue_pods'] = 5
        deployment_state['green_pods'] = 5
        deployment_state['current_strategy'] = 'blue-green'
        deployment_state['last_deployment_time'] = time.time()
        
        # Update actual K8s deployments
        apps_v1.patch_namespaced_deployment_scale(BLUE_DEPLOY, NAMESPACE, {'spec': {'replicas': 5}})
        apps_v1.patch_namespaced_deployment_scale(GREEN_DEPLOY, NAMESPACE, {'spec': {'replicas': 5}})
        
        # Wait a moment for the scaling to take effect
        time.sleep(1)
            
        return jsonify({'status': 'reset', 'blue': 5, 'green': 5})
    except Exception as e:
        print(f"Error in reset: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 