#!/bin/bash

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Build the documentation
mkdocs build

# Serve the built site (for Render)
echo "Starting MkDocs server on port $PORT"
mkdocs serve --dev-addr=0.0.0.0:$PORT --no-livereload 