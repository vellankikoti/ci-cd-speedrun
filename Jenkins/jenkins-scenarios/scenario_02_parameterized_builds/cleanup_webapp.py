#!/usr/bin/env python3
"""
Cleanup script for Jenkins Scenario 2 Web Application
Stops any running webapp servers and cleans up files
"""

import os
import signal
import sys
import time

def cleanup_webapp():
    """Clean up webapp processes and files"""
    print("🧹 Cleaning up webapp processes...")
    
    # Check if webapp directory exists
    if not os.path.exists("webapp"):
        print("✅ No webapp directory found - nothing to clean up")
        return True
    
    # Stop webapp server if running
    pid_file = "webapp/webapp.pid"
    if os.path.exists(pid_file):
        try:
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            print(f"🛑 Stopping webapp server (PID: {pid})...")
            try:
                os.kill(pid, signal.SIGTERM)
                time.sleep(2)
                
                # Check if process is still running
                try:
                    os.kill(pid, 0)
                    print(f"⚠️  Process still running, force killing...")
                    os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    print("✅ Webapp server stopped successfully")
            except ProcessLookupError:
                print("✅ Webapp server was not running")
        except (ValueError, FileNotFoundError):
            print("⚠️  Invalid PID file")
    
    # Clean up files
    cleanup_files = [
        "webapp/webapp.pid",
        "webapp/webapp.port", 
        "webapp/webapp.log"
    ]
    
    for file_path in cleanup_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️  Removed {file_path}")
            except OSError as e:
                print(f"⚠️  Could not remove {file_path}: {e}")
    
    print("✅ Cleanup completed successfully!")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage: python3 cleanup_webapp.py")
        print("Stops any running webapp servers and cleans up files")
        sys.exit(0)
    
    success = cleanup_webapp()
    sys.exit(0 if success else 1)
