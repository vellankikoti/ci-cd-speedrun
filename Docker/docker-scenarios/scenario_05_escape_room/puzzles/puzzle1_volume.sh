#!/bin/bash

# Puzzle 1: The Secret Vault (Volumes)
# Dr. NullPointer has hidden the escape key in a Docker volume

echo "🔐 Setting up Puzzle 1: The Secret Vault"
echo "Dr. NullPointer is creating a secret volume..."

# Clean up any existing volume
docker volume rm vault-volume 2>/dev/null || true

# Create the secret volume
docker volume create vault-volume

# Hide the secret code in the volume
docker run --rm -v vault-volume:/mnt busybox sh -c "
mkdir -p /mnt/secret
echo 'escape123' > /mnt/secret/code.txt
echo 'Secret code hidden successfully!' > /mnt/secret/note.txt
"

echo "✅ Puzzle 1 setup complete!"
echo "📝 The secret code is hidden in vault-volume at /secret/code.txt"
echo "💡 Use: docker run --rm -v vault-volume:/mnt busybox cat /mnt/secret/code.txt" 