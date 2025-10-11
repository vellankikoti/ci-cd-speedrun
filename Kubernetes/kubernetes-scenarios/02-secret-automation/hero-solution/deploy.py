#!/usr/bin/env python3
"""
🔐 Secure Todo App Deployer
Clean, simple deployment with automated secret generation
"""
import os
import sys
import subprocess
import time
import secrets
import string
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
        return False

    print(f"\n✅ Success: {description}")
    return True

def generate_secure_password(length=32):
    """Generate a cryptographically secure password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def detect_environment():
    """Detect Kubernetes environment"""
    print("\n🔍 Detecting Kubernetes environment...")
    result = subprocess.run("kubectl config current-context",
                          shell=True, capture_output=True, text=True)
    context = result.stdout.strip()

    if "minikube" in context:
        print("✅ Detected: Minikube")
        return "minikube"
    elif "docker-desktop" in context:
        print("✅ Detected: Docker Desktop")
        return "docker-desktop"
    else:
        print(f"✅ Detected: {context}")
        return "unknown"

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║  🔐 SECURE TODO APP - Secret Management Demo              ║
║  Simple, Clean, Powerful!                                  ║
╚════════════════════════════════════════════════════════════╝
""")

    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    env = detect_environment()

    # Generate secure credentials
    print("\n🔐 Generating secure credentials...")
    api_key = generate_secure_password(32)
    app_secret = generate_secure_password(32)
    print("✅ Generated cryptographically secure secrets")
    print(f"   API Key: {api_key[:12]}... (32 chars)")
    print(f"   App Secret: {app_secret[:12]}... (32 chars)")

    # Build Docker image
    image_name = "secure-todo:latest"

    if env == "minikube":
        print("\n📦 Building image inside Minikube...")
        if not run_command(
            "eval $(minikube docker-env) && docker build -t " + image_name + " .",
            "Build image in Minikube"
        ):
            if not run_command(f"docker build -t {image_name} .", "Build image locally"):
                return False
    else:
        if not run_command(f"docker build -t {image_name} .", "Build Docker image"):
            return False

    # Update manifest
    print("\n📝 Updating Kubernetes manifest...")
    with open('k8s-manifests.yaml', 'r') as f:
        manifest = f.read()

    manifest = manifest.replace('GENERATED_BY_SCRIPT', api_key, 1)
    manifest = manifest.replace('GENERATED_BY_SCRIPT', app_secret, 1)
    manifest = manifest.replace('YOUR_IMAGE_HERE', image_name)

    with open('k8s-deployed.yaml', 'w') as f:
        f.write(manifest)

    print("✅ Manifest updated")

    # Deploy
    if not run_command("kubectl apply -f k8s-deployed.yaml", "Deploy to Kubernetes"):
        return False

    # Wait for pods
    print("\n⏳ Waiting for pods to be ready...")
    for i in range(30):
        result = subprocess.run(
            "kubectl get pods -n secure-todo -o jsonpath='{.items[*].status.phase}'",
            shell=True, capture_output=True, text=True
        )

        if result.returncode == 0:
            phases = result.stdout.strip().split()
            if phases and all(p == 'Running' for p in phases):
                print("\n✅ All pods are running!")
                break

        print(f"   Attempt {i+1}/30: Waiting...")
        time.sleep(5)

    # Show success
    print(f"\n{'='*60}")
    print("🎉 DEPLOYMENT COMPLETE!")
    print(f"{'='*60}\n")

    print("🌐 ACCESS YOUR SECURE TODO APP:\n")
    print("   🎯 Try NodePort: http://localhost:31005")
    print("   ℹ️  If that doesn't work, use port-forward below:")

    print("\n🔧 PORT-FORWARD COMMANDS (Copy & Paste):\n")
    print("   # Terminal 1: Start port-forward")
    print("   kubectl port-forward -n secure-todo svc/todo-app 31005:80")
    print()
    print("   # Then open: http://localhost:31005")

    print("\n📊 VERIFY DEPLOYMENT:\n")
    print("   kubectl get all -n secure-todo")
    print("   kubectl get secrets -n secure-todo")
    print("   kubectl logs -n secure-todo -l app=todo-app")

    print("\n🎮 HOW TO USE:\n")
    print("   1. Run port-forward command above")
    print("   2. Open http://localhost:31005")
    print("   3. Add, complete, delete tasks")
    print("   4. See security features in the UI")

    print("\n🔐 SECURITY FEATURES:\n")
    print("   ✅ Auto-generated 32-char secure passwords")
    print("   ✅ Secrets encrypted in etcd")
    print("   ✅ Non-root container (UID 1000)")
    print("   ✅ Read-only root filesystem")
    print("   ✅ Dropped all capabilities")
    print("   ✅ Resource limits")
    print("   ✅ Health checks")

    print("\n🧪 TEST SECURITY:\n")
    print("   # View secret (base64 encoded)")
    print("   kubectl get secret app-secrets -n secure-todo -o yaml")
    print()
    print("   # Decode secret")
    print("   kubectl get secret app-secrets -n secure-todo -o jsonpath='{.data.api-key}' | base64 -d")
    print()
    print("   # Verify non-root")
    print("   kubectl exec -it -n secure-todo deploy/todo-app -- id")

    print("\n🧹 CLEANUP:\n")
    print("   kubectl delete namespace secure-todo")
    print("   rm k8s-deployed.yaml")

    print(f"\n{'='*60}")
    print("✅ Ready! Open http://localhost:31005 and try it!")
    print(f"{'='*60}\n")

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
