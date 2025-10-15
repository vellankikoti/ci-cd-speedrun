#!/usr/bin/env python3
"""
Run the Show - Automatic Launcher
=================================

Automatically activates virtual environment and runs the reality engine.
Handles all the setup so you just run: python3 run_show.py

Usage:
    python3 run_show.py
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main launcher function"""
    print("🎭 Starting The Reality Engine...")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("reality_engine.py").exists():
        print("❌ Error: reality_engine.py not found!")
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
    print("✅ Starting reality engine...")
    print()
    
    # Run the reality engine
    try:
        # Use shell=True to ensure proper environment inheritance
        subprocess.run(f"{python_cmd} reality_engine.py", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running reality engine: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Reality engine stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()
