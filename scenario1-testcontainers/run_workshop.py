#!/usr/bin/env python3
"""
Run the Workshop - Automatic Launcher
=====================================

Automatically activates virtual environment and runs the workshop.
Handles all the setup so you just run: python3 run_workshop.py

Usage:
    python3 run_workshop.py
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main launcher function"""
    print("🎓 Starting The Workshop...")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("workshop.py").exists():
        print("❌ Error: workshop.py not found!")
        print("   Make sure you're in the scenario1-testcontainers directory")
        sys.exit(1)
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found!")
        print("   Run: python3 fix_venv.py")
        sys.exit(1)
    
    # Determine the correct Python executable
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # macOS/Linux
        python_cmd = "venv/bin/python"
    
    # Check if the Python executable exists
    if not Path(python_cmd).exists():
        print(f"❌ Python executable not found: {python_cmd}")
        print("   Run: python3 fix_venv.py")
        sys.exit(1)
    
    print("✅ Virtual environment found")
    print("✅ Starting workshop...")
    print()
    
    # Run the workshop
    try:
        # Run in interactive mode
        subprocess.run([python_cmd, "workshop.py"], check=True, stdin=sys.stdin)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running workshop: {e}")
        print("   Note: Workshop requires interactive terminal")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Workshop stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()
