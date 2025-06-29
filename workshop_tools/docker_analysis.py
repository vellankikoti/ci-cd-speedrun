#!/usr/bin/env python3
import subprocess
import os
import csv
from datetime import datetime
from pathlib import Path

def run_command(cmd):
    """
    Run a shell command and capture stdout.
    """
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def get_image_size(image_tag):
    """
    Return the image size in MB.
    """
    size_bytes = run_command(
        f"docker image inspect {image_tag} --format='{{{{.Size}}}}'"
    )
    if size_bytes.isdigit():
        return round(int(size_bytes) / (1024 * 1024), 2)
    return 0

def save_image_size(image_tag, size_mb):
    """
    Record the size of an image into CSV for tracking.
    """
    csv_path = Path("reports/docker_image_sizes.csv")
    exists = csv_path.exists()
    with open(csv_path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not exists:
            writer.writerow(["timestamp", "image_tag", "size_MB"])
        writer.writerow([datetime.now().isoformat(), image_tag, size_mb])

def save_file(path, contents):
    Path(path).write_text(contents)

def generate_docker_report(version):
    image_tag = f"ci-cd-chaos-app:v{version}"
    version_dir = Path(f"reports/version_{version}")
    version_dir.mkdir(parents=True, exist_ok=True)

    # --- Image size ---
    size_mb = get_image_size(image_tag)
    save_image_size(image_tag, size_mb)

    # --- docker history ---
    history = run_command(f"docker history {image_tag}")
    save_file(version_dir / "docker_history.txt", history)

    # --- SBOM ---
    sbom = run_command(f"docker sbom {image_tag} || echo 'SBOM not supported.'")
    save_file(version_dir / "sbom.txt", sbom)

    # --- Vulnerability scan ---
    scan = run_command(f"docker scan {image_tag} || echo 'Docker scan not supported.'")
    save_file(version_dir / "vulnerabilities.txt", scan)

    # --- HTML Dashboard ---
    html = f"""
    <html>
    <head>
      <style>
        body {{ font-family: sans-serif; background: #1e1e2f; color: #eee; }}
        h1 {{ color: #6cf; }}
        pre {{ background: #333; padding: 1em; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 50%; }}
        td, th {{ border: 1px solid #555; padding: 8px; }}
      </style>
    </head>
    <body>
      <h1>Docker Report - Version {version}</h1>
      <h2>Image Size</h2>
      <p>{size_mb} MB</p>

      <h2>Layer History</h2>
      <pre>{history}</pre>

      <h2>SBOM</h2>
      <pre>{sbom}</pre>

      <h2>Vulnerabilities</h2>
      <pre>{scan}</pre>
    </body>
    </html>
    """
    save_file(version_dir / "docker_report.html", html)
    print(f"✅ Docker report generated for version {version} at {version_dir}/docker_report.html")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python docker_analysis.py <version>")
        sys.exit(1)

    version = sys.argv[1]
    generate_docker_report(version)
