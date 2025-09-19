# HTML Test Reports

Generate beautiful HTML test reports

## Overview

This scenario demonstrates generate beautiful html test reports in a Jenkins pipeline.

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
docker build -t 03-html-reports .
docker run 03-html-reports
```
