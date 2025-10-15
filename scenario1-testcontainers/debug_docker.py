#!/usr/bin/env python3
"""Debug Docker detection in Codespaces"""
import subprocess
import os

print("🔍 Debugging Docker Detection\n")

# Check if we're in Codespaces
if os.getenv('CODESPACES'):
    print("✅ Running in Codespaces")
else:
    print("⚠️  NOT in Codespaces")

print(f"Platform: {os.uname().sysname}\n")

# Test which command
print("1️⃣ Testing 'which docker':")
try:
    result = subprocess.run(['which', 'docker'], capture_output=True, text=True, timeout=2)
    print(f"   Return code: {result.returncode}")
    if result.returncode == 0:
        print(f"   ✅ Found at: {result.stdout.strip()}")
    else:
        print(f"   ❌ Not found")
        print(f"   stderr: {result.stderr}")
except Exception as e:
    print(f"   ❌ Exception: {e}")

print()

# Check all paths
print("2️⃣ Checking paths:")
paths = [
    '/usr/local/bin/docker',
    '/usr/bin/docker',
    '/usr/local/bin/docker-compose',
    '/bin/docker',
    '/opt/homebrew/bin/docker'
]

for path in paths:
    exists = os.path.exists(path)
    print(f"   {'✅' if exists else '❌'} {path}")

print()

# Check docker command directly
print("3️⃣ Running docker command directly:")
docker_cmds = [
    ['docker', '--version'],
    ['/usr/local/bin/docker', '--version'],
    ['/usr/bin/docker', '--version']
]

for cmd in docker_cmds:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            print(f"   ✅ {' '.join(cmd)}: {result.stdout.strip()}")
        else:
            print(f"   ❌ {' '.join(cmd)}: Failed (rc={result.returncode})")
    except FileNotFoundError:
        print(f"   ❌ {' '.join(cmd)}: Not found")
    except Exception as e:
        print(f"   ❌ {' '.join(cmd)}: {e}")

print()

# Check PATH
print("4️⃣ PATH environment:")
path_env = os.environ.get('PATH', '')
for p in path_env.split(':')[:10]:
    print(f"   • {p}")

print("\n5️⃣ Docker socket:")
socket_paths = [
    '/var/run/docker.sock',
    '/run/docker.sock'
]
for sock in socket_paths:
    exists = os.path.exists(sock)
    print(f"   {'✅' if exists else '❌'} {sock}")
