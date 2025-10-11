#!/usr/bin/env python3
"""
Simple Voting App Deployer
Builds Docker image locally and deploys to Kubernetes
Works with Minikube, Kind, Docker Desktop
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(cmd, description, check=True):
    """Run a command and print output"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"$ {cmd}\n")

    result = subprocess.run(cmd, shell=True, capture_output=False, text=True)

    if check and result.returncode != 0:
        print(f"\n❌ Failed: {description}")
        if "docker build" in cmd:
            print("\n💡 Troubleshooting:")
            print("  1. Make sure Docker is running")
            print("  2. Check if you have internet connection")
            print("  3. Try: docker pull python:3.11-slim")
        return False

    print(f"\n✅ Success: {description}")
    return True

def detect_environment():
    """Detect Kubernetes environment"""
    print("\n🔍 Detecting Kubernetes environment...")

    # Check if minikube
    result = subprocess.run("kubectl config current-context",
                          shell=True, capture_output=True, text=True)
    context = result.stdout.strip()

    if "minikube" in context:
        print("✅ Detected: Minikube")
        return "minikube"
    elif "docker-desktop" in context:
        print("✅ Detected: Docker Desktop")
        return "docker-desktop"
    elif "kind" in context:
        print("✅ Detected: Kind")
        return "kind"
    else:
        print(f"✅ Detected: {context}")
        return "unknown"

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║  🗳️  SIMPLE VOTING APP - WFH vs WFO                       ║
║  One Command Deployment - Actually Works!                  ║
╚════════════════════════════════════════════════════════════╝
""")

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Detect environment
    env = detect_environment()

    # Step 1: Build Docker image
    image_name = "simple-vote-app:latest"

    if env == "minikube":
        print("\n📦 Building image inside Minikube...")
        if not run_command(
            "eval $(minikube docker-env) && docker build -t " + image_name + " .",
            "Build Docker image in Minikube"
        ):
            print("\n💡 Alternative: Try building locally first")
            if not run_command(f"docker build -t {image_name} .", "Build Docker image locally"):
                return False
    else:
        if not run_command(f"docker build -t {image_name} .", "Build Docker image"):
            return False

    # Step 2: Update k8s manifest with image name
    print("\n📝 Updating Kubernetes manifest...")
    with open('k8s-manifests.yaml', 'r') as f:
        manifest = f.read()

    manifest = manifest.replace('YOUR_DOCKER_IMAGE_HERE', image_name)
    manifest = manifest.replace('imagePullPolicy: Always', 'imagePullPolicy: IfNotPresent')

    # Add imagePullPolicy if not present
    if 'imagePullPolicy' not in manifest:
        manifest = manifest.replace(
            f'image: {image_name}',
            f'image: {image_name}\n        imagePullPolicy: IfNotPresent'
        )

    with open('k8s-manifests-updated.yaml', 'w') as f:
        f.write(manifest)

    print("✅ Manifest updated")

    # Step 3: Deploy to Kubernetes
    if not run_command(
        "kubectl apply -f k8s-manifests-updated.yaml",
        "Deploy to Kubernetes"
    ):
        return False

    # Step 4: Wait for pods to be ready
    print("\n⏳ Waiting for pods to be ready...")
    for i in range(30):
        result = subprocess.run(
            "kubectl get pods -n voting-app -o jsonpath='{.items[*].status.phase}'",
            shell=True, capture_output=True, text=True
        )

        if result.returncode == 0:
            phases = result.stdout.strip().split()
            if phases and all(p == 'Running' for p in phases):
                print("\n✅ All pods are running!")
                break

        print(f"   Attempt {i+1}/30: Waiting...")
        time.sleep(5)

    # Step 5: Get access information
    print(f"\n{'='*60}")
    print("🎉 DEPLOYMENT COMPLETE!")
    print(f"{'='*60}\n")

    # Get NodePort
    result = subprocess.run(
        "kubectl get svc vote-app -n voting-app -o jsonpath='{.spec.ports[0].nodePort}'",
        shell=True, capture_output=True, text=True
    )
    node_port = result.stdout.strip() or "31000"

    print("🌐 ACCESS YOUR VOTING APP:\n")

    if env == "minikube":
        result = subprocess.run("minikube ip", shell=True, capture_output=True, text=True)
        minikube_ip = result.stdout.strip()
        print(f"   🎯 Direct URL: http://{minikube_ip}:{node_port}")
        print(f"   🔧 Or run: minikube service vote-app -n voting-app")
    elif env == "docker-desktop":
        print(f"   🎯 URL: http://localhost:{node_port}")
    else:
        print(f"   🎯 URL: http://localhost:{node_port}")
        print(f"   🔧 Or port-forward: kubectl port-forward -n voting-app svc/vote-app 8080:80")
        print(f"      Then open: http://localhost:8080")

    print("\n📊 VERIFY DEPLOYMENT:\n")
    print("   kubectl get all -n voting-app")
    print("   kubectl logs -n voting-app -l app=vote-app -f")

    print("\n🎮 HOW TO USE:\n")
    print("   1. Open the URL in your browser")
    print("   2. Click 🏠 WFH or 🏢 WFO to vote")
    print("   3. Watch the results update in real-time!")
    print("   4. Open multiple tabs and vote - all votes are counted")

    print("\n🧹 CLEANUP WHEN DONE:\n")
    print("   kubectl delete namespace voting-app")

    print(f"\n{'='*60}")
    print("✅ Everything is ready! Open the URL and start voting!")
    print(f"{'='*60}\n")

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
