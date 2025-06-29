#!/usr/bin/env python3

import subprocess
import sys
import os
import shutil
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

CHAOS_ASCII = r"""
██████╗  ██████╗ ███████╗██╗     ██████╗ 
██╔══██╗██╔═══██╗██╔════╝██║     ██╔══██╗
██║  ██║██║   ██║███████╗██║     ██║  ██║
██║  ██║██║   ██║╚════██║██║     ██║  ██║
██████╔╝╚██████╔╝███████║███████╗██████╔╝
╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═════╝ 
"""

def print_banner():
    console.print(f"[bold cyan]{CHAOS_ASCII}[/bold cyan]")
    console.print("🐍 Welcome to the CI/CD Chaos Workshop Deploy Tool 🐍\n")

def run_cmd(command, capture_output=False, shell=False):
    if capture_output:
        result = subprocess.run(command, check=True, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    else:
        subprocess.run(command, check=True, shell=shell)

def check_docker_daemon():
    try:
        run_cmd("docker info", capture_output=True)
    except subprocess.CalledProcessError:
        console.print(
            "[red]❌ Docker daemon does not appear to be running. "
            "Please start Docker and try again.[/red]"
        )
        sys.exit(1)

def deploy(version):
    check_docker_daemon()

    console.print(f"👉 [bold yellow]Switching to version {version}[/bold yellow]")

    # Replace main.py
    source_file = f"app/main_v{version}.py"
    target_file = "app/main.py"
    if not os.path.exists(source_file):
        console.print(f"[red]❌ File {source_file} not found![/red]")
        sys.exit(1)

    shutil.copy(source_file, target_file)
    console.print(f"✅ Replaced [green]{target_file}[/green]")

    # Stop any running container on port 3000
    container_ids = run_cmd(
        "docker ps --filter 'publish=3000' --format '{{.ID}}'", capture_output=True
    )
    if container_ids:
        console.print("⚠️  A container is running on port 3000. Stopping and removing it...")
        for cid in container_ids.splitlines():
            run_cmd(f"docker stop {cid}")
            run_cmd(f"docker rm {cid}")

    # Remove previous container with same name
    container_name = f"chaos-app-v{version}"
    exists = run_cmd(f"docker ps -aq -f name={container_name}", capture_output=True)
    if exists:
        console.print(f"⚠️  Removing previous container named {container_name}...")
        run_cmd(f"docker stop {container_name}")
        run_cmd(f"docker rm {container_name}")

    # Build image
    console.print("🔨 Building Docker image...")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task("Building Docker image...", total=None)
        run_cmd(f"docker build -t ci-cd-chaos-app:v{version} .")

    # Run container
    console.print(f"🚀 Running container chaos-app-v{version}...")
    run_cmd(f"docker run -d -p 3000:3000 --name {container_name} ci-cd-chaos-app:v{version}")

    # Run Docker analysis
    console.print("📊 Generating Docker analysis report...")
    run_cmd(f"python3 workshop_tools/docker_analysis.py {version}")

    # Output clickable report path
    report_path = f"reports/version_{version}/docker_report.html"
    if Path(report_path).exists():
        console.print(f"✅ Deployment complete for version [bold green]{version}[/bold green]!")
        console.print(f"👉 [cyan]View Docker report here:[/cyan] {report_path}")
    else:
        console.print(f"[yellow]⚠️ Docker report not found at {report_path}[/yellow]")

if __name__ == "__main__":
    print_banner()

    if len(sys.argv) < 2:
        console.print("[red]❌ Please provide a version number. Example:[/red]")
        console.print("    python3 workshop_tools/deploy_version.py 3")
        sys.exit(1)

    version = sys.argv[1]
    deploy(version)
