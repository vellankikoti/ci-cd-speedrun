#!/usr/bin/env python3
"""
Cleanup script for Scenario 2: Parameterized Builds
Cleans up resources created by the demo
"""

import os
import sys
import time

def print_header(title):
    """Print a beautiful header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def cleanup_demo_files():
    """Clean up demo files"""
    print_header("🧹 Cleaning Up Demo Files")
    
    files_to_remove = [
        'demo.html',
        'demo_interactive.pyc',
        '__pycache__'
    ]
    
    removed_count = 0
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                if os.path.isdir(file):
                    import shutil
                    shutil.rmtree(file)
                    print(f"   ✅ Removed directory: {file}")
                else:
                    os.remove(file)
                    print(f"   ✅ Removed file: {file}")
                removed_count += 1
            except Exception as e:
                print(f"   ❌ Failed to remove {file}: {e}")
        else:
            print(f"   ℹ️  File not found: {file}")
    
    print(f"\n📊 Cleanup Summary:")
    print(f"   • Files/directories removed: {removed_count}")
    print(f"   • Jenkins pipeline: Preserved")
    print(f"   • Demo scripts: Preserved")

def show_cleanup_info():
    """Show cleanup information"""
    print_header("ℹ️  Cleanup Information")
    
    print("""
🧹 What was cleaned up:
   • Demo HTML files
   • Python cache files
   • Temporary files

🔒 What was preserved:
   • Jenkins pipeline (Jenkinsfile)
   • Demo scripts (demo_simple.py, demo_interactive.py)
   • Documentation (scenario_02_parameterized_builds.md)

📋 Manual cleanup (if needed):
   • Jenkins jobs: Delete from Jenkins UI
   • Docker containers: docker system prune
   • Log files: Check Jenkins logs directory

🎯 To run the demo again:
   • python3 demo_simple.py
   • python3 demo_interactive.py
   • Follow Jenkins setup instructions
""")

def main():
    """Main function"""
    print("🚀 Starting cleanup for Scenario 2: Parameterized Builds")
    
    try:
        cleanup_demo_files()
        show_cleanup_info()
        
        print("\n✅ Cleanup completed successfully!")
        print("🎓 Thanks for learning about Jenkins parameterized builds!")
        
    except Exception as e:
        print(f"\n❌ Cleanup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()