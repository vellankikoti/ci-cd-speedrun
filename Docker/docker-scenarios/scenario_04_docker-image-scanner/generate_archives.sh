#!/bin/bash
set -e

# Check for rar and install if missing (Linux only)
if ! command -v rar >/dev/null 2>&1; then
  echo "rar not found. Attempting install..."
  if [[ "$(uname)" == "Linux" ]]; then
    sudo apt-get update && sudo apt-get install -y rar || echo "Could not install rar, skipping rar archives."
  else
    echo "Please install rar manually if you want rar archives."
  fi
fi

# Clean up any old test dirs
rm -rf test_archives
mkdir test_archives
cd test_archives

echo "Creating example folders..."

###########################
# Example 1 - Python Flask
###########################
mkdir example1
cat > example1/Dockerfile <<EOF
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
EOF
echo "flask" > example1/requirements.txt
echo "print('Hello from Flask app!')" > example1/app.py

############################
# Example 2 - Node.js App
############################
mkdir example2
cat > example2/Dockerfile <<EOF
FROM node:18-alpine
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["node", "index.js"]
EOF
echo '{ "name": "test", "dependencies": { "express": "^4.18.2" } }' > example2/package.json
echo "console.log('Hello from Node.js!')" > example2/index.js

#############################
# Example 3 - Nginx Static
#############################
mkdir -p example3/site-content
cat > example3/Dockerfile <<EOF
FROM nginx:alpine
COPY ./site-content /usr/share/nginx/html
EXPOSE 80
EOF
echo "<h1>Hello from Nginx!</h1>" > example3/site-content/index.html

################################
# Example 4 - Java Spring Boot
################################
mkdir example4
cat > example4/Dockerfile <<EOF
FROM openjdk:17-jdk-slim
WORKDIR /app
COPY target/app.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
EOF
mkdir -p example4/target
echo "dummy jar content" > example4/target/app.jar

##############################
# Example 5 - Go Application
##############################
mkdir example5
cat > example5/Dockerfile <<EOF
FROM golang:1.21-alpine AS builder
WORKDIR /src
COPY . .
RUN go build -o app main.go

FROM alpine:3.18
WORKDIR /app
COPY --from=builder /src/app .
CMD ["./app"]
EOF
echo 'package main; import "fmt"; func main() { fmt.Println("Hello from Go!") }' > example5/main.go

echo "Creating archives..."

# Create 2 .zip files
zip -r example1.zip example1
zip -r example2.zip example2

# Create 2 .tar files
tar -cf example3.tar example3
tar -cf example4.tar example4

# Create 2 .tar.gz files
tar -czf example5.tar.gz example5
tar -czf example1_copy.tar.gz example1

# Create 2 .gz files (compress single files)
echo "This is a test file for gzip #1" > file1.txt
echo "This is a test file for gzip #2" > file2.txt
gzip -c file1.txt > file1.txt.gz
gzip -c file2.txt > file2.txt.gz

# Create 2 .rar files if rar installed
if command -v rar >/dev/null 2>&1; then
  rar a example2.rar example2
  rar a example5.rar example5
else
  echo "rar not installed, skipping .rar archives"
fi

echo "Done. Archives created in test_archives/:"
ls -lh *.zip *.tar *.tar.gz *.gz *.rar 2>/dev/null || true

