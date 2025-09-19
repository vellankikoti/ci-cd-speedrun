# TestContainers Integration

Integration testing with TestContainers

## Overview

This scenario demonstrates integration testing with testcontainers in a Jenkins pipeline.

## Files

- `Jenkinsfile` - Jenkins pipeline definition
- `Dockerfile` - Docker container definition
- `requirements.txt` - Python dependencies
- `tests/` - Test files directory

## Usage

1. Create a new Jenkins job
2. Point to this directory as the source
3. Run the pipeline

## Testing

Run tests locally:
```bash
python -m pytest tests/ -v
```

## Docker

Build and run locally:
```bash
docker build -t 02-testcontainers .
docker run 02-testcontainers
```
