#!/bin/bash
set -e

rm -rf simple_dockerfiles
mkdir simple_dockerfiles
cd simple_dockerfiles

# 1. Alpine echo
cat > Dockerfile1 <<EOF
FROM alpine:3.18
CMD ["echo", "Hello from Alpine!"]
EOF

# 2. Ubuntu version
cat > Dockerfile2 <<EOF
FROM ubuntu:22.04
CMD ["bash", "-c", "echo Hello from Ubuntu! && cat /etc/os-release"]
EOF

# 3. Nginx default
cat > Dockerfile3 <<EOF
FROM nginx:alpine
EXPOSE 80
EOF

# 4. Busybox sleep
cat > Dockerfile4 <<EOF
FROM busybox
CMD ["sleep", "10"]
EOF

# 5. Debian print date
cat > Dockerfile5 <<EOF
FROM debian:stable-slim
CMD ["date"]
EOF

echo "Generated 5 simple Dockerfiles in simple_dockerfiles/:"
ls -l
